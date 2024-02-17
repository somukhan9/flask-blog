import os
import pathlib

from typing import List

from uuid import uuid4

from werkzeug.utils import secure_filename

# from dotenv import load_dotenv

import cloudinary
# Import the cloudinary.api for managing assets
import cloudinary.api
# Import the cloudinary.uploader for uploading assets
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

# load_dotenv()


def get_uuid4():
    return uuid4().hex


def upload_image(file, folder: str = "flask-blog/"):
    fname = file.filename
    try:
        filename = secure_filename(os.path.join(get_uuid4(), fname))

        stem = pathlib.Path(filename).stem
        result = cloudinary.uploader.upload(file,
                                            filename=filename, public_id=stem, folder=folder)

        return {"public_url": result["url"], "secure_url": result["secure_url"]}
    except Exception as ex:
        print(ex)
        print("Error while uploading image!")


def delete_image(filename: str, folder: str = "flask-blog/"):
    stem = pathlib.Path(filename).stem
    print(stem)
    print("-------------delete image--------------")
    try:
        file = folder + "/" + stem
        image_delete_result = cloudinary.uploader.destroy(
            file, resource_type="image", type="upload")

        print(image_delete_result)

        return image_delete_result
    except Exception as ex:
        print(ex)
        print("Error while deleting images!")
