function busesInRadius(lat, lng, radius = 1000) {
    return $.ajax({
        url: `https://chalo.com/app/api/nearbybus/v2/city/PALAKKAD`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            metaData: { source: "web" },
            requiredFields: {
                nearbyBuses: { lat, lng, radius },
                cardsInfo: {}
            }
        }),
        success: function(response) {
            console.log('Buses:', response);
            const buses = response.buses.map(bus => ({
                name: bus.session._routeName,
                lat: String(bus.parameters.lat),
                log: String(bus.parameters.lon),
                route_id: bus.session._routeId,
                vehicle_id: bus.session._vehicleId,
            }));
            return buses;
        },
        error: function(xhr, status, error) {
            console.error('Error:', error, xhr.responseText);
        }
    });
}

function routeDetails(route_id, day) {
    return $.ajax({
        url: 'https://chalo.com/app/api/scheduler_v4/v4/palakkad/routedetailslive',
        method: 'GET',
        data: { route_id, day },
        success: function(response) {
            console.log('Route details:', response);
        },
        error: function(xhr, status, error) {
            console.error('Error:', error, xhr.responseText);
        }
    });
}

function routeLive(route, stop) {
    return $.ajax({
        url: `https://chalo.com/app/api/vasudha/track/route-live-info/palakkad/${route}`,
        method: 'GET',
        data: { stopIds: stop },
        success: function(response) {
            console.log('Route live info:', response);
        },
        error: function(xhr, status, error) {
            console.error('Error:', error, xhr.responseText);
        }
    });
}

busesInRadius(10.776, 76.971);
routeDetails('0bAuGARK', 'tuesday');
routeLive("0bAuGARK","pUEvXzth");