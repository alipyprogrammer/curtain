from django.db import models
import os
from user.models import User
from django.core.exceptions import ValidationError
from img.models import Img
from django.contrib.contenttypes.models import ContentType

# ==============================================
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext
# ==============================================
def upload_image_path_slider(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.name}{ext}"
    return f"Ui/Slider/{final_name}"

def upload_image_path_banner(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.name}{ext}"
    return f"Ui/Banner/{final_name}"


# ==============================================

# image Box
#############################
class Slider(Img):
    name    = models.CharField(max_length=200)
    mobile  = models.BooleanField(default=False)
    summery = models.TextField(max_length=350)
    status  = models.BooleanField(default=True)
    link    = models.CharField(max_length=200,  null=True,  blank=True)
    def __str__(self):
        return self.name


class Banner(Img):
    name    = models.CharField(max_length=250,  null=True, blank=True)
    status  = models.BooleanField(default=True)
    link    = models.CharField(max_length=200,  null=True,  blank=True)
    def __str__(self):
        return self.name

# image Box
#############################


# header
##################
class MenuItem(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    index = models.IntegerField(default=1)
    def __str__(self):
        return self.name

class MenuItemTitle(models.Model):
    title = models.CharField(max_length=250)
    item = models.ManyToManyField(MenuItem)
    def __str__(self):
        return self.title
class Menu(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    menu_item = models.ManyToManyField(MenuItemTitle, blank=True)
    def __str__(self):
        return self.title
class NavBar(models.Model):
    name = models.CharField(max_length=250, unique=True)
    idd  = models.CharField(max_length=250, unique=True)
    menu = models.ManyToManyField(Menu, blank=True)
    def __str__(self):
        return self.name

# header
##################


# box
###########################################

class Box(models.Model):
    idd                  = models.CharField(max_length=250, null=True, blank=True, unique=True)
    name                 = models.CharField(max_length=250, null=True, blank=True, unique=False)
    img                  = models.ManyToManyField(Img, blank=True)
    content_type         = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    content_type_setting = models.JSONField(null=True, blank=True)

# box
###########################################

class Page(models.Model):
    header         = models.ForeignKey(NavBar, on_delete=models.SET_NULL, null=True)
    slider         = models.ManyToManyField(Slider)
    banner         = models.ManyToManyField(Banner)
    box            = models.ManyToManyField(Box, blank=True)
    status         = models.BooleanField(default=False)
    idd            = models.CharField(max_length=20, default='')
