from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .models import Route, RouteStop,Stop
from .utils import remove_duplicates, get_or_create_route
from . import chalo_api

def route(request, route_id):
    route,msg = get_or_create_route(route_id)
    if not route:
        return JsonResponse({"status":400,"msg": msg})
    return render(request, "route.html", {"route":route,"msg": msg})

def buses_in_radius_live(request):
    print(request.GET.get("lat"),request.GET.get("lng"))
    return JsonResponse({"buses": [
        { "name": "Palakkad-Pathanamthitta", "lat": "10.59975", "log": "76.45969" },
        { "name": "Bus 2", "lat": "10.599793", "log": "76.460434" }
    ]})
def route_live_status(request, pk):
    route = Route.objects.get(id=pk)
    route_stops = RouteStop.objects.filter(route=route).select_related("stop")
    raw_data = remove_duplicates(chalo_api.route_live(route.route_id,route.first_stop.stop_id)['routeLiveInfo'])
    current_time = int(datetime.now().timestamp() * 1000)    
    buses_by_stop = {}
    for bus in raw_data.values():
        if current_time - bus["tS"] > 15 * 60 * 1000:continue
        name=Stop.objects.get(stop_id=bus['psId']).group.name
        buses_by_stop.setdefault(bus['psId'], []).append({
            "vNo": bus["vNo"],
            "message":f"Left {name} {(current_time - bus['psTime']) // 1000} seconds ago",
        })
    stops_data = []
    for rs in route_stops:
        stop = rs.stop
        stops_data.append({
            "name": stop.group.name,
            "platform": "Platform 1",
            "buses": buses_by_stop.get(stop.stop_id, []),
        })
    return JsonResponse({"route_id": route.route_id, "stops": stops_data})
