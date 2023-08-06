#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2021/7/24
# Author: clarkmonkey@163.com

from pathlib import Path
from typing import Tuple

####################
#    INFORMATION
####################
PROJECT: str = 'cache3'
VERSION: Tuple = (0, 3, 4, 'pre')

####################
#    DEFAULT SETTING
####################
SQLITE_TIMEOUT: int = 30  # 30s
DEFAULT_TIMEOUT: float = 600.0  # 300s
CACHE_NAME: str = 'cache3'
CACHE_STORE: Path = Path('~/.cache3')

####################
#    LIMIT SETTING
####################
# MAX_KEY_LENGTH: int = 1 << 10    # 1K
# MIN_KEY_LENGTH: int = 1
# MAX_TIMEOUT: int = 365 * 24 * 60 * 60
# MIN_TIMEOUT: int = 0
#
# LRU_EVICT: str = 'lru'
