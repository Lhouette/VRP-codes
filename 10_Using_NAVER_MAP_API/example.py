import json
import urllib
from urllib.request import Request, urlopen
import folium
import webbrowser
import csv

option = 'trafast'
waypoint=[]

depot = ["경기도 광명시 일직로 40"]

store = ["경기도 용인시 기흥구 탑실로 38",
         "서울특별시 서초구 양재대로 159",
         "경기도 하남시 미사강변중앙로 40",
         "인천 연수구 컨벤시아대로230번길 60",
         "서울특별시 영등포구 선유로 156",
         "서울특별시 중랑구 망우로 336",
         "경기도 고양시 일산동구 장백로 25",
         "경기도 의정부시 용민로 489번길 9"]

chargingstation = ["서울특별시 노원구 상계2동 373-13",
                   "서울특별시 성동구 동일로 199",
                   "경기도 부천시 옥산로10번길 16",
                   "경기도 용인시 기흥구 구성로77번길 17"]

fuelstation = ["서울 관악구 남부순환로 1920"]

def get_optimal_route(start, goal, waypoint=waypoint, option=option):
    client_id = 'qi526b5swj'
    client_secret = 'lwJRz5esmKfJDGb8hg1nbMoxaoVJ4ouQgDBMswzt'

    url = f"https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start={start[0]},{start[1]}&goal={goal[0]},{goal[1]}&option={option}"
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)

    response = urllib.request.urlopen(request)
    res = response.getcode()

    if(res == 200) : 
        response_body = response.read().decode('utf-8')
        print('optimal route complete')
        return json.loads(response_body)
    else:
        print('ERROR')

def get_location(loc) :
    client_id = 'qi526b5swj'
    client_secret = 'lwJRz5esmKfJDGb8hg1nbMoxaoVJ4ouQgDBMswzt'
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" \
    			+ urllib.parse.quote(loc)
    
    # 주소 변환
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
    response = urlopen(request)
    res = response.getcode()
    
    if (res == 200) : # 응답이 정상적으로 완료되면 200을 return한다
        response_body = response.read().decode('utf-8')
        response_body = json.loads(response_body)
        #print(response_body)
        # 주소가 존재할 경우 total count == 1이 반환됨.
        if response_body['meta']['totalCount'] == 1 : 
        	# 위도, 경도 좌표를 받아와서 return해 줌.
            lat = response_body['addresses'][0]['y']
            lon = response_body['addresses'][0]['x']
            print('get location complete')
            return (lon, lat)
        else :
            print(loc + ': location not exist')
        
    else :
        print('ERROR')

def change(loc):
    return [loc[1], loc[0]]
'''
start = get_location("경기도 광명시 일직로 40")
goal = get_location("경기도 의정부시 용민로 489번길 9")
result = get_optimal_route(start, goal, option=option)


print('stop')

tL = result['route']['trafast'][0]['summary']['distance']
tT = result['route']['trafast'][0]['summary']['duration']
section = result['route']['trafast'][0]['section']'''

#result = get_optimal_route(start, goal, option=option)

#route = result['route']['trafast'][0]['path']
#route = list(map(change, route))

depot = list(map(get_location, depot))
depot = list(map(change, depot))

store = list(map(get_location, store))
store = list(map(change, store))

chargingstation = list(map(get_location, chargingstation))
chargingstation = list(map(change, chargingstation))

fuelstation = list(map(get_location, fuelstation))
fuelstation = list(map(change, fuelstation))

coordinates = depot+store+chargingstation+fuelstation
coordinates = list(map(change, coordinates))

route = []
c = []
e = []
t = []

rcf, rcs = 9600, 8600
ecf, ecs = 2700, 3600

for i in range(len(coordinates)):
    route.append([])
    c.append([])
    e.append([])
    t.append([])
    for j in range(len(coordinates)):
        print(i, j, '', end='')
        if i != j:
            result = get_optimal_route(coordinates[i], coordinates[j], option=option)
            route[i].append(result['route']['trafast'][0]['path'])
            with open('route/{}-{}.csv'.format(i, j), 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(route[i][j])
            tL = result['route']['trafast'][0]['summary']['distance']
            tT = result['route']['trafast'][0]['summary']['duration']
            section = result['route']['trafast'][0]['section']
            fL = 0
            for n in range(len(section)):
                if '고속도로' in section[n]['name']:
                    fL = fL + section[n]['distance']
            sL = tL - fL
            c[i].append(sL/rcs+fL/rcf)
            e[i].append(sL/ecs+fL/ecf)
            t[i].append(tT)
        else:
            print()
            route[i].append([])
            c[i].append(0)
            e[i].append(0)
            t[i].append(0)

with open('c.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(c)

with open('e.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(e)

with open('t.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(t)

Map = folium.Map(location=[37.527072, 126.973507], zoom_start=10, width=750, height=500, tiles='Stamen Terrain')

#folium.PolyLine(locations=route, tooltip='PolyLine').add_to(map)
for i in range(len(coordinates)):
    for j in range(len(coordinates)):
        if i == j:
            continue
        rut = list(map(change, route[i][j]))
        folium.PolyLine(locations=rut).add_to(Map)

for n in range(1):
    folium.Marker(location=depot[n], tooltip="COSTCO DEPOT", icon=folium.Icon(color='blue', icon="star")).add_to(Map)
for n in range(len(store)):
    folium.Marker(location=store[n], tooltip="COSTCO "+str(n), icon=folium.Icon(color='orange', icon="store", prefix="fa")).add_to(Map)
for n in range(len(chargingstation)):
    folium.Marker(location=chargingstation[n], tooltip="Charging Station "+str(n), icon=folium.Icon(color='green', icon='charging-station', prefix="fa")).add_to(Map)
for n in range(len(fuelstation)):
    folium.Marker(location=fuelstation[n], tooltip="Fuel Station "+str(n), icon=folium.Icon(color='red', icon='gas-pump', prefix="fa")).add_to(Map)

Map.save('map.html')
webbrowser.open_new_tab('map.html')

print("direction start")
#print(result)
print("direction end")

