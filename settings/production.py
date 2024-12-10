from .common import Settings as CommmonSettings


class Settings(CommmonSettings):
    message_broker_username: str = "guest"
    message_broker_password: str = "guest"
    message_broker_host: str = "localhost"
    message_broker_vhost: str = "/"
