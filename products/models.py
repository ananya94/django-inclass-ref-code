from django.db import models


# Create your models here.
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify

###### Checking to find out if a product is active (not discontinued) or not ######
from django.core.urlresolvers import reverse

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self,*args,**kwargs):
        return self.get_queryset().active()

class Product(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    slug = models.SlugField(blank=True)
    price = models.DecimalField(max_digits = 15, decimal_places = 2, default=9.99)
    sale_price = models.DecimalField(max_digits = 15, decimal_places = 2, blank=True, null=True)
    active = models.BooleanField(default = True)
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products_slug_view",kwargs = {"slug":self.slug})

def product_pre_save_reciever(sender,instance,*args,**kwargs): #Param_list: sender = Product, instance = Newly Created Product(eg AirJordan 3)
    print(sender)
    print(instance)

    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(product_pre_save_reciever,sender=Product)

class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits = 15, decimal_places = 2)
    sale_price = models.DecimalField(max_digits = 15, decimal_places =2,blank=True,null=True)
    active = models.BooleanField(default = True)
    inventory = models.IntegerField(null = True, blank = True)

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

def product_variation_post_save_receiver(sender,instance,created,*args,**kwargs):
    print(sender)
    print(instance)

    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_variation = Variation()
        new_variation.product = product
        new_variation.title = "Default"
        new_variation.price = product.price
        new_variation.save()

    print(created)

post_save.connect(product_variation_post_save_receiver,sender=Product)
