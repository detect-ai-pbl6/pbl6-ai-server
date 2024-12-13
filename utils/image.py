import logging
import os
import uuid
from io import BytesIO

import requests
from PIL import Image

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ImageProcessingError(Exception):
    """Custom exception for image processing errors."""

    pass


def download_and_process_image(url: str) -> str:
    """
    Download and process an image from a given URL.

    Args:
        url (str): The URL of the image to download and process.

    Returns:
        str: Path to the saved PNG image.

    Raises:
        ImageProcessingError: If there are issues downloading or processing the image. # noqa
    """
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        logger.info(f"Content-Type: {content_type}")

        if not content_type or not content_type.startswith("image/"):
            raise ImageProcessingError("The URL does not point to an image.")

        if "gif" in content_type.lower():
            logger.warning("GIF files are not supported.")
            raise ImageProcessingError("GIF files are not supported.")

        try:
            img = Image.open(BytesIO(response.content))
        except Exception as e:
            raise ImageProcessingError(f"Failed to open image: {str(e)}")

        logger.info(f"Image format detected: {img.format}")

        if img.format != "PNG":
            logger.info(
                f"Image is in {img.format} format. Converting to PNG..."
            )  # noqa
            img = img.convert("RGBA")
        else:
            logger.info("Image is already in PNG format.")

        output_filename = f"{uuid.uuid4().hex}.png"

        try:
            img.save(output_filename, format="PNG")
        except Exception as e:
            raise ImageProcessingError(f"Failed to save image: {str(e)}")

        logger.info(f"Image saved as {output_filename}")

        return output_filename

    except requests.RequestException as e:
        logger.error(f"Network error when downloading image: {str(e)}")
        raise ImageProcessingError(f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error processing image: {str(e)}")
        raise ImageProcessingError(f"Unexpected error: {str(e)}")


def safe_delete_file(file_path: str):
    """
    Safely delete a file with error handling.

    Args:
        file_path (str): Path to the file to be deleted
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Successfully deleted file: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
