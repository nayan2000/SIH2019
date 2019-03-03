import requests
import json

# URLS
USGS_GEODATA_URL = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson'

SERVER_URL = 'http://139.59.85.163/main/auto_notify'
GEO_UPDATE_KEY = 'itsmeonlycozwearethebest'


# If there is a change, this function called
def create_alert(feature):
    print(feature)
    headers = {
	"content-type": "application/json",
	"geo-update-key": "{}".format(GEO_UPDATE_KEY),
    }
    payload = json.dumps({
        'title': '',
        'message': '',
        'mag': feature['properties']['mag'],
        'coords': feature['geometry']['coordinates'],
    })
    try:
        res = requests.post(url=SERVER_URL, headers=headers, data=payload)
    except:
        print('Could Not POST to URL')



# Get Geojson
def get_geodata(geo_url):
    georeq = requests.get(geo_url).text
    geoj = json.loads(georeq)
    with open('prev.geojson', 'r') as fl:
        prevData = json.load(fl)
    print('Done with geojsons')
    if not len(geoj['features']) or not len(prevData['features']):
        print('NO Data in past hour')
        return 2
    try:
        if geoj['features'][0]['properties']['place'] != prevData['features'][0]['properties']['place']:
            create_alert(geoj['features'][0])
            with open('prev.geojson', 'w') as f:
                f.write(json.dumps(geoj))
        else:
            print('The Data are same!')
    except:
        print('Unable to access prev.geojson or features')



def makePrev(geo_url):
    georeq = requests.get(geo_url).text
    geoj = json.loads(georeq)
    print(geoj)
    with open('prev.geojson', 'w+') as fl:
        fl.write(json.dumps(geoj))


# makePrev(USGS_GEODATA_URL)

get_geodata(USGS_GEODATA_URL)
