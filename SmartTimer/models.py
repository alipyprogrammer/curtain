from django.db import models

# Create your models here.


class Seo(models.Model):
    _id_seo          =  models.AutoField(primary_key=True ,editable=False)
    title_seo       = models.CharField(max_length=55)
    description_seo = models.TextField(max_length=139)
    slug            = models.SlugField(max_length=500,unique=True,allow_unicode=True,default='',verbose_name='نامک')

