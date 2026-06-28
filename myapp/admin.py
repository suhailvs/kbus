from django.contrib import admin
from .models import Stop, User,Route,RouteStop, Trip


admin.site.register(User)
admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(RouteStop)
admin.site.register(Trip)