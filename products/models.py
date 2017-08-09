from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.utils.text import slugify

class Product(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    slug = models.SlugField(blank=True)
    price = models.DecimalField(max_digits = 15, decimal_places = 2, default=9.99)
    sale_price = models.DecimalField(max_digits = 15, decimal_places = 2, blank=True, null=True)

    def __str__(self):
        return self.title

def product_pre_save_reciever(sender,instance,*args,**kwargs): #Param_list: sender = Product, instance = Newly Created Product(eg AirJordan 3)
    print(sender)
    print(instance)

    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(product_pre_save_reciever,sender=Product)
