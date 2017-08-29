from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormMixin

from products.models import Variation
from .models import Cart, CartItem
from orders.models import UserCheckout, Order, UserAddress
from orders.forms import GuestCheckoutForm

from orders.mixins import CartOrdermixin

#BRAINTREE PAYMENT SETUP
from django.conf import settings
from django.contrib import messages
import braintree

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    '34hkzh8p357qypjk',
    'r6k25wjjgrs85k5k',
    '3e8a367a637ec65a728e2c17e582e6bb'
)

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id = settings.BRAINTREE_MERCHANT_ID,
                                  public_key = settings.BRAINTREE_PUBLIC,
                                  private_key = settings.BRAINTREE_PRIVATE)

# Create your views here.
class CartView(SingleObjectMixin,View):
    model = Cart
    template_name = "carts/view.html"


    def get_object(self,*args,**kwargs):
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get("cart_id")
        if cart_id is None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id = cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self,request,*args,**kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete",False)
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Variation,id = item_id)
            qty = request.GET.get("qty",1) #Giving the quantity a default value of 1
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            cart_item,created_item = CartItem.objects.get_or_create(cart=cart, item = item_instance)
            if created_item:
                item_added = True
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))
        if request.is_ajax():
            print(request.GET.get("item"))
            try:
                subtotal = cart_item.cart_subtotal
            except:
                subtotal = None
            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal": subtotal,
                "cart_total": cart_total,
                "tax_total": tax_total,
                "total_items": total_items,
            }
            return JsonResponse(data)  # Return a JSON Response.
            #return JsonResponse({"deleted":delete_item,"created":item_added}) # Return a JSON Response.
        context = {
            "object":self.get_object()
        }
        print(context)
        template = self.template_name
        return render(request,template,context)


class CheckoutView(CartOrdermixin,FormMixin,DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"
    form_class = GuestCheckoutForm

    # def get_order(self, *args, **kwargs):
    #     cart = self.get_object()
    #     new_order_id = self.request.session.get("order_id")
    #     if new_order_id is None:
    #         new_order = Order.objects.create(cart=cart)
    #         self.request.session["order_id"] = new_order.id
    #     else:
    #         new_order = Order.objects.get(id=new_order_id)
    #     return new_order

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart == None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get("user_checkout_id")
        # or if request.user.is_guest:
        if not self.request.user.is_authenticated() or user_check_id == None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        elif self.request.user.is_authenticated() or user_check_id != None:
            user_can_continue = True
            # return redirect "address select view"
        else:
            pass
        if self.request.user.is_authenticated():
            user_checkout, created = UserCheckout.objects.get_or_create(
                email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.save()
            context["client_token"] = user_checkout.get_client_token()
            self.request.session["user_checkout_id"] = user_checkout.id

        elif not self.request.user.is_authenticated() and user_check_id == None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        else:
            pass
        if user_check_id != None:
            user_can_continue = True
            if not self.request.user.is_authenticated(): #GUEST USER - Making sure an authenticated token and a guest user token don't come at the same time
                 user_checkout_2 = UserCheckout.objects.get(id=user_check_id)
                 context["client_token"] = user_checkout_2.get_client_token()
        # This will allow use to show the order in the html.
        context["order"] = self.get_order()
        context["user_can_continue"] = user_can_continue
        context["form"] = self.get_form()
        print(context, "---User Checkout ID ---", user_check_id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_checkout, created = UserCheckout.objects.get_or_create(
                email=email)
            request.session["user_checkout_id"] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")

    def get(self, request, *args, **kwargs):
        print(request.GET)
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart == None:
            return redirect("cart")
        new_order = self.get_order()
        user_checkout_id = request.session.get("user_checkout_id")
        if user_checkout_id != None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if new_order.billing_address == None or new_order.shipping_address == None:
                return redirect("address_form")
            new_order.user = user_checkout
            new_order.save()
        return get_data


class CheckoutFinalView(CartOrdermixin,View):
    def post(self,request,*args,**kwargs):
        print(request.POST)
        order = self.get_order() # Getting the order
        order_total = order.order_total # Getting the order total
        nonce = request.POST.get('payment_method_nonce') # Getting payment nonce from braintree
        if nonce:
            result = braintree.Transaction.sale({
                "amount": order_total,
                "payment_method_nonce": nonce,
                "billing": {
                    "postal_code": "%s" %(order.billing_address.zipcode),
                  },
                "options": {
                    "submit_for_settlement": True
                }
            })
            if result.is_success:
                print(result.transaction.id)
                order.mark_completed(order_id = result.transaction.id)
                messages.success(request,"Thank you for your purchase")
                del request.session["cart_id"]
                del request.session["order_id"]
            else:
                messages.error(request,"%s" %(result.message))
                return redirect("checkout")
        return redirect("order_detail",pk=order.pk)

    def get(self,request,*args,**kwargs):
        """This GET call will redirect us back to the checkout URL
        otherwise we would raise a 405 Forbidden Error"""
        return redirect("checkout")
