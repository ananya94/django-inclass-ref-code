from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from .models import Product

from .forms import ProductAddForm

def create_view(request):
    print(request.POST)
    form = ProductAddForm(request.POST or None)

    ### Reference Code ####
    # if request.method == "POST":
    #     print(request.POST)
    if form.is_valid():
        # Getting validated data from our POST
        data = form.cleaned_data
        title = data.get("title")
        description = data.get("description")
        price = data.get("price")

        # Saving the data to our object inside of our PostGreSQL database
        # This can be done in two ways actually
        """ The first way"""
        #new_object = Product.objects.create(title=title,description=description,price=price)

        """ OR We could do it this way """
        new_object = Product()
        new_object.title = title
        new_object.description = description
        new_object.price = price
        new_object.save()
# Both of the above solutions work roughly the same way^^
        #print(request.POST)
    template = "create_view.html"
    context = {
        "form":form
    }
    return render(request,template,context)


def detail_slug_view(request,slug=None):
    print(request)
    try:
        product = get_object_or_404(Product,slug=slug)
    except:
        product = Product.objects.filter(slug=slug).order_by("title").first() # This will gain access to our slug and order by our title
    print(slug)
    template = "detail_view.html"
    context = {
        "object": product
    }
    return render(request, template, context)

def detail_view(request,object_id=None):
    print(request)
    products = Product.objects.get(id = object_id)
    template = "detail_view.html"
    context = {
        "object": products
    }
    return render(request,template,context)

def list_view(request):
    print(request)
    products = Product.objects.all()
    template = "list_view.html"
    context = {
        "object": products
    }
    return render(request,template,context)
