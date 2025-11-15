from pyexpat import model
from statistics import mode
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import os

# from Ads.models import Agency


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.name}{ext}"
    return f"user/{final_name}"


class Age(models.Model):
    Age = models.CharField(max_length=50 , verbose_name='سن')





class User(AbstractUser):
    name             = models.CharField(max_length=40 ,null=True , blank=True)
    mobile           = models.CharField(max_length=11 , null=True, blank=True)
    manager          = models.BooleanField(default=False)
    national_code    = models.CharField(max_length=10, null=True , blank=True)
    customer         = models.BooleanField(default=True)
    blog_manager     = models.BooleanField(default=False)
    product_manager  = models.BooleanField(default=False)
    ordering_manager = models.BooleanField(default=False)
    type_ads         = models.CharField(max_length=36, null=True, blank=True)
    def __str__(self):
        return self.username


# class UserLog(models.Model):
#     user   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     ip     = models.CharField(max_length=41)
#     url    = models.TextField(null=True , blank=True)
#     agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
#     date   = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    name      = models.CharField(max_length=40 , null=True , blank=True)
    address   = models.TextField()
    post_code = models.TextField(max_length=10)
    city      = models.TextField()
    user      = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

