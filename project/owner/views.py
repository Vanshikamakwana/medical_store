from django.shortcuts import render
from owner.models import Sales,user
# Create your views here.
def index(request):
    orders = Sales.objects.all()
    users=user.objects.all()
    return render(request,'owner/template/index.html', {'orders': orders},{'users':users})
          
def view_order(request):
    orders = Sales.objects.all()
    users=user.objects.all()
    return render(request, 'view_order.html', {'orders': orders},{'users':users})



           


         
