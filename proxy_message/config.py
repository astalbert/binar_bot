from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    name_session: str = "AndrewNikiforov"
    api_id: int = 27265516
    api_hash: str = "bf9691fa3d1c090840ec9f67fdb3c5df"
    system_version: str = "4.16.30-vxCUSTOM"
    device_model: str = " y530"
    app_version: str = "1.0"

    message_username: int = -1001983420577
    receiver_username: int = 1149273704

    kafka_host: str = '127.0.0.1:9092'
    partition_count: int = 1
    topic: str = 'aaaa'


settings = Settings()
