import logging
import traceback

import torch
from celery import shared_task
from PIL import Image
from torchvision import transforms

from main import celery as celery_app
from main import settings as app_settings
from utils.image import ImageProcessingError  # noqa
from utils.image import download_and_process_image, safe_delete_file
from utils.model import load_model

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@shared_task(name=f"{app_settings.app_name}.predict")
def predict_image(payload):

    saved_file = None
    image_url = payload["image_url"]
    prediction = {
        "image_url": image_url,
        "log_id": payload["log_id"],
        "email": payload["email"],
    }
    try:
        saved_file = download_and_process_image(image_url)
        model = load_model(app_settings.trained_model_path)
        transform = transforms.Compose(
            [
                transforms.ToTensor(),  # Convert to tensor
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
        image = Image.open(saved_file).convert("RGB")
        image_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            prob = model(image_tensor).sigmoid().item()
            prediction.update(
                {
                    "status": "success",
                    "prediction": {
                        "type": "Synthetic" if prob > 0.5 else "Real",
                        "confidence_percentage": f"{prob * 100:.2f}%",
                    },
                }
            )

    except ImageProcessingError as e:
        logger.error(f"Image Processing Error: {str(e)}")
        prediction.update(
            {
                "status": "failed",
                "prediction": {},
                "error": str(e),
            }
        )

    except Exception as e:
        logger.error(f"Unexpected Error: {traceback.format_exc()}")
        prediction.update(
            {
                "status": "failed",
                "prediction": {},
                "error": str(e),
            }
        )
    finally:
        if saved_file:
            safe_delete_file(saved_file)

    logger.info(f"Prediction result: {prediction}")
    message = {
        **prediction,
    }
    celery_app.send_task(
        f"{app_settings.main_server_name}.predict_result",
        queue=f"{app_settings.main_server_name}_queue",
        args=(message,),
    )
