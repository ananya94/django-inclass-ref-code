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
    publish = forms.ChoiceField(label="Publish-Product",widget=forms.RadioSelect,
        choices = PUBLISH_CHOICES,required = False )

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 1.00:
            raise forms.ValidationError("Your Price Must Be Greater than a $1.00")
        elif price > 1000.00:
            raise forms.ValidationError("Your Price Must NOT be Greater than $1,000.00")
        else:
            return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Your Title Must Be at least 3 Characters Long!")

class ProductUpdateForm(forms.ModelForm):
    title=forms.CharField(label="Product-Title",widget=forms.TextInput())
    description = forms.CharField(label="Product-Description",widget=forms.Textarea())
    price = forms.DecimalField(label="Product-Price")
    publish = forms.ChoiceField(label="Publish-Product",widget=forms.RadioSelect,
        choices = PUBLISH_CHOICES,required = False )
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
        ]


    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 1.00:
            raise forms.ValidationError("Your Price Must Be Greater than a $1.00")
        elif price > 1000.00:
            raise forms.ValidationError("Your Price Must NOT be Greater than $1,000.00")
        else:
            return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Your Title Must Be at least 3 Characters Long!")
