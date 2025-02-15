# forms.py
from django import forms
from owner.models import purchase,Product,suppliers
from owner.models import CustomUser
from django.contrib.auth.hashers import make_password, check_password

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = suppliers
        fields = ['suppliers_name', 'suppliers_contact', 'comp_id']

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['Fname', 'Lname', 'Gender', 'Address', 'Mob_no', 'Email', 'password', 'Area_id', 'shop_id', 'role_id']

    def save(self, commit=True):
        user_instance = super().save(commit=False)
        user_instance.password = make_password(self.cleaned_data['password'])  # ✅ Password hashing
        if commit:
            user_instance.save()
        return user_instance

class LoginForm(forms.Form):
    Email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
