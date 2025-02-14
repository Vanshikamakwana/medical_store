from django import views
from django.urls import path
from account.views import register, email_login, user_logout

urlpatterns = [
    
    path('', register, name='register'),
    path('login/',  email_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
