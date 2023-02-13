from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
import json

from . models import Route, Station
from . serializers import RouteSerializer


@database_sync_to_async
def get_route_objects():
    try:
        routes = Route.objects.filter(is_active=True)
        print("--------------------")
        serialized = RouteSerializer(routes, many=True).data
        return serialized
    except:
        return None


class RouteConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print(self.scope)
        await self.channel_layer.group_add(
            'routes',
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            "text": "connection established",
            "message": "You are now connected to routes websocket"
        }))
        await self.routeList()

    async def routeList(self):
        routes = await get_route_objects()
        print(json.dumps({'routes': routes}))
        await self.send(text_data=json.dumps({'routes': routes}))

    async def send_new_data(self, event):
        message = event['text']
        await self.routeList()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('routes', self.channel_name)
