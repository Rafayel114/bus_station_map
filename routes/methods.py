from . serializers import *
from . models import *

def route_to_dict(route_id):
    route = Route.objects.get(pk=route_id)
    serialized = RouteSerializer(route)
    return serialized
