from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from .models import Product

from .forms import ProductAddForm,ProductUpdateForm

######## CLASS BASED VIEWS START #########

# Classbased View Imports
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# TODO Create Mixin for SlugView for ClassBased Views

# Mixin import
from django_digital.mixins import ProductSlugMixin


class ProductDetailView(ProductSlugMixin,DetailView):
    model = Product

    def get_context_data(self,**kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        print(context)
        return context

class ProductListView(ListView):
    model = Product
    context_object_name = "someother_list"  # This will specify a specific name for the "object_list" if desired.
    def get_queryset(self,*args,**kwargs):
        queryset = super(ProductListView,self).get_queryset(**kwargs)
        return queryset
######## CLASS BASED VIEWS END ##########

def slug_update_view(request,slug=None):
    try:
        product = get_object_or_404(Product,slug = slug)
    except:
        product = Product.objects.filter(slug=slug).orderby("title").first()
    form = ProductUpdateForm(request.POST or None, instance=product)
    template = "update_view.html"
    context = {
        "form":form,
        "object":product
    }
    return render(request,template,context)

def update_view(request,object_id=None):
    print(request)
    product = get_object_or_404(Product,id = object_id)
    form = ProductUpdateForm(request.POST or None,instance=product)
    if form.is_valid():
        print(form.cleaned_data.get("publish"))
        instance = form.save(commit=False)
        print(instance)
        instance.save()
    template = "update_view.html"
    context = {
        "object":product,
        "form":form,
    }
    return render(request,template,context)

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
