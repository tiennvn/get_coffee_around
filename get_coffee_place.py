#!/usr/bin/env python3

import requests
import json
import time

link_form = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" \
            "location={}&radius={}&name={}&pagetoken={}&key={}"


def get_place(location, radius, name, key, pagetoken=''):
    result = []
    while True:
        get_link = link_form.format(location, radius, name, pagetoken, key)
        print(get_link)
        while True:
            response = requests.get(get_link)
            data = response.text
            json_data = json.loads(data)
            if json_data['status'] == 'OVER_QUERY_LIMIT':
                time.sleep(30)
            else:
                result = result + json_data['results']
                break
        print('OK')
        if 'next_page_token' not in json_data:
            return result
        pagetoken = json_data['next_page_token']
        time.sleep(60)


def create_geojson(places_json):
    result = {"type": "FeatureCollection", "features": []}
    for place in places_json:
        place_geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place['geometry']['location']['lng'],
                                place['geometry']['location']['lat']]
            },
            "properties": {
                "Address": place['vicinity'],
                "name": place['name']
            }
        }
        result['features'].append(place_geojson)
    return result


def write_geojson(geojson_data):
    with open('map.geojson', 'wt') as file:
        json.dump(geojson_data, file, indent=2)


def main():
    with open('key', 'rt') as file:
        key = file.read().rstrip()
    print('key = ', key)
    location = '10.770002,106.686186'
    radius = '1000'
    name = 'coffee'
    write_geojson(create_geojson(get_place(location, radius, name, key)))
    print('DONE')


if __name__ == "__main__":
    main()
