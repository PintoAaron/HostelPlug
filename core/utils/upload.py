from firebase_admin import storage


def upload_image_to_storage_bucket_and_produce_url(file):
    bucket = storage.bucket()
    blob = bucket.blob(file.name)

    blob.upload_from_file(file.file)

    blob.make_public()

    return blob.public_url