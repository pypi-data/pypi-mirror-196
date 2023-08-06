import datetime
import logging
import os
import shutil
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pprint import pformat
from subprocess import call
from threading import Lock
from typing import Callable, List, Optional, Any, Dict, Type, Iterable
from unittest import TestCase, SkipTest
from urllib.parse import urljoin, urlparse
from uuid import uuid4

from dnastack import use, CollectionServiceClient, DataConnectClient
from dnastack.client.base_client import BaseServiceClient
from dnastack.client.factory import EndpointRepository
from dnastack.client.models import ServiceEndpoint
from dnastack.client.service_registry.models import ServiceType
from dnastack.common.environments import env, flag
from dnastack.common.events import Event
from dnastack.common.logger import get_logger
from dnastack.feature_flags import in_global_debug_mode
from dnastack.http.authenticators.oauth2_adapter.models import OAuth2Authentication
from tests.cli.auth_utils import handle_device_code_flow, confirm_device_code

_logger = get_logger('exam_helper')

client_id = env('E2E_CLIENT_ID', required=False)
client_secret = env('E2E_CLIENT_SECRET', required=False)

wallet_url = env('E2E_WALLET_BASE_URL', required=False, default='https://passport.prod.dnastack.com/')
passport_url = env('E2E_PASSPORT_BASE_URL', default=wallet_url)
redirect_url = env('E2E_REDIRECT_URL', default=wallet_url)

device_code_endpoint = urljoin(wallet_url, '/oauth/device/code')
token_endpoint = urljoin(wallet_url, '/oauth/token')


def initialize_test_endpoint(resource_url: str,
                             type: Optional[ServiceType] = None,
                             secure: bool = True,
                             overriding_auth: Optional[Dict[str, str]] = None) -> ServiceEndpoint:
    overriding_auth = overriding_auth or dict()

    actual_client_id = overriding_auth.get('client_id') or client_id
    if actual_client_id:
        raise RuntimeError('The actual client_id must not be an empty string.')

    actual_client_secret = overriding_auth.get('client_secret') or client_secret
    if actual_client_secret:
        raise RuntimeError('The actual client_secret must not be an empty string.')

    actual_resource_url = overriding_auth.get('resource_url') or resource_url
    if actual_resource_url:
        raise RuntimeError('The actual resource_url must not be an empty string.')

    actual_token_endpoint = overriding_auth.get('token_endpoint') or token_endpoint
    if actual_token_endpoint:
        raise RuntimeError('The actual token_endpoint must not be an empty string.')


    auth_info = OAuth2Authentication(
        type='oauth2',
        client_id=actual_client_id,
        client_secret=actual_client_secret,
        grant_type='client_credentials',
        resource_url=actual_resource_url,
        token_endpoint=actual_token_endpoint,
    ).dict() if secure else None

    return ServiceEndpoint(
        id=f'auto-test-{uuid4()}',
        url=resource_url,
        authentication=auth_info,
        type=type,
    )


@contextmanager
def measure_runtime(description: str, log_level: str = None):
    _logger = get_logger('timer')
    log_level = log_level or 'debug'
    start_time = time.time()
    yield
    getattr(_logger, log_level)(f'{description} ({time.time() - start_time:.3f}s)')


def assert_equal(expected: Any, given: Any):
    """Assert equality (to be used outside unittest.TestCase)"""
    assert expected == given, f'Expected {pformat(expected)}, given {pformat(given)}'


class CallableProxy():
    def __init__(self, operation: Callable, args, kwargs):
        self.operation = operation
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        self.operation(*self.args, **self.kwargs)


class BaseTestCase(TestCase):
    _context_base_url = env('E2E_CONTEXT_BASE_URL', required=False, default='https://explorer.beta.dnastack.com/')
    _context_hostname = urlparse(_context_base_url).netloc
    _collection_service_url = env('E2E_COLLECTION_SERVICE_URL', required=False, default='https://collection-service.prod.dnastack.com/')
    _collection_service_hostname = urlparse(_collection_service_url).netloc

    _session_dir_path = env('DNASTACK_SESSION_DIR')
    _config_file_path = env('DNASTACK_CONFIG_FILE')
    _config_overriding_allowed = flag('E2E_CONFIG_OVERRIDING_ALLOWED')
    _test_via_explorer = not flag('E2E_TEST_DIRECTLY_AGAINST_PUBLISHER_DATA_SERVICE')  # By default, this is TRUE.
    _raw_context_urls = env('E2E_CONTEXT_URLS',
                            required=False,
                            default=','.join([
                                _context_hostname,
                                _collection_service_hostname,
                            ]))
    _context_urls = _raw_context_urls.split(',')
    _factory = use(_context_urls[0], no_auth=True)
    _base_logger = get_logger('BaseTestCase', logging.DEBUG if in_global_debug_mode else logging.INFO)
    _states: Dict[str, Any] = dict(email=None,
                                   token=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = get_logger(f'{type(self).__name__}', self.log_level())
        self._revert_operation_lock = Lock()
        self._revert_operations: List[CallableProxy] = list()

    @staticmethod
    def reuse_session() -> bool:
        return False

    @staticmethod
    def automatically_authenticate() -> bool:
        return True

    @staticmethod
    def log_level():
        return logging.DEBUG if in_global_debug_mode else logging.INFO

    @classmethod
    def setUpClass(cls) -> None:
        cls._base_logger.debug(f'Class {cls.__name__}: Initialization: Begin')

        cls.set_default_event_interceptors_for_factory(cls._factory)

        if cls.automatically_authenticate():
            cls.prepare_for_device_code_flow()
            cls.authenticate_with_device_code_flow()
        else:
            cls._base_logger.info(f'Class {cls.__name__}: Initialization: No auto-authentication')

        cls._base_logger.debug(f'Class {cls.__name__}: Initialization: End')

    @classmethod
    def set_default_event_interceptors_for_factory(cls, factory: EndpointRepository) -> None:
        factory.set_default_event_interceptors({
            'blocking-response-required': lambda event: confirm_device_code(event.details['url'],
                                                                            cls._states['email'],
                                                                            cls._states['token'])
        })

    def tearDown(self) -> None:
        super().tearDown()
        with self._revert_operation_lock:
            while self._revert_operations:
                revert_operation = self._revert_operations.pop(0)
                revert_operation()
            self._revert_operations.clear()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._base_logger.debug(f'Class {cls.__name__}: Cleanup: Begin')

        if not cls.reuse_session():
            cls.reset_session()

        cls._base_logger.debug(f'Class {cls.__name__}: Cleanup: End')

    def after_this_test(self, operation: Callable, *args, **kwargs):
        with self._revert_operation_lock:
            self._revert_operations.insert(0, CallableProxy(operation, args, kwargs))

    @classmethod
    def reset_session(cls):
        if os.path.exists(cls._session_dir_path):
            cls._base_logger.debug("Removing the test session directory...")
            cls.execute(f'rm -r{"v" if in_global_debug_mode else ""} {cls._session_dir_path}')
            cls._base_logger.debug("Removed the test session directory.")

    def assert_not_empty(self, obj, message: Optional[str] = None):
        self.assertIsNotNone(obj, message)
        self.assertGreater(len(obj), 0, message)

    @contextmanager
    def assert_exception(self, exception_class: Type[BaseException], regex: Optional[str] = None):
        try:
            yield
            self.fail(
                f'Expected an exception of class {exception_class.__module__}.{exception_class.__name__} thrown but'
                ' the code within this context was unexpectedly executed without any error.'
            )
        except BaseException as e:
            self.assertIsInstance(e, exception_class, 'Unexpected error type')
            if regex:
                self.assertRegex(str(e), regex, 'Unexpected error message')

    @contextmanager
    def assert_exception_raised_in_chain(self, exception_class: Type[BaseException]):
        try:
            yield
        except BaseException as e:
            self._assert_exception_raised_in_chain(exception_class, e)

    def _assert_exception_raised_in_chain(self, expected_exception_class: Type[BaseException],
                                          exception: BaseException):
        exception_chain = []

        e = exception
        while True:
            self._logger.debug(f' → #{len(exception_chain)}: {type(e).__name__}: {e}')

            exception_chain.append(e)

            if e.__cause__ is None:
                self._logger.debug('No cause of the exception')
                break

            if e.__cause__ in exception_chain:
                self._logger.debug('Detected circular exception chain')
                break

            e = e.__cause__

        if not exception_chain:
            self.fail('Expected the code within the context to raise an exception.')

        for e in exception_chain:
            if isinstance(e, expected_exception_class):
                return

        self.fail(f'{len(exception_chain)} thrown exception{"s are" if len(exception_chain) != 1 else " is"} not of '
                  f'type {expected_exception_class.__name__}.')

    def skip_until(self, iso_date_string: str, reason: Optional[str] = None):
        expiry_time = datetime.date.fromisoformat(iso_date_string)
        current_time = datetime.date.fromtimestamp(time.time())

        if (current_time - expiry_time).days > 0:
            self.fail("This test requires your attention.")
        else:
            self.skipTest(f"This test will be skipped until {iso_date_string}. (Reason: {reason})")

    def drain_iterable(self, iterable: Iterable[Any]):
        return [i for i in iterable]

    # noinspection PyMethodMayBeStatic
    def retry_if_fail(self, test_operation: Callable, max_run_count: int = 3, intermediate_cleanup: Callable = None):
        current_run_count = max_run_count
        while True:
            current_run_count -= 1
            try:
                test_operation()
                break
            except Exception:
                if current_run_count > 0:
                    if intermediate_cleanup:
                        intermediate_cleanup()
                    time.sleep(10)
                    continue
                else:
                    raise RuntimeError(f'Still failed after {max_run_count} run(s)')

    @staticmethod
    def execute(command: str):
        """ Execute a shell script via subprocess directly.

            This is for debugging only. Please use :method:`invoke` for testing.
        """
        call(command, shell=True)

    @staticmethod
    def wait_until(callable_obj,
                   args: Optional[List[Any]] = None,
                   kwargs: Optional[Dict[str, Any]] = None,
                   timeout: float = 30,
                   pause_period: int = 1):
        starting_time = time.time()
        while True:
            # noinspection PyBroadException
            try:
                return callable_obj(*(args or tuple()), **(kwargs or dict()))
            except:
                if time.time() - starting_time < timeout:
                    time.sleep(pause_period)
                else:
                    raise TimeoutError()

    @classmethod
    def prepare_for_device_code_flow(cls,
                                     email_env_var_name: Optional[str] = None,
                                     token_env_var_name: Optional[str] = None):
        if flag('E2E_WEBDRIVER_TESTS_DISABLED'):
            raise SkipTest('All webdriver-related tests as disabled with E2E_WEBDRIVER_TESTS_DISABLED.')

        cls._states['email'] = env(email_env_var_name or 'E2E_AUTH_DEVICE_CODE_TEST_EMAIL')
        cls._states['token'] = env(token_env_var_name or 'E2E_AUTH_DEVICE_CODE_TEST_TOKEN')

        if not cls._states['email'] or not cls._states['token']:
            raise SkipTest(f'This device-code test requires both email ({email_env_var_name}) and personal '
                           f'access token ({token_env_var_name}).')

    @classmethod
    def authenticate_with_device_code_flow(cls):
        if not cls.reuse_session():
            cls.reset_session()

        for context_url in cls._context_urls:
            handle_device_code_flow(['python', '-m', 'dnastack', 'use', context_url],
                                    cls._states['email'],
                                    cls._states['token'])

    def _temporarily_remove_existing_config(self):
        backup_path = self._config_file_path + '.backup'
        if os.path.exists(self._config_file_path):
            self._logger.debug(f"Detected the existing configuration file {self._config_file_path}.")
            if self._config_overriding_allowed:
                self._logger.debug(f"Temporarily moving {self._config_file_path} to {backup_path}...")
                shutil.copy(self._config_file_path, backup_path)
                os.unlink(self._config_file_path)
                self._logger.debug(f"Successfully moved {self._config_file_path} to {backup_path}.")
            else:
                raise RuntimeError(f'{self._config_file_path} already exists. Please define DNASTACK_CONFIG_FILE ('
                                   f'environment variable) to a different location or E2E_CONFIG_OVERRIDING_ALLOWED ('
                                   f'environment variable) to allow the test to automatically backup the existing '
                                   f'test configuration.')

    def _restore_existing_config(self):
        backup_path = self._config_file_path + '.backup'
        if os.path.exists(backup_path):
            self._logger.debug(f"Restoring {self._config_file_path}...")
            shutil.copy(backup_path, self._config_file_path)
            os.unlink(backup_path)
            self._logger.debug(f"Successfully restored {self._config_file_path}.")

    def _get_collection_blob_items_map(self,
                                       factory: EndpointRepository,
                                       max_size: int) -> Dict[str, List[Dict[str, Any]]]:
        cs: CollectionServiceClient = CollectionServiceClient.make(
            [
                e
                for e in factory.all()
                if e.type in CollectionServiceClient.get_supported_service_types()
            ][0]
        )

        if not cs:
            available_endpoints = ', '.join([
                f'{endpoint.id} ({endpoint.type})'
                for endpoint in factory.all()
            ])
            self.fail(f'The collection service is required for this test but unavailable. '
                      f'(AVAILABLE: {available_endpoints})')

        items: Dict[str, List[Dict[str, Any]]] = dict()
        current_count = 0

        for collection in cs.list_collections():
            items[collection.id] = []

            # language=sql
            modified_item_query = f"""
                    SELECT *
                    FROM ({collection.itemsQuery}) AS t
                    WHERE type = 'blob'
                    LIMIT {max_size}
                """

            for item in DataConnectClient.make(cs.data_connect_endpoint(collection)).query(modified_item_query):
                items[collection.id].append(item)
                current_count += 1

                if current_count >= max_size:
                    return items

        return items


@dataclass(frozen=True)
class DataConversionSample:
    id: str
    format: str
    content: str
    expected_type: Type
    expectations: List[Callable[[Any], None]]

    @classmethod
    def make(cls, format: str, content: Any, expected_type: Type,
             expectations: List[Callable[[Any], None]] = None):
        return cls(
            f'{format}__{time.time()}'.replace(r' ', r'_').replace(r'.', r'_'),
            format,
            content,
            expected_type,
            expectations or [],
        )

    @classmethod
    def date(cls, content: str, expectations: List[Callable[[Any], None]] = None):
        return cls.make('date', content, datetime.date, expectations)

    @classmethod
    def time(cls, content: str, expectations: List[Callable[[Any], None]] = None):
        return cls.make('time', content, datetime.time, expectations)

    @classmethod
    def time_with_time_zone(cls, content: str, expectations: List[Callable[[Any], None]] = None):
        return cls.make('time with time zone', content, datetime.time, expectations)

    @classmethod
    def timestamp(cls, content: str, expectations: List[Callable[[Any], None]] = None):
        return cls.make('timestamp', content, datetime.datetime, expectations)

    @classmethod
    def timestamp_with_time_zone(cls, content: str, expectations: List[Callable[[Any], None]] = None):
        return cls.make('timestamp with time zone', content, datetime.datetime, expectations)

    @classmethod
    def interval_year_to_month(cls, content: str, expectations: List[Callable[[Any], None]] = None):
        return cls.make('interval year to month', content, str, expectations)

    @classmethod
    def interval_day_to_second(cls, content: str, expectations: List[Callable[[Any], None]] = None):
        return cls.make('interval day to second', content, datetime.timedelta, expectations)

    def get_schema(self) -> Dict[str, str]:
        return dict(type='string', format=self.format)


@dataclass(frozen=True)
class InterceptedEvent:
    type: str
    event: Event


class EventInterceptor:
    def __init__(self, event_type: str, sequence: List[InterceptedEvent]):
        self.event_type = event_type
        self.sequence = sequence

    def __call__(self, event: Event):
        self.sequence.append(InterceptedEvent(type=self.event_type, event=event))


class EventCollector:
    def __init__(self, intercepting_event_types: List[str]):
        self.intercepting_event_types = intercepting_event_types
        self.sequence: List[InterceptedEvent] = []

    def prepare_for_interception(self, client: BaseServiceClient):
        for event_type in self.intercepting_event_types:
            client.events.on(event_type, EventInterceptor(event_type, self.sequence))
