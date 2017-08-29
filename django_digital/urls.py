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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from products import views
from carts.views import CartView, CheckoutView, CheckoutFinalView
from orders.views import AddressSelectFormView, UserAddressCreateView, OrderList,OrderDetail

from products.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create/$', views.create_view, name="create_view"),
    url(r'^detail/(?P<object_id>\d+)/$', views.detail_view, name="detail_view"),
    url(r'^detail/(?P<object_id>\d+)/edit/$',
        views.update_view, name="update_view"),
    url(r'^detail/(?P<slug>[\w-]+)/$',
        views.detail_slug_view, name="detail_slug_view"),
    url(r'^list/$', views.list_view, name="list_view"),
    url(r'^products/', ProductListView.as_view(), name="product_list_view"),
    url(r'^products/add/$', ProductCreateView.as_view(), name="product_create_view"),
    url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view(),
        name="product_detail_view"),
    url(r'^products/(?P<slug>[\w-]+)/$',
        ProductDetailView.as_view(), name="product_detail_view"),
    url(r'^products/(?P<pk>\d+)/edit/$',
        ProductUpdateView.as_view(), name="product_update_view"),
    url(r'^products/(?P<slug>[\w-]+)/edit/$',
        ProductUpdateView.as_view(), name="product_update_view"),
    url(r'^accounts/', include('allauth.urls')),
    # Cart View
    url(r'^orders/$',OrderList.as_view(), name = "orders"),
    url(r'^orders/(?P<pk>\d+)/$',OrderDetail.as_view(), name = "order_detail"),
    url(r'^cart/$', CartView.as_view(), name="cart"),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),

    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name="address_form"),
    url(r'^checkout/address/add$', UserAddressCreateView.as_view(),
        name="user_address_create"),
    url(r'^checkout/final/$',CheckoutFinalView.as_view(),name="checkout_final"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
