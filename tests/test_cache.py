import pytest
import time
from app.core.cache import SemanticPolicyCache

def test_cache_hit_and_miss():
    cache = SemanticPolicyCache(default_ttl=10)
    assert cache.get("water_policy") is None
    assert cache.misses == 1

    cache.set("water_policy", {"chunks": [1, 2, 3]})
    hit = cache.get("water_policy")
    assert hit == {"chunks": [1, 2, 3]}
    assert cache.hits == 1
    assert cache.hit_rate == 50.0

def test_cache_expiration():
    cache = SemanticPolicyCache(default_ttl=1)
    cache.set("short_key", "value", ttl=1)
    assert cache.get("short_key") == "value"
    time.sleep(1.1)
    assert cache.get("short_key") is None
