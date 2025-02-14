from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmailLoginForm, RegisterForm
from django.contrib.auth.models import User
from account.utils import email_authenticate
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')  # Redirect after login
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def email_login(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = email_authenticate(email, password)  # Custom email authentication
            if user:
                login(request, user)  # Login the user
                return redirect('home')  # Redirect to home page
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password'})
    else:
        form = EmailLoginForm()
    
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

