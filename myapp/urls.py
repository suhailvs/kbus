from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path("", TemplateView.as_view(template_name="googlemap.html"), name="home"),
    path("leaflet/", TemplateView.as_view(template_name="leafletmap.html")),
    path("route/<str:route_id>/", views.route, name="route"),
    path("ajax_save_route_details/", views.ajax_save_route_details),
    path("ajax_route_live/", views.ajax_route_live),
    
]