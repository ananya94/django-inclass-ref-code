from django import forms
from .models import Product

PUBLISH_CHOICES = (
    ("publish","Publish"),
    ("draft","Draft"),
)

class ProductAddForm(forms.Form):
    title=forms.CharField(label="Product-Title",widget=forms.TextInput())
    description = forms.CharField(label="Product-Description",widget=forms.Textarea())
    price = forms.DecimalField(label="Product-Price")
    publish = forms.ChoiceField(label="Publish-Product",widget=forms.RadioSelect,choices = PUBLISH_CHOICES,required = False )
