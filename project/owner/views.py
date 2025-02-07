from django.shortcuts import render

# Create your views here.
def index(request):
    data = {
        'sales': [12, 19, 3, 5],
        'months': ['Jan', 'Feb', 'Mar', 'Apr']
    }
    
    return render(request,'owner/template/index.html', {'data': data})
          
         
