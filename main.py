from fastapi import FastAPI, status, HTTPException
from celery import Celery

import os

if os.getenv("ENV", "dev") == "dev":
    from settings.local import Settings
else:
    from settings.production import Settings

settings = Settings()
app = FastAPI()

celery = Celery(settings.app_name)
celery.conf.update(imports=["tasks"])
celery.conf.broker_url = settings.message_broker_url
celery.conf.result_backend = "rpc://"
celery.conf.task_default_queue = f"{settings.app_name}_queue"
celery.conf.broker_connection_retry_on_startup = True


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    if bool(celery.control.inspect().active()):
        return "OK"
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
