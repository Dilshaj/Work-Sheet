import os
import sys
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load env file manually
load_dotenv(".env")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def test_upload():
    try:
        # Create a dummy image or use base64
        import base64
        dummy_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
        response = cloudinary.uploader.upload(dummy_base64, folder="test")
        print("Upload success:", response.get("secure_url"))
    except Exception as e:
        print("Upload failed:", str(e))

if __name__ == "__main__":
    test_upload()
