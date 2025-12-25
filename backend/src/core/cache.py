"""
Simple caching utilities for the AI-Powered Book Assistant
"""
import time
from typing import Any, Optional
from collections import OrderedDict


class SimpleCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        Initialize cache with max size and TTL (time-to-live in seconds)
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache = OrderedDict()
        self._timestamps = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        """
        if key not in self._cache:
            return None

        # Check if expired
        if time.time() - self._timestamps[key] > self.ttl:
            self._cache.pop(key)
            self._timestamps.pop(key)
            return None

        # Move to end (most recently used)
        value = self._cache.pop(key)
        self._cache[key] = value
        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache
        """
        # Remove oldest if at max capacity
        if len(self._cache) >= self.max_size:
            oldest_key = next(iter(self._cache))
            self._cache.pop(oldest_key)
            self._timestamps.pop(oldest_key)

        # Add new item
        self._cache[key] = value
        self._timestamps[key] = time.time()

    def delete(self, key: str) -> bool:
        """
        Delete key from cache
        """
        if key in self._cache:
            self._cache.pop(key)
            self._timestamps.pop(key)
            return True
        return False

    def clear(self) -> None:
        """
        Clear the entire cache
        """
        self._cache.clear()
        self._timestamps.clear()


# Global cache instance
cache = SimpleCache()