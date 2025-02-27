# delivery/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from owner.models import User  # Custom User Model

class DeliveryLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    def clean(self):
        Email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if Email and password:
            user = authenticate(username=Email, password=password)
            if not user or not hasattr(user, 'role_id') or user.role_id.role_type != 'Delivery':
                raise forms.ValidationError("Invalid email or not authorized for delivery login")
        return self.cleaned_data
