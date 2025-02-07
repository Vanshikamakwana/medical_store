
from django.urls import path
from owner import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("owner/",views.index,name="ownerhome"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)