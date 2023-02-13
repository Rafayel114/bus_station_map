from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.forms.models import model_to_dict
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# from . methods import route_to_dict


channel_layer = get_channel_layer()


class Station(models.Model):
    title = models.CharField(max_length=512, null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True)
    lat = models.DecimalField(max_digits=18, decimal_places=15)
    lon = models.DecimalField(max_digits=18, decimal_places=15)
    point = gis_models.PointField(null=True, blank=True)

    def save(self, *args, **kwargs):    # переопределили сейв чтобы сохранить поинт
        is_new = True if not self.id else False
        if is_new:
            super(Station, self).save(*args, **kwargs)
        else:
            print(self.lon)
            self.point = Point((self.lon, self.lat),)
            instance = Station.objects.get(pk=self.id)
            old_lat = instance.lat
            old_lon = instance.lon
            super(Station, self).save(*args, **kwargs)
            instance.refresh_from_db()
            if instance.lat != old_lat or instance.lon != old_lon:
                try:
                    route_dict = model_to_dict(self.current_stop.last().route)
                    async_to_sync(channel_layer.group_send)('routes', {'type': 'send_new_data', 'text': json.dumps(route_dict, indent=4, sort_keys=True, default=str)})
                except:
                    pass



    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = "Остановка"
        verbose_name_plural = "Остановки"


class Route(models.Model):
    title = models.CharField(max_length=512, null=True, blank=True)
    number = models.CharField(max_length=512, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{}, № {} ".format(self.title, self.number)

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def save(self, *args, **kwargs):       # TODO
        is_new = True if not self.id else False
        if is_new:
            super(Route, self).save(*args, **kwargs)
            print("new save")
        else:
            instance = Route.objects.get(id=self.id)
            print(instance.current_stop.all())
            super(Route, self).save(*args, **kwargs)
            route_dict = model_to_dict(instance)
            async_to_sync(channel_layer.group_send)('routes', {'type': 'send_new_data', 'text': json.dumps(route_dict, indent=4, sort_keys=True, default=str)})


class CurrentStop(models.Model):
    route = models.ForeignKey(Route, related_name="current_stop", on_delete=models.CASCADE)
    station = models.ForeignKey(Station, related_name="current_stop", on_delete=models.CASCADE)
    index = models.IntegerField()   #индекс сортировки
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "Остановка: {}, маршрут: {} ".format(self.station.title, self.route.title)

    def save(self, *args, **kwargs):       # TODO
        is_new = True if not self.id else False
        if is_new:
            super(CurrentStop, self).save(*args, **kwargs)
            print("new current_stop save")
            pass
        else:
            instance = CurrentStop.objects.get(id=self.id)
            old_instance_route = instance.route.id
            old_station_id = instance.station.id
            old_station_lon = instance.station.lon
            old_station_lat = instance.station.lat
            super(CurrentStop, self).save(*args, **kwargs)
            instance.refresh_from_db()
            # chinstance = CurrentStop.objects.get(id=self.id)
            route = Route.objects.get(pk=instance.route.id)
            route_dict = model_to_dict(route)
            if instance.route.id != old_instance_route:
                async_to_sync(channel_layer.group_send)('routes', {'type': 'send_new_data', 'text': json.dumps(route_dict, indent=4, sort_keys=True, default=str)})
            if instance.station.id != old_station_id:
                async_to_sync(channel_layer.group_send)('routes', {'type': 'send_new_data', 'text': json.dumps(route_dict, indent=4, sort_keys=True, default=str)})

    class Meta:
        verbose_name = "Остановка маршрута"
        verbose_name_plural = "Остановки маршрутов"


# @receiver(pre_save, sender=Route)
# def update_route(sender, instance: Route, **kwargs):
#     if not instance.id:
#         return
#     else:
#         old_instance = sender.objects.get(id=instance.id)
#         old_station_ids = sorted(list(old_instance.current_stop.all().values_list('id', flat=True)))
#         print(old_station_ids)
#         new_station_ids = sorted(list(instance.current_stop.all().values_list('id', flat=True)))
#         print(new_station_ids)
#         if old_station_ids != new_station_ids:
#             async_to_sync(channel_layer.group_send)('auctions', {'type': 'send_new_data',
#                                                                  'text': json.dumps(auc_dict, indent=4, sort_keys=True, default=str)})
#             async_to_sync(channel_layer.group_send)('auction'+str(cur_auction.id), {'type': 'send_new_data',
#                                                                                      'text': json.dumps(auc_dict, indent=4, sort_keys=True, default=str)})
