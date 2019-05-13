"""
Helper functions to acquire locks
"""

import logging
from datetime import timedelta
from functools import wraps

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import redis_lock
from redis import StrictRedis


REDIS_LOCK_URL = getattr(settings, 'REDIS_LOCK_URL', False)

DEFAULT_PREFIX = getattr(settings, 'REDIS_LOCK_DEFAULT_PREFIX', 'acquires_lock')


logger = logging.getLogger('tg-utils.lock')
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)


def get_redis_connection():
    if not REDIS_LOCK_URL:
        raise ImproperlyConfigured("To use locking, set REDIS_LOCK_URL in your settings.py")

    return StrictRedis.from_url(REDIS_LOCK_URL)


def get_lock(resource, expires):
    # Seconds from now on
    if isinstance(expires, timedelta):
        expires = expires.total_seconds()

    return redis_lock.Lock(get_redis_connection(), resource, expire=expires)


def acquires_lock(expires, should_fail=True, should_wait=False, resource=None, prefix=DEFAULT_PREFIX, create_id=None):
    """
    Decorator to ensure function only runs when it is unique holder of the resource.

    Any invocations of the functions before the first is done
    will raise RuntimeError.

    Locks are stored in redis with default prefix: `lock:acquires_lock`

    Arguments:
        expires(timedelta|int): Expiry time of lock, way more than expected time to run.
                            Intended as a failsafe clean-up mechanism.
        should_fail(bool): Should error be raised if failed to acquire lock.
        should_wait(bool): Should this task wait for lock to be released.
        resource(str): Resource identifier, by default taken from function name.
        prefix(str): Change prefix added to redis key (the 'lock:' part will always be added)
        create_id(function): Change suffix added to redis key to lock only specific function call based on arguments.

    Example:

        You have a celery task and you want to ensure it is never
        executed concurrently:

        @shared_task
        @acquire_lock(60, resource='foo')
        def foo():
            ...
    """
    # This is just a tiny wrapper around redis_lock
    # 1) acquire lock or fail
    # 2) run function
    # 3) release lock

    def decorator(f):
        nonlocal resource

        if resource is None:
            resource = f.__name__

        resource = '%s:%s' % (prefix, resource)

        @wraps(f)
        def wrapper(*args, **kwargs):
            lock_suffix = None

            if create_id:
                lock_suffix = create_id(*args, **kwargs)

            # The context manager is annoying and always blocking...
            lock = get_lock(
                resource='%s:%s' % (resource, lock_suffix) if lock_suffix else resource,
                expires=expires,
            )
            lock_acquired = False

            # Get default lock blocking mode
            # Copying to local variable so original variable would not be touched
            nonlocal should_wait
            is_blocking = should_wait

            should_execute_if_lock_fails = False
            if 'should_execute_if_lock_fails' in kwargs:
                should_execute_if_lock_fails = kwargs.pop("should_execute_if_lock_fails")

            # If decorated fn is called with should_wait kwarg
            # Override lock blocking mode
            if 'should_wait' in kwargs:
                is_blocking = kwargs.pop('should_wait')

                if is_blocking:
                    logger.debug('Waiting for resource "%s"', resource)

            if not lock.acquire(blocking=is_blocking):
                if should_fail:
                    raise RuntimeError("Failed to acquire lock: %s" % resource)

                logger.warning('Failed to acquire lock: %s', resource)
                if not should_execute_if_lock_fails:
                    return False

            else:
                lock_acquired = True

            try:
                return f(*args, **kwargs)
            finally:
                try:
                    if lock_acquired:
                        lock.release()
                except Exception as e:
                    logger.exception('Failed to release lock: %s', str(e), exc_info=False)

        return wrapper

    return decorator
