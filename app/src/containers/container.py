from dependency_injector import containers, providers

from core.config import Settings
from services.request_service import DataGetter


class Container(containers.DeclarativeContainer):
    settings: providers.Singleton[Settings] = providers.Singleton(Settings)
    #redis_conn = providers.Resource(get_redis, settings_mock().redis_host, settings_mock().redis_port)

    request_service: providers.Singleton[DataGetter] = providers.Singleton(DataGetter)
