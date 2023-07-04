from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The max allowed dimesion for images are 70x70- size you uploaded = {img.size}"
                )
            
def validate_image_file_extension(val):
    ext = os.path.splitext(val.name)[1]
    valid_ext = ['.jpg', '.jpeg', 'png', '.gif']
    if ext.lower() not in valid_ext:
        raise ValidationError("Unsupported file extension")