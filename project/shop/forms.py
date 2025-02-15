from django import forms
from django.contrib.auth.models import User
from owner.models import CustomUser

class RegisterForm(forms.ModelForm):
            # password = forms.CharField(widget=forms.PasswordInput)
            # confirm_password = forms.CharField(widget=forms.PasswordInput)

            # class Meta:
            #     model = User
            #     fields = ['username', 'email', 'password']

            # def clean(self):
            #     cleaned_data = super().clean()
            #     password = cleaned_data.get("password")
            #     confirm_password = cleaned_data.get("confirm_password")

            #     if password and confirm_password and password != confirm_password:
            #         raise forms.ValidationError("Passwords do not match!")
            #     return cleaned_data
        password = forms.CharField(widget=forms.PasswordInput)
    
        class Meta:
            model = CustomUser
            fields = ['Fname', 'Lname', 'Gender', 'Address', 'Mob_no', 'Email', 'password', 'Area_id', 'shop_id']
            # , 'role_id'
            widgets = {
            'password': forms.PasswordInput(),
            }
            labels = {
                'Area_id': 'Select Area',  # Custom label for Area selection
                'shop_id': 'Select Shop',  # Custom label for Shop selection
            }