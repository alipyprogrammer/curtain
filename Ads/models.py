from django.db import models
# from User.models import User



class Cost(models.Model):
    date  = models.DateField()
    price = models.DecimalField(max_digits=25, decimal_places=0)

class CostShip(models.Model):
    agency_name = models.ForeignKey("Agency", on_delete=models.CASCADE)
    cost = models.ForeignKey(Cost, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now=True)


class Agency(models.Model):
    user          = models.ForeignKey('User.User', on_delete=models.SET_NULL, null=True, blank=True)
    name          = models.CharField(max_length=50,null=True,blank=True, unique=True)
    cost          = models.ManyToManyField(Cost, blank=True, through='CostShip')
    date_joined   = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
