from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("route/<str:route_id>/", views.route, name="route"),
    path("route/<int:pk>/ajax/", views.route_live_status, name="route_live_status"),
]