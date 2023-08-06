"""Caching utilities. 
    Primarily for short-lived caching or development purposes.
"""

import time
import hashlib
import logging

from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)

# Caches store tuples: 
# key: (Expiration, Object)
_MEMCACHE: Dict[str, Tuple[Optional[float], object]] = {}

# FCACHE must be activated prior to use
_FCACHE: Optional[Dict[str, Tuple[Optional[float], object]]] = None

def _get_cache(use_file_cache: bool) -> Dict[str, Tuple[Optional[float], object]]:

    if use_file_cache:
        if _FCACHE is None:
            logger.debug("File cache selected but file cache not activated, using mem cache instead")
            cache = _MEMCACHE
        else:
            cache = _FCACHE
    else:
        cache = _MEMCACHE

    return cache

def _str_to_key(key: str) -> str:
    return hashlib.md5(key.encode()).hexdigest()
    
def save(key: str, o: object, duration_seconds: Optional[int] = None, use_file_cache: bool = False):
    key=_str_to_key(key)
    if duration_seconds == -1 or duration_seconds is None:
        expiration = None
    else:
        expiration = time.time() + duration_seconds

    cache = _get_cache(use_file_cache)
    cache[key] = (expiration, o)

def get(key: str, use_file_cache: bool = False) -> object:
    key=_str_to_key(key)
    cache = _get_cache(use_file_cache)

    if key not in cache:
        return None
    else:
        expiration, o = cache[key]

        if expiration is not None and time.time() > expiration:
            del cache[key]
            return None
        else:
            return o

def clear_caches():
    global _MEMCACHE, _FCACHE

    _MEMCACHE = {}
    if _FCACHE is None:
        return
    elif isinstance(_FCACHE, dict):
        _FCACHE = _MEMCACHE
    else: # this is a FCACHE
        _FCACHE.clear()

def activate_file_cache(directory: str):
    # by default, in memory cache is used    
    try:
        from fcache.cache import FileCache # type: ignore

        global _FCACHE
        _FCACHE = FileCache("iql", flag="cs", app_cache_dir=directory)  # type: ignore

    except Exception:
        logger.exception("Unable to initialize FCache, make sure fcache is installed: pip install fcache")
            