from tabnanny import verbose
from django.db import models
from User.models import User
from core.Functions import get_filename_ext
from Img.models import Img
from SmartTimer.models import Seo

# ==============================================
# ==============================================
def upload_image_path_Category(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.Alt}{ext}"
    return f"Blog/category/{final_name}"



class MainCategories(Img, Seo):
    name         = models.CharField(max_length=50,default='',verbose_name='عنوان')
    descriptions = models.TextField(max_length=3000 , null=True, blank=True)

    def __str__(self):
        return self.Title
    class Meta:
        verbose_name='دسته بندی اصلی'
        verbose_name_plural='دسته بندی اصلی'



class Subcategories(Img, Seo):
    name         = models.CharField(max_length=50,default='',verbose_name='عنوان')
    descriptions = models.TextField(max_length=3000 , null=True, blank=True)

    def __str__(self):
        return self.Title
    class Meta:
        verbose_name='دسته بندی اصلی'
        verbose_name_plural='دسته بندی اصلی'

class Tag(Img, Seo):
    name = models.SlugField(max_length=1000,default='',verbose_name='نامک')

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name='برچسب'
        verbose_name_plural='برچسب'


class Blog(Img, Seo):
    user         =  models.ForeignKey(User,on_delete=models.SET_NULL ,null=True)
    name         =  models.CharField(max_length=200,null=True ,blank=True)
    main_category = models.ForeignKey(
        MainCategories, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دسته بندی اصلی'
    )
    sub_category = models.ForeignKey(Subcategories, default='', on_delete=models.CASCADE, verbose_name='دسته بندی فرعی')
    tag          =  models.ManyToManyField(Tag,blank=True )
    description  =  models.TextField(null=True,blank=True)
    summary      =  models.CharField(default='' ,max_length=150 ,verbose_name='توضیح مختصر')
    _id          =  models.AutoField(primary_key=True ,editable=False)
    def __str__(self):
        return self.name
    class  Meta:
        db_table = ''
        managed = True
        verbose_name = 'وبلاگ'
        verbose_name_plural = 'وبلاگ ها'

