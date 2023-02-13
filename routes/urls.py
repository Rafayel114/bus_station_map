from django.urls import path
from django.conf.urls.static import static

from bus_station import settings
from . consumers import *
from . views import *


urlpatterns = [
    path('map/', RouteMap.as_view(), name='home'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
