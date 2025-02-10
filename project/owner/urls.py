
from django.urls import path
from owner import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("owner/",views.index,name="ownerhome"),
    path("view_order/",views.view_order,name="view_order"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)