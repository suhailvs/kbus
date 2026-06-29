from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path("", TemplateView.as_view(template_name="googlemap.html"), name="home"),
    path("leaflet/", TemplateView.as_view(template_name="leafletmap.html")),
    path("route/<str:route_id>/", views.route, name="route"),
    path("route_live/<int:pk>/ajax/", views.route_live_status, name="route_live_status"),
    path("buses_in_radius/ajax/", views.buses_in_radius_live, name="buses_in_radius_live"),
    
]