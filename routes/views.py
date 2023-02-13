from django.shortcuts import render
from django.views.generic import View


class RouteMap(View):
    def get(self, request, pk=None):
        return render(request, 'routes/route_panel_control.html')
