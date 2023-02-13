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
        print(routes)
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
        # await self.send_new_data()

    async def routeList(self):
        routes = await get_route_objects()
        print(json.dumps({'routes': routes}))
        await self.send(text_data=json.dumps({'routes': routes}))

    async def send_new_data(self, event):
        message = event['text']
        await self.routeList()
        ## serialized = await SimpleAuctionSerializer(message)
        ## Send message to WebSocket
        ## await self.send(text_data=json.dumps({
        ##     'message': message
        ## }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard('routes', self.channel_name)



# class SingleAuctionConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#         print(self.scope)
#         self.auction_id = self.scope['url_route']['kwargs'].get('auction_id', None)
#         self.room_name = 'auction' + str(self.auction_id)
#         await self.channel_layer.group_add(
#             self.room_name,
#             self.channel_name
#         )
#         await self.accept()
#         await self.send(text_data=json.dumps({
#             "text": "connection established",
#             "message": "You are now connected to single auction websocket"
#         }))
#         await self.singleAuction()
#         ## await self.send_new_data()
#
#     async def singleAuction(self):
#         auction = await get_auction_object(self.auction_id)
#         # print(json.dumps({'auction': auction}))
#         await self.send(text_data=json.dumps({'auction': auction}))
#
#     async def send_new_data(self, event):
#         message = event['text']
#         await self.singleAuction()
#         ## serialized = await SimpleAuctionSerializer(message)
#         ## Send message to WebSocket
#         ## await self.send(text_data=json.dumps({
#         ##     'message': message
#         ## }))
#
#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.room_name, self.channel_name)
