from django.contrib import admin
from django.db.models import Count
from .models import Stop, User,Route,RouteStop, Trip, StopGroup

admin.site.register(User)
admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(RouteStop)
admin.site.register(Trip)

@admin.register(StopGroup)
class StopGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "stop_count")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(stop_count=Count("stops"))

    def stop_count(self, obj):
        return obj.stop_count