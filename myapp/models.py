from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_driver=models.BooleanField(default=False)

class ChaloApiRequestLog(models.Model):
    name = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    query_string = models.TextField(blank=True)
    # Request Data
    request_headers = models.JSONField(default=dict, blank=True)
    request_body = models.JSONField(null=True, blank=True)
    # Response
    status_code = models.PositiveSmallIntegerField(default=0)
    response_headers = models.JSONField(default=dict, blank=True)
    response_body = models.JSONField(null=True, blank=True)
    
    duration_ms = models.PositiveIntegerField(default=0)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class StopGroup(models.Model):
    name = models.CharField(max_length=255)
    # def is_all_near(self, threshold_km=1):
    #     from geopy.distance import geodesic
    #     stops = list(self.stop_set.all())
    #     base = (stops[0].latitude, stops[0].longitude)
    #     return all(
    #         geodesic(base, (s.latitude, s.longitude)).km <= threshold_km
    #         for s in stops
    #     )
    def __str__(self):
        return self.name

class Stop(models.Model):
    group = models.ForeignKey(StopGroup, on_delete=models.CASCADE, related_name="stops",null=True, blank=True)
    stop_id = models.CharField(max_length=20, unique=True)
    short_id = models.IntegerField()
    # stop_name = models.CharField(max_length=255)
    stop_address = models.CharField(max_length=255, blank=True)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    city = models.CharField(max_length=100)
    transport_type = models.CharField(max_length=50)
    station_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        if self.group_id and getattr(self, "group", None):
            return self.group.name
        return self.stop_id

    def __str__(self):
        return self.display_name

class Route(models.Model):
    short_id = models.IntegerField(unique=True)
    route_id = models.CharField(max_length=20, unique=True)
    reverse_routeId = models.CharField(max_length=20, blank=True, null=True)
    route_name = models.CharField(max_length=255)
    internalName = models.CharField(max_length=50, blank=True, null=True)
    subCategory = models.CharField(max_length=30)
    serviceCategory = models.CharField(max_length=30)
    routeNamingScheme = models.CharField(max_length=20)
    direction = models.CharField(max_length=10)
    via = models.TextField(blank=True, help_text="Comma-separated list of intermediate stops")
    first_stop = models.ForeignKey(
        "Stop", related_name="routes_starting_here", on_delete=models.SET_NULL, null=True
    )
    last_stop = models.ForeignKey(
        "Stop", related_name="routes_ending_here", on_delete=models.SET_NULL, null=True
    )
    isPremiumBusRoute = models.BooleanField(default=False)
    polyline = models.TextField(blank=True, help_text="Encoded polyline string for the route path")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.route_name} ({self.route_id})"

class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()
    trip_duration = models.PositiveIntegerField()
    trip_id = models.CharField(max_length=20, unique=True)

    @staticmethod
    def format_seconds_as_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, _seconds = divmod(remainder, 60)
        period = "AM" if hours < 12 else "PM"
        display_hour = hours % 12 or 12
        return f"{display_hour}:{minutes:02d} {period}"

    @staticmethod
    def format_seconds_as_duration(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, _seconds = divmod(remainder, 60)
        if hours:
            return f"{hours} hr {minutes} min"
        return f"{minutes} min"

    @property
    def start_time_display(self):
        return self.format_seconds_as_time(self.start_time)

    @property
    def end_time_display(self):
        return self.format_seconds_as_time(self.end_time)

    @property
    def trip_duration_display(self):
        return self.format_seconds_as_duration(self.trip_duration)
    
class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.route.route_name} - {self.stop.display_name}'
