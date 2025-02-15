
from django.urls import path
from owner import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
     path('', views.index, name='ownerhome'),
    path('view_order/', views.view_order, name='view_order'),
    path('product_list/', views.product_list, name='product_list'),
    path('purchase_order/', views.purchase_order, name='purchase_order'),
    path('new/', views.product_create, name='product_create'),
    path('<int:product_id>/edit/', views.product_update, name='product_update'),
    path('<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/update/<int:supplier_id>/', views.update_supplier, name='update_supplier'),
    path('suppliers/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('delivery-persons/', views.delivery_person_list, name='delivery_person_list'),
    path('delivery-persons/add/', views.add_delivery_person, name='add_delivery_person'),
    path('delivery-persons/edit/<int:delivery_id>/', views.update_delivery_person, name='update_delivery_person'),
    path('delivery-persons/delete/<int:delivery_id>/', views.delete_delivery_person, name='delete_delivery_person'),
    path('batches/', views.list_batches, name='list_batches'),
    path('batches/add/', views.create_batch, name='create_batch'),
    path('batches/update/<int:batch_id>/', views.update_batch, name='update_batch'),
    path('batches/delete/<int:batch_id>/', views.delete_batch, name='delete_batch'),
    path('manage-profile/', views.manage_profile, name='manage_profile'),
    path('register_view/', views.register_view, name='register1'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout, name='logout'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('forgot/', views.forgot_pass, name='forgot_pass'),
    path('reset_password/<str:reset_token>/', views.reset_password, name='reset_password'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)