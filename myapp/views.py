from datetime import datetime
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Route, RouteStop,Stop
from .utils import remove_duplicates, get_or_create_route

def route(request, route_id):
    obj = Route.objects.filter(route_id=route_id).first()
    return render(request, "route.html", {'route':obj,'route_id':route_id})

@csrf_exempt
def ajax_save_route_details(request):
    route = get_or_create_route(json.loads(request.body))
    if route:
        return JsonResponse({
            'pk': route.pk,
            'polyline':route.polyline,
            'subCategory':route.subCategory,
            'serviceCategory':route.serviceCategory,
            'route_name': route.route_name,
            'via': route.via,
        })
    return JsonResponse({"error": "Failed to save route details."}, status=400)

@csrf_exempt
def ajax_route_live(request):
    raw_data = json.loads(request.body)
    routelive = remove_duplicates(raw_data['data']['routeLiveInfo'])
    route = Route.objects.get(id=raw_data['pk'])
    route_stops = RouteStop.objects.filter(route=route).select_related("stop")
    current_time = int(datetime.now().timestamp() * 1000)    
    buses_by_stop = {}
    for bus in routelive.values():
        if current_time - bus["tS"] > 15 * 60 * 1000:continue
        name=Stop.objects.get(stop_id=bus['psId']).group.name
        buses_by_stop.setdefault(bus['psId'], []).append({
            "vNo": bus["vNo"],
            "message":f"Left {name} {(current_time - bus['psTime']) // 1000} seconds ago",
            "lat":bus["_latitude"],
            "lng":bus["_longitude"],
        })
    stops_data = []
    for rs in route_stops:
        stop = rs.stop
        stops_data.append({
            "name": stop.group.name,
            "order": rs.order,
            "buses": buses_by_stop.get(stop.stop_id, []),
            "lat": stop.stop_lat,
            "lng": stop.stop_lon,
        })
    return JsonResponse({"route_id": route.route_id, "stops": stops_data})
