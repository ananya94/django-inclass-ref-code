from django.contrib import admin

# Register your models here.
from .models import Product, Variation

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__','description','price','sale_price']
    search_fields = ["description","title","bob"]
    list_filter = ["price"]
    list_editable = ["sale_price"]

    class Meta:
        model = Product

class VariationAdmin(admin.ModelAdmin):
    list_display = ["__str__","product"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)
