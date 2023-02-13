from django.contrib import admin
from . models import Station, Route, CurrentStop


class CurrentStopInline(admin.TabularInline):
    model = CurrentStop

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'number', 'is_active')
    inlines = [
        CurrentStopInline,
    ]
    ordering = ['id']

admin.site.register(Station)
admin.site.register(CurrentStop)
