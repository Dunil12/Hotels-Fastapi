import redis.asyncio as redis
import logging

from src.config import settings


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        """Асинхронное подключение к Redis."""
        logging.info(f"Подключение к redis ... host={settings.REDIS_HOST}, port={settings.REDIS_PORT}")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        # Можно проверить соединение
        try:
            await self.redis.ping()
            logging.info(f"Подключение к redis успешно, host={settings.REDIS_HOST}, port={settings.REDIS_PORT}")
        except Exception as e:
            logging.error(f"Failed to connect to Redis: {e}")

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