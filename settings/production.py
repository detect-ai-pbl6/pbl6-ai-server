import os

from .common import Settings as CommmonSettings


class Settings(CommmonSettings):
    message_broker_username: str = os.getenv("MESSAGE_BROKER_USERNAME", "")
    message_broker_password: str = os.getenv("MESSAGE_BROKER_PASSWORD", "")
    message_broker_host: str = os.getenv("MESSAGE_BROKER_HOST", "")
    message_broker_vhost: str = os.getenv("MESSAGE_BROKER_VHOST", "")
    trained_model_path: str = "model.pth"
