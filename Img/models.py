import os
from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
# ==============================================
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext
# ==============================================
def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    file_name = f"{instance.file_name}{ext}"
    content_type_name = slugify(str(instance.content_type))  # Converts to "admin-log-entry"

    return f"{content_type_name}/{file_name}"
# ==============================================




class Img(PolymorphicModel):
    image        = models.ImageField(null=True, blank=True,  upload_to=upload_image_path)
    href         = models.CharField(max_length=250, null=True, blank=True)
    file_name    = models.CharField(max_length=30, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)


