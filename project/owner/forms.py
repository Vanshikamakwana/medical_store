# forms.py
from django import forms
from owner.models import purchase,Product,suppliers

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = suppliers
        fields = ['suppliers_name', 'suppliers_contact', 'comp_id']