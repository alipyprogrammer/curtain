from django.db import models
from django.utils import timezone
from datetime import datetime

from Product.models import Product, Properties
from User.models import User
import uuid

class Agency(models.Model):
    code = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=36, unique=True)

class Type(models.Model):
    agency =  models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    code   =  models.CharField(max_length=36, unique=True)




class PropertyItem(models.Model):
    fittngs         = models.IntegerField(null=True, blank=True)
    help_price      = models.IntegerField(null=True, blank=True)
    lentgh            = models.IntegerField(null=True, blank=True)
    width          = models.DecimalField(default=1.0, max_digits=4, decimal_places=2)
    count_in_stock  = models.IntegerField(null=True, blank=True, default=0)
    salary          = models.IntegerField(null=True, blank=True, default=0)
    create_date     = models.DateTimeField(default=timezone.now)
    update_date     = models.DateTimeField(auto_now=True)

class FactorItem(models.Model):
    product          = models.ForeignKey(Product, on_delete=models.CASCADE)
    property         = models.ManyToManyField(PropertyItem)
    count            = models.IntegerField(default=1)
    date_available   = models.IntegerField(default=3)
    gold_price      = models.IntegerField(default=0)
    pre_cost_percent = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    update_date      = models.DateTimeField(auto_now=True)
    create_date      = models.DateTimeField(default=timezone.now)

class Factor(models.Model):
    name             = models.CharField(max_length=100, default="")
    user             = models.ForeignKey(User, on_delete=models.CASCADE)
    serial           = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    item             = models.ManyToManyField(FactorItem, through='FactorItemShip', blank=True)
    address          = models.TextField()
    city             = models.TextField(default='')
    post_code        = models.TextField(max_length=10)
    mobile           = models.CharField(max_length=11)
    pay_status       = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    has_2fa          = models.BooleanField(default=False)
    status_code      = models.IntegerField(default=0)
    type_ads         = models.CharField(max_length=36, null=True, blank=True)

#ship
###################
class FactorItemShip(models.Model):
    factor        = models.ForeignKey(Factor, on_delete=models.CASCADE)
    item          = models.ForeignKey(FactorItem, on_delete=models.CASCADE)
    created_at    = models.DateField(auto_now_add=True)
#ship
###################

class Card(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    property    = models.ForeignKey(Properties, on_delete=models.CASCADE)
    count       = models.IntegerField(default=1)
    date_joined = models.DateField(null=True, blank=True)

class CodeFactor(models.Model):
    code     = models.CharField(max_length=150)
    factor   = models.ForeignKey(Factor, on_delete=models.CASCADE)
    createAt =  models.DateTimeField(auto_now_add=True)

class ValidateFactor(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tracking_id = models.CharField(max_length=35)

    # def __str__(self):
    #     return self.user
