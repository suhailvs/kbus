from django.contrib import admin
from django.db.models import Count
from .models import Stop, User,Route,RouteStop, Trip, StopGroup, ChaloApiRequestLog

admin.site.register(User)
admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(RouteStop)
admin.site.register(Trip)

@admin.register(ChaloApiRequestLog)
class ChaloApiRequestLogAdmin(admin.ModelAdmin):
    list_display = ("name", "method", "path", "status_code", "duration_ms", "created_at")

@admin.register(StopGroup)
class StopGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "stop_count")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(stop_count=Count("stops"))

    def stop_count(self, obj):
        return obj.stop_count