from django.urls import path
from . consumers import *
from . views import *

urlpatterns = [
    path('map/', RouteMap.as_view(), name='home'),
]
