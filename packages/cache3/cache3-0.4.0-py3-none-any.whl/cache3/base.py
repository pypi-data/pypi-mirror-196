#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2021/7/24
# Author: clarkmonkey@163.com

import functools
import hashlib
import pickle
from abc import ABC, abstractmethod
from typing import (
    Any, Type, Optional, Dict, Callable, NoReturn, List, Tuple, Iterable, Set
)

from cache3.utils import empty, cached_property, Time, Number, current
from cache3.validate import NumberValidate, StringValidate, EnumerateValidate

try:
    import ujson as json
except ImportError:
    import json

TG: Type = Optional[str]
VT: Type = int
VH: Type = Callable[[Any, VT], NoReturn]


class CacheKeyWarning(RuntimeWarning):
    """A warning that is thrown when the key is not legitimate """


class InvalidCacheKey(ValueError):
    """ An error thrown when the key invalid """


class NotImplementedEvictError(NotImplementedError):
    """ An error thrown when not implement evict method """


class AbstractCache(ABC):
    """ A base class that specifies the API that caching
    must implement and some default implementations.

    The processing logic of cache keys and values is as follows：

        key:
            serial_key(key)         ->  sk
            restore(store_key)      ->  key

        value:
            serial_value(value)          -> sv
            deserialize_value(sv)        -> value
    """

    max_size: int = NumberValidate(minvalue=0)
    name: StringValidate = StringValidate(minsize=1)

    def set(self, key: Any, value: Any, timeout: Time = None, tag: TG = None) -> bool:
        """ set a value in the cache. Use timeout for the key if
        it's given, Otherwise use the default timeout.
        """
        sk: str = self.serial_key(key)
        sv: Any = self.serial_value(value)
        return self._store(sk, sv, timeout, tag)

    def get(self, key: Any, default: Any = None, tag: TG = None) -> Any:
        """ Fetch a given key from the cache. If the key does not exist, return
        default, which itself defaults to None.
        """
        sk: str = self.serial_key(key)
        try:
            sv = self._load(sk, tag)
        except KeyError:
            return default
        else:
            return self.deserialize_value(sv)

    def ex_set(self, key: Any, value: Any, timeout: Time = None, tag: TG = None) -> bool:
        """ Set a value in the cache if the key does not already exist. If
        timeout is given, use that timeout for the key; otherwise use the
        default cache timeout.

        Return True if the value was stored, False otherwise.
        """
        sk: str = self.serial_key(key)
        sv: Any = self.serial_value(value)
        return self._ex_store(sk, sv, timeout, tag)

    def has_key(self, key: Any, tag: str = None) -> bool:
        """ Return True if the key is in the cache and has not expired. """

        sk: str = self.serial_key(key)
        return self._has_key(sk, tag)

    def incr(self, key: Any, delta: Number = 1, tag: TG = None) -> Number:
        """ Add delta to value in the cache.

        If the key does not exist, raise a ValueError exception.
        """
        sk: str = self.serial_key(key)
        return self._incr(sk, delta, tag)

    def decr(self, key: Any, delta: Number = 1, tag: TG = None) -> Number:
        """ Subtract delta from value in the cache.

        If the key does not exist, raise a ValueError exception.
        """

        return self.incr(key, -delta, tag)

    def inspect(self, key: Any, tag: TG = None) -> Optional[Dict[str, Any]]:
        """Displays the information of the key value if it exists in cache.
        Returns the details if the key exists, otherwise None."""

        sk: str = self.serial_key(key)
        info: Optional[Dict[str, Any]] = self._inspect(sk, tag)
        if info:
            info['key'] = self.serial_key(info['serial_key'])
            info['value'] = self.serial_key(info['serial_value'])
        return info

    def touch(self, key: Any, timeout: Time, tag: TG = None) -> bool:
        """ Update the key's expiry time using timeout. Return True if successful
        or False if the key does not exist."""

        sk: str = self.serial_key(key)
        return self._touch(sk, timeout, tag)

    @abstractmethod
    def _get_many(self, sks: Set[str], tag: TG) -> Iterable[Any]:
        """"""

    def get_many(self, keys: List[str], tag: TG = None) -> Dict[str, Any]:
        """ Fetch a bunch of keys from the cache. For certain backends (memcached,
        pgsql) this can be *much* faster when fetching multiple values.

        Return a dict mapping each key in keys to its value. If the given
        key is missing, it will be missing from the response dict.
        """
        sks: Set[str] = set((self.serial_key(key) for key in keys))
        svs: Iterable[Any] = self._get_many(sks, tag)
        return dict(zip(sks, svs))

    def memoize(self, tag: TG = None, timeout: Time = None) -> Callable:
        """ The cache is decorated with the return value of the function,
        and the timeout is available. """

        if callable(tag):
            raise TypeError(
                """
                %r cannot be callable. 
                Sample:
                    @cache.memoize()
                    def foo():
                        ...
                """ % tag
            )

        def decorator(func) -> Callable[[Callable[[Any], Any]], Any]:
            """ Decorator created by memoize() for callable `func`."""

            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                """Wrapper for callable to cache arguments and return values."""
                value: Any = self.get(func.__name__, empty, tag)
                if value is empty:
                    value: Any = func(*args, **kwargs)
                    self.set(func.__name__, value, timeout, tag)
                return value
            return wrapper

        return decorator

    def delete(self, key: Any, tag: TG = None) -> bool:

        """ Delete a key from the cache

        Return True if delete success, False otherwise.
        """
        sk: str = self.serial_key(key)
        return self._delete(sk, tag)

    def ttl(self, key: Any, tag: TG = None) -> Time:
        """ Return the Time-to-live value. """
        qt: Time = current()
        sk: str = self.serial_key(key)
        return self._ttl(sk, tag, qt)

    def serial_key(self, key: Any) -> str:
        """ Default function to generate keys.

        Construct the key used by all other methods. By default,
        the key will be converted to a unified string format
        as much as possible. At the same time, subclasses typically
        override the method to generate a specific key.
        """
        return key

    def serial_value(self, value: Any) -> str:
        """ Serialize the value for easy backend storage.
        By default, return directly to value doing nothing.
        """
        return value

    def deserialize_key(self, dump: Any) -> str:
        """"""
        return dump

    def deserialize_value(self, dump: Any) -> Any:
        """"""
        return dump

    @abstractmethod
    def _store(self, sk: str, sv: Any, timeout: Time, tag: str) -> bool:
        """ push k-v pair to cache and set expire time """

    @abstractmethod
    def _load(self, sk: str, tag: str) -> Any:
        """ Load value from self(cache)

        Args:
            sk: serial key
            default: will return default when not found key in the tag namespace
            tag: k-v pair tag namespace

        Returns:
            deserialize value, not value!
        """

    @abstractmethod
    def _ex_store(self, sk: str, sv: Any, timeout: Time, tag: TG) -> bool:
        """"""

    @abstractmethod
    def _has_key(self, sk: str, tag: TG) -> bool:
        """"""

    @abstractmethod
    def _incr(self, sk: str, delta: Number, tag: TG) -> Number:
        """"""

    @abstractmethod
    def _inspect(self, sk: str, tag: TG) -> Optional[Dict[str, Any]]:
        """"""

    @abstractmethod
    def _touch(self, sk: str, timeout: Time, tag: TG) -> bool:
        """"""

    @abstractmethod
    def _iter(self, tag: str = None, qt: Time = None) -> Iterable[Tuple[str, Any]]:
        """"""

    def iter(self, tag: str = None) -> Iterable[Tuple[str, Any]]:
        qt: Time = current()
        for sk, sv in self._iter(tag, qt):
            yield self.deserialize_key(sk), self.deserialize_value(sv)

    @abstractmethod
    def _delete(self, sk: str, tag: TG = None) -> bool:
        """"""

    @abstractmethod
    def _ttl(self, sk: str, tag: TG, qt: Time) -> Time:
        """  """

    @abstractmethod
    def clear(self) -> bool:
        """ clear all caches. """

    def __repr__(self) -> str:
        return '<%s max_size=%d>' % (self.__class__.__name__, self.max_size)

    @abstractmethod
    def __iter__(self) -> Iterable[Tuple[str, Any, str]]:
        """ Iterator of cache """

    @abstractmethod
    def __len__(self) -> int:
        """Return the cache items count."""


class JSONMixin:

    @staticmethod
    def deserialize(dump: Any, *args, **kwargs) -> Any:
        if isinstance(dump, (int, float, bytes)):
            return dump
        return json.loads(dump)

    @staticmethod
    def serialize(value: Any, *args, **kwargs) -> Any:
        if isinstance(value, (int, float, bytes)):
            return value
        return json.dumps(value)


class PickleMixin:

    @staticmethod
    def deserialize_value(dump: Any) -> Any:
        """ In order to save overhead, it is more important to implement incr
        in SQLite layer """
        if isinstance(dump, (int, float, str)):
            return dump
        return pickle.loads(dump)

    @staticmethod
    def serial_value(value: Any) -> Any:
        """ incr by sqlite statement """
        if isinstance(value, (int, float, str)):
            return value
        return pickle.dumps(value)


class HashKeyMixin:

    @staticmethod
    def deserialize_key(dump: Any) -> Any:
        return 'md5:%s' % dump

    @staticmethod
    def serial_key(key: Any) -> str:
        return hashlib.md5(str(key).encode('latin')).hexdigest()
