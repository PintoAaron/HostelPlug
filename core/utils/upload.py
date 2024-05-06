import logging
from firebase_admin import storage


logger = logging.getLogger(__name__)


def upload_image_to_storage_bucket_and_produce_url(file):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file.name)

        blob.upload_from_file(file.file)

        blob.make_public()
        logger.info(f"Success - Image uploaded to storage")
        return blob.public_url
    except Exception as e:
        logger.error(f"Error - failed to upload image to storage: {e}")
        return False