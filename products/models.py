from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    price = models.DecimalField(max_digits = 15, decimal_places = 2, default=9.99)
    sale_price = models.DecimalField(max_digits = 15, decimal_places = 2, blank=True, null=True)

    def __str__(self):
        return self.title
