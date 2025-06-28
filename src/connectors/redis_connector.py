import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        """Асинхронное подключение к Redis."""
        self.redis = await redis.Redis(host=self.host, port=self.port)
        # Можно проверить соединение
        try:
            await self.redis.ping()
            print("Connected to Redis")
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")

    async def set(self, key, value, expire: int = None):
        """Установить значение по ключу."""
        if self.redis is None:
            raise RuntimeError("Redis connection is not established.")
        await self.redis.set(key, value, expire)

    async def get(self, key):
        """Получить значение по ключу."""
        if self.redis is None:
            raise RuntimeError("Redis connection is not established.")
        return await self.redis.get(key)

    async def delete(self, key):
        """Удалить ключ."""
        if self.redis is None:
            raise RuntimeError("Redis connection is not established.")
        await self.redis.delete(key)

    async def close(self):
        """Закрыть соединение с Redis."""
        if self.redis:
            await self.redis.close()