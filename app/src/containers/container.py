from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dependency_injector import containers, providers

from core.config import Settings
from db.redis_storage import get_redis
from services.image_service import ImageService
from services.request_service import DataGetter


class Container(containers.DeclarativeContainer):
    settings: providers.Singleton[Settings] = providers.Singleton(Settings)
    redis = providers.Resource(get_redis,
                               settings().redis.host,
                               settings().redis.port,
                               settings().redis.db
                               )
    bot: providers.Singleton[Bot] = providers.Singleton(Bot, settings().token)
    storage: providers.Singleton[RedisStorage] = providers.Singleton(RedisStorage, redis)
    dp: providers.Singleton[Dispatcher] = providers.Singleton(Dispatcher, storage=storage)
    request_service: providers.Factory[DataGetter] = providers.Factory(DataGetter)
    image_service: providers.Factory[ImageService] = providers.Factory(ImageService)
