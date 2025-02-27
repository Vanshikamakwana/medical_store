
from django.urls import path
from . import views
from django.conf import settings
app_name = 'delivery'

urlpatterns = [
    path('', views.index, name='deliveryhome'),
    # path('delivery_login/', views.delivery_login, name='delivery_login'),  # ✅ Delivery Person Login Page
    # path('logout/', views.delivery_logout, name='delivery_logout'),  # ✅ Delivery Logout
    
    path('view_sales/', views.view_sales, name='delivery_view_sales'),
    path('sales_history/', views.sales_history, name='delivery_sales_history'),
    path('update_sale_status/<int:sale_id>/', views.update_sale_status, name='update_sale_status'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

