from celery import shared_task
from main import celery as celery_app, settings as app_settings


@shared_task(name=f"{app_settings.app_name}.predict")
def predict_image(x, y):
    celery_app.send_task(
        f"{app_settings.main_server_name}.predict_result",
        queue=f"{app_settings.main_server_name}_queue",
    )
    return x + y
