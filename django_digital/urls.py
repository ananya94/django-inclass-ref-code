"""django_digital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from products import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create/$',views.create_view,name ="create_view"),
    url(r'^update/(?P<object_id>\d+)$',views.update_view,name ="update_view"),
    #### Class Based Views URLS  Start###
    url(r'^products/$',views.ProductListView.as_view(), name = "products_list_view"),
    url(r'^products/detail/(?P<pk>\d+)/$',views.ProductDetailView.as_view(),name="products_detail_view"),
    url(r'^products/detail/(?P<slug>[\w-]+)/$',views.ProductDetailView.as_view(),name="products_slug_view"),
    ##### Class Based Views URLS End ####
    url(r'^update/(?P<slug>[\w-]+)$',views.slug_update_view,name ="slug_update_view"),
    url(r'^detail/(?P<object_id>\d+)$',views.detail_view,name ="detail_view"),
    url(r'^detail/(?P<slug>[\w-]+)$',views.detail_slug_view,name ="detail_slug_view"),
    url(r'^list/$',views.list_view,name="list_view"),
]
