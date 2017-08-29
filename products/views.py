from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
# Create your views here.

from django_digital.mixins import ProductSlugMixin

from .forms import ProductAddForm,ProductUpdateForm
from .models import Product

class ProductCreateView(CreateView):
    model = Product
    template_name = "form.html"
    form_class = ProductAddForm
    success_url = "/products/add/"

    def get_context_data(self,*args,**kwargs):
        context = super(ProductCreateView,self).get_context_data(*args,**kwargs)
        context["submit_btn"] = "Add Product"
        return context

class ProductUpdateView(ProductSlugMixin,UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductAddForm
    success_url = "/products/list/"

    def get_context_data(self,*args,**kwargs):
        context = super(ProductUpdateView,self).get_context_data(*args,**kwargs)
        context["submit_btn"] = "Add Product"
        return context
#Creating a ListView using the Class Based Version of the views
class ProductDetailView(ProductSlugMixin,DetailView):
    model = Product

    def get_context_data(self,**kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        print(context)
        return context

#Creating a ListView using the Class Based Version of the views
class ProductListView(ListView):
    model = Product

    def get_queryset(self,*args,**kwargs):
        qs = super(ProductListView,self).get_queryset(**kwargs) #The super keyword is referring to the parent class - which in the case is ProductListView()
        return qs

def create_view(request):
    print(request.POST)
    form = ProductAddForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data.get("publish"))
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "form":form
    }
    return render(request,template,context)

def update_view(request,object_id=None):
    print(request)
    product = get_object_or_404(Product,id=object_id)
    form = ProductAddForm(request.POST or None, instance=product)
    if form.is_valid():
        print(form.cleaned_data.get("publish"))
        instance = form.save(commit=False)
        #instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "object": product,
        "form":form
    }
    return render(request, template, context)

def detail_slug_view(request,slug=None):
    print(request)
    try:
        product = get_object_or_404(Product,slug=slug)
    except:
        product = Product.objects.filter(slug=slug).order_by("title").first() # This will gain access to our slug and order by our title
    print(slug)
    template = "products/product_detail.html"
    context = {
        "object": product
    }
    return render(request, template, context)
# Getting one item
def detail_view(request,object_id=None):
    print(request)
    product = get_object_or_404(Product,id=object_id)
    template = "detail_view.html"
    context = {
        "object": product
    }
    return render(request, template, context)

####### Reference Code ###################

    # if object_id is not None:
    #     try:
    #         product = Product.objects.get(id=object_id)
    #     except Product.DoesNotExist:
    #         product = None
    #     template = "detail_view.html"
    #     context = {
    #         "object": product
    #     }
    # else:
    #     raise Http404
    # return render(request, template, context)


def list_view(request):
    # Getting a list of items
    print(request)
    queryset = Product.objects.all()
    template = "list_view.html"
    context = {
        "queryset": queryset
    }
    return render(request, template, context)
