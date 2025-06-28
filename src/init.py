from first_project.src.config import settings
from first_project.src.connectors.redis_connector import RedisManager

redis_manager = RedisManager(settings.REDIS_HOST, settings.REDIS_PORT)