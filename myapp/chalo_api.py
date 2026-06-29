import requests

API_URL='https://chalo.com/app/'

def busses_in_radius():
    url = f'{API_URL}api/nearbybus/v2/city/PALAKKAD'
    headers = {
        'accept': 'application/json',
        'accesstoken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI3MzU2Nzc1OTgxIiwiZGV2aWNlSWQiOiJmYjNiZDgxNjU4NzYyZDhlYTJiMmEwODNkODYxZDY1OSIsImlhdCI6MTc4MjM3MzU1NSwiZXhwIjoxNzgyMzgwNzU1LCJqdGkiOiJlbHd6MW1xdDc3MTZqIn0.BK_W7wiT0_jmgHnjvPTZsP0ktVk1S5J9TaHbHCZPynE',
        'authtype': 'ACCESS_TOKEN',
        'content-type': 'application/json',
        'deviceid': 'fb3bd81658762d8ea2b2a083d861d659',
        'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',    
        'source': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
        'userid': '7356775981',
        'x-type': 'pass',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://chalo.com',
        'priority': 'u=1, i',
        'referer': f'{API_URL}nearest-bus-stop/live-map',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',        
    }
    cookies = {
        '_gcl_au': '1.1.1984223656.1782373503',
        '_fbp': 'fb.1.1782373503545.596836865874114001',
        '_ga': 'GA1.1.1496000061.1782373504',
        '_ga_5PRF9T2GLN': 'GS2.1.s1782373504$o1$g0$t1782373506$j58$l0$h0',
        'mp_b1925cf6c0b3db7d5f3904a66abf8ec7_mixpanel': '{"distinct_id":"fb3bd81658762d8ea2b2a083d861d659","$device_id":"69b9c059-6e28-4b09-a3e8-f941e2c18f3f","$initial_referrer":"https://chalo.com/chalo-app/track-your-bus-live","$initial_referring_domain":"chalo.com","__mps":{},"__mpso":{},"__mpus":{},"__mpa":{},"__mpu":{},"__mpr":[],"__mpap":[],"$user_id":"fb3bd81658762d8ea2b2a083d861d659","clientSource":"PWA","appVersionCode":"1001","selected language":"English","timeZone":"+05:30","deviceId":"fb3bd81658762d8ea2b2a083d861d659","mailId":"","phone":"7356775981","gender":"","firstName":"","lastName":"","mobileNumber":"7356775981","userId":"7356775981","selectedCity":"palakkad"}',
        '_ga_SEWPQ4G3XZ': 'GS2.1.s1782373509$o1$g1$t1782373609$j60$l0$h0',
    }
    payload = {"metaData":{"source":"web"},"requiredFields":{"nearbyBuses":{"lat":"10.5962","lng":"76.4814","radius":"1000.0"},"cardsInfo":{}}}
    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    data = response.json()
    return data
    
def route_details(route,day):
    '''
    Get full route details. all stops for a route.
    '''
    url = f'{API_URL}api/scheduler_v4/v4/palakkad/routedetailslive'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'referer': f'{API_URL}live-tracking/route-map/{route}',
        'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'source': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
        'x-type': 'pass',
    }
    cookies = {
        '_gcl_au': '1.1.1984223656.1782373503',
        '_fbp': 'fb.1.1782373503545.596836865874114001',
        '_ga': 'GA1.1.1496000061.1782373504',
        '_ga_5PRF9T2GLN': 'GS2.1.s1782373504$o1$g0$t1782373506$j58$l0$h0',
        '_ga_SEWPQ4G3XZ': 'GS2.1.s1782373509$o1$g1$t1782376462$j46$l0$h0',
        'mp_b1925cf6c0b3db7d5f3904a66abf8ec7_mixpanel': '{"distinct_id":"fb3bd81658762d8ea2b2a083d861d659","$device_id":"69b9c059-6e28-4b09-a3e8-f941e2c18f3f","$initial_referrer":"https://chalo.com/chalo-app/track-your-bus-live","$initial_referring_domain":"chalo.com","__mps":{},"__mpso":{},"__mpus":{},"__mpa":{},"__mpu":{},"__mpr":[],"__mpap":[],"$user_id":"fb3bd81658762d8ea2b2a083d861d659","clientSource":"PWA","appVersionCode":"1001","selected language":"English","timeZone":"+05:30","deviceId":"fb3bd81658762d8ea2b2a083d861d659","mailId":"","phone":"7356775981","gender":"","firstName":"","lastName":"","mobileNumber":"7356775981","userId":"7356775981","selectedCity":"palakkad"}',
    }
    params = {'route_id': route,'day': day}
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    data = response.json()
    return data

def route_live(route,stop):
    url = f'{API_URL}api/vasudha/track/route-live-info/palakkad/{route}?stopIds={stop}'
    headers = {
        'sec-ch-ua-platform': '"Linux"',
        'Referer': f'{API_URL}live-tracking/route-map/{route}',
        'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'x-type': 'pass',
        'source': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }    
    response = requests.get(url, headers=headers)
    data = response.json()
    return data