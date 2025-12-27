from django.db import models
from User.models import User
from core.Functions import get_filename_ext
from django.core.exceptions import ValidationError

# ==============================================

# ==============================================
def upload_image_path_tag(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.title_seo}{ext}"
    return f"Product/Tag/{final_name}"


def upload_image_path_category(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}{ext}"
    return f"Product/category/{final_name}"


def upload_image_path_product(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.slug}{ext}"
    return f"Product/product/{final_name}"


def upload_image_path_packaging(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}{ext}"
    return f"Product/packaging/{final_name}"





def upload_image_path_product_gif(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance._id}{ext}"
    return f"Product/product/gif/{final_name}"



def upload_image_path_gallery(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}{ext}"
    return f"Product/Gallery/{final_name}"





def upload_image_path_brand(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.title_seo}{ext}"
    return f"Product/Brand/{final_name}"


# ==============================================

gender_CHOICES = (
    ("adult", "مردانه"),
    ("teen", "زنانه"),
    ("child", "بچگانه"),
)


class Brand(models.Model):
    slug = models.CharField(max_length=1000, unique=True)
    name = models.CharField(max_length=1000, unique=True)
    title_seo = models.CharField(max_length=55)
    description_seo = models.TextField(max_length=139)
    image = models.ImageField(null=True, blank=True, upload_to=upload_image_path_brand)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug.replace(' ', '-').lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند'


class Tag(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    slug = models.CharField(max_length=1000, unique=True)
    title_seo = models.CharField(max_length=55)
    description_seo = models.TextField(max_length=139)
    image = models.ImageField(null=True, blank=True, upload_to=upload_image_path_tag)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug.replace(' ', '-').lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب'


class MainCategories(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    slug = models.CharField(max_length=1000, unique=True)
    title_seo = models.CharField(max_length=55)
    description_seo = models.TextField(max_length=139, default='')
    description     = models.TextField(default='', blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_image_path_category)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug.replace(' ', '-').lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'دسته بندی اصلی '
        verbose_name_plural = 'دسته بندی اصلی '

class Subcategories(models.Model):
    name = models.CharField(max_length=200)
    main = models.ForeignKey(
        MainCategories,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='انتخاب دسته بندی اصلی'
    )
    slug = models.CharField(max_length=1000, unique=True)
    title_seo = models.CharField(max_length=55)
    description_seo = models.TextField(max_length=139, default='')
    image = models.ImageField(null=True, blank=True, upload_to=upload_image_path_category)
    description     = models.TextField(default='', blank=True, null=True)
    age_rank = models.CharField(max_length=9,
                              choices=gender_CHOICES,
                              default="adult",
                              null=True,
                              blank=True
                              )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug.replace(' ', '-').lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'دسته بندی فرعی'
        verbose_name_plural = 'دسته بندی فرعی'




class Properties(models.Model):
    name            = models.CharField(max_length=150, default='name')
    fittings        = models.IntegerField(null=True, blank=True)
    fabric_material = models.IntegerField(null=True, blank=True)
    base_price      = models.DecimalField(default=1.0, max_digits=4, decimal_places=2)
    length          = models.DecimalField(default=1.0, max_digits=4, decimal_places=2)
    width           = models.DecimalField(default=1.0, max_digits=4, decimal_places=2)
    height          = models.DecimalField(default=1.0, max_digits=4, decimal_places=2)
    send_salary     = models.DecimalField(default=1.0, max_digits=4, decimal_places=2)
    frame_price     = models.DecimalField(default=1.0, max_digits=4, decimal_places=2)
    normal_discount = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    installment = models.BooleanField(default=False)
    installment_discount = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    installment_period_month = models.IntegerField(default=0, null=True, blank=True)
    pre_cost = models.DecimalField(max_digits=15, decimal_places=0)
    def __str__(self):
        return f"{self.name} - {self.id}"
    class Meta:
        verbose_name = 'ویژگی ها'
        verbose_name_plural = 'ویژگی ها'





class Gallery(models.Model):
    image     = models.ImageField(upload_to=upload_image_path_gallery)
    property  = models.ManyToManyField(Properties, blank=True)
    name      = models.CharField(max_length=180, default='')
    slug = models.CharField(max_length=1000, default='', unique=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug.replace(' ', '-').lower()
        super().save(*args, **kwargs)


class Attributes(models.Model):
    name    = models.CharField(max_length=150)
    comment = models.CharField(max_length=150)
    def __str__(self):
        return self.name



class EventType(models.Model):
    name  = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Packaging(models.Model):
    name  = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_image_path_packaging)
    def __str__(self):
        return self.name


class Product(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path_product, default='')
    packaging = models.ManyToManyField(Packaging, blank=True)
    main_category = models.ForeignKey(
        MainCategories, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دسته بندی اصلی'
    )
    sub_category = models.ForeignKey(Subcategories, default='', on_delete=models.CASCADE, verbose_name='دسته بندی فرعی')
    tag = models.ManyToManyField(Tag, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    attributes  = models.ManyToManyField(Attributes, blank=True)
    properties = models.ManyToManyField(Properties, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    create_at = models.DateField(auto_now_add=True)
    suggested = models.BooleanField(default=False)
    new = models.BooleanField(default=True)
    slug = models.CharField(max_length=1000, unique=True)
    title_seo = models.CharField(max_length=55)
    description_seo = models.TextField(max_length=139)
    gallery = models.ManyToManyField(Gallery, blank=True)
    available = models.BooleanField()
    date_available = models.IntegerField(default=3)
    gender = models.CharField(max_length=9,
                              choices=gender_CHOICES,
                              default="man",
                              null=True,
                              blank=True
                              )
    price = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    count_in_stock = models.BooleanField(default=False)
    delete_status  = models.BooleanField(default=False)
    draft          = models.BooleanField(default=True)
    even_type      = models.ManyToManyField(EventType, blank=True)
    gif            = models.FileField(upload_to=upload_image_path_product_gif, null=True, blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug.replace(' ', '-').lower()
        self.main_category = self.sub_category.main


        super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        if self.suggested and self.new:
            raise ValidationError({
                "suggested": ["انتخاب همزمان 'new' و 'suggested' مجاز نیست."],
                "new": ["انتخاب همزمان 'new' و 'suggested' مجاز نیست."],
            })
        return self


    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)

    class Meta:
        verbose_name = 'کامنت ها'
        verbose_name_plural = 'کامنت ها'



