from django.shortcuts import render

# Create your views here.
from .models import Product
def detail_view(request):
    print(request)
    products = Product.objects.all()
    template = "detail_view.html"
    context = {
        "object": products
    }
    return render(request,template,context)
