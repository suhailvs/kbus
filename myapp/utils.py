from datetime import datetime
import json
from django.db import transaction
from .models import Route, RouteStop, Stop, StopGroup, Trip
from . import chalo_api

def get_or_create_stop(stop_data):
    group, _ = StopGroup.objects.get_or_create(name=stop_data.get("stop_name"))
    stop, _created = Stop.objects.update_or_create(
        stop_id=stop_data["stop_id"],
        defaults={
            "short_id": stop_data.get("short_id"),
            "group": group,
            "stop_address": stop_data.get("stop_address", ""),
            "stop_lat": stop_data.get("stop_lat"),
            "stop_lon": stop_data.get("stop_lon"),
            "city": stop_data.get("city", ""),
            "transport_type": stop_data.get("transport_type", ""),
            "station_type": stop_data.get("station_type", ""),
        },
    )
    return stop

@transaction.atomic
def create_route(route_id):
    route = Route.objects.filter(route_id=route_id).first()
    if route:
        return (route, f"route({route_id}) already exists in DB.")
    payload = chalo_api.route_details(route_id,datetime.today().strftime("%A").lower())
    route_data = payload.get("route")
    if not route_data:
        return (None, "route key not found in chalo API response.")
    first_stop_data = route_data.get("first_stop")
    last_stop_data = route_data.get("last_stop")
    first_stop = get_or_create_stop(first_stop_data) if first_stop_data else None
    last_stop = get_or_create_stop(last_stop_data) if last_stop_data else None
    route, _created = Route.objects.update_or_create(
        route_id=route_data["route_id"],
        defaults={
            "short_id": route_data.get("short_id"),
            "reverse_routeId": route_data.get("reverse_routeId") or None,
            "route_name": route_data.get("route_name", ""),
            "internalName": route_data.get("internalName") or None,
            "subCategory": route_data.get("subCategory", ""),
            "serviceCategory": route_data.get("serviceCategory", ""),
            "routeNamingScheme": route_data.get("routeNamingScheme", ""),
            "direction": route_data.get("direction", ""),
            "via": route_data.get("via", ""),
            "first_stop": first_stop,
            "last_stop": last_stop,
            "isPremiumBusRoute": route_data.get("isPremiumBusRoute", False),
            "polyline": route_data.get("polyline", ""),
        },
    )
    stop_sequence = route_data.get("stopSequenceWithDetails", [])
    RouteStop.objects.filter(route=route).delete()
    route_stops = []
    for index, stop_data in enumerate(stop_sequence):
        stop = get_or_create_stop(stop_data)
        route_stops.append(RouteStop(route=route, stop=stop, order=index))
    RouteStop.objects.bulk_create(route_stops)    
    trips_data = payload.get("trips", [])
    for trip_data in trips_data:
        Trip.objects.update_or_create(
            trip_id=trip_data["trip_id"],
            defaults={
                "route": route,
                "start_time": trip_data.get("start_time"),
                "end_time": trip_data.get("end_time"),
                "trip_duration": trip_data.get("trip_duration"),
            },
        )        
    return (route, f"New route created successfully with {len(route_stops)} stops.")

def remove_duplicates(data):
    # remove_duplicate_bus_no_with_latest_ts
    latest = {}
    for key, raw_value in data.items():
        if not raw_value:
            continue
        entry = json.loads(raw_value)
        v_no = entry.get("vNo")
        ts = entry.get("tS", 0)
        if v_no not in latest or ts > latest[v_no][1].get("tS", 0):
            latest[v_no] = (key, entry)
    return {key: entry for key, (key, entry) in latest.items()}