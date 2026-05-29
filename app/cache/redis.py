from redis import Redis
import json

class RedisCacheBackend:
    def __init__(self, redis_url: str, ttl_seconds: int):
        self.redis_client = Redis.from_url(redis_url)
        self.ttl_seconds = ttl_seconds

    def set(self, key: str, value: dict):
        self.redis_client.set(key, json.dumps(value), ex=3600)

    def get(self, key: str) -> dict:
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def delete(self, key: str):
        self.redis_client.delete(key)