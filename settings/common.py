import os

from pydantic_settings import BaseSettings

env = os.getenv("ENV", "dev")


class Settings(BaseSettings):
    app_name: str = f"pbl6_{env}_ai_server"
    main_server_name: str = "detect_ai_backend"
    message_broker_username: str
    message_broker_password: str
    message_broker_host: str
    message_broker_vhost: str

    @property
    def message_broker_url(self) -> str:
        return (
            f"amqp://{self.message_broker_username}:"
            f"{self.message_broker_password}@"
            f"{self.message_broker_host}/"
            f"{self.message_broker_vhost}"
        )
