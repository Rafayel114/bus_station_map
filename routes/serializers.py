from rest_framework import serializers
from . models import *


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = '__all__'


class CurrentStopSerializer(serializers.ModelSerializer):
    station = StationSerializer()

    class Meta:
        model = CurrentStop
        fields = ['id','index', 'is_active', 'station']


class RouteSerializer(serializers.ModelSerializer):
    current_stops = serializers.SerializerMethodField('get_current_stops')

    def get_current_stops(self, obj):
        stops = obj.current_stop.all()
        serialized = CurrentStopSerializer(stops, many=True).data
        return serialized

    class Meta:
        model = Route
        fields = [
            'id',
            'title',
            'number',
            'is_active',
            'current_stops'
        ]
