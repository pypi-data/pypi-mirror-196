#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# date: 2023/1/20

from typing import Type, NoReturn, Any
from cache3.base import AbstractCache
from threading import Lock


class MultiCache:

    def __init__(self) -> None:
        self.__bucket = {}
        self._lock = Lock()

    def create(self, name: str, cache: AbstractCache) -> NoReturn:

        if not isinstance(cache, AbstractCache):
            raise ValueError(
                'cache must allowed AbstractCache'
            )

        with self._lock:
            if name in self.__bucket:
                raise KeyError(
                    'cache bucket named %r has been created' % name
                )
            self.__bucket[name] = cache


    def __getattr__(self, item) -> Any:

        def wrapper(name, *args, **kwargs):
            return self.proxy(item, name, *args, **kwargs)
        return wrapper

    def proxy(self, method, name: str, *args, **kwargs):
        cache: AbstractCache = self.__bucket[name]
        v = getattr(cache, method)
        if callable(v):
            return v(*args, **kwargs)
        return v
