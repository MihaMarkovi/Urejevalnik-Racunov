from django import forms
from .models import Company, Bill


class BillDetailsForm(forms.Form):
    eor = forms.CharField(label="EOR", max_length=100,
                          widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background-color: darkgray'}))
    producer = forms.ModelChoiceField(label="Proizvajalec", queryset=Company.objects.all())
    bill_number = forms.CharField(label='Številka Računa', max_length=200)
    seller = forms.CharField(label='Prodajalec', max_length=200)
    tax_level = forms.FloatField(label='Davčna Stopnja')
    zoi = forms.CharField(label='ZOI', max_length=200)
    status = forms.BooleanField(label='Potrjeno', required=False)


class ProductDetailsForm(forms.Form):
    product_title = forms.CharField(label="Ime Produkta", max_length=200)
    quantity = forms.IntegerField(label="Količina")
    value = forms.FloatField(label="Cena (€)")


class CompanyDetailsForm(forms.Form):
    title = forms.CharField(label="Ime Podjetja", max_length=200)
    address = forms.CharField(label="Naslov", max_length=200)
    post_office = forms.CharField(label="Pošta", max_length=200)
    ddv_id = forms.CharField(label="ID za DDV", max_length=200)
