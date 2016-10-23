# coding: utf-8

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

import requests
import polyline as pl


app = Flask(__name__, template_folder="templates")

API_KEY = 'AIzaSyC2dJqMwzhYxf6xiNYh9XVVrfLFFcMDwHs'


# you can set key as config
app.config['GOOGLEMAPS_KEY'] = API_KEY

# you can also pass key here
GoogleMaps(app, key=API_KEY)

def coord_to_str(coord):
    return str(coord[0]) + "," + str(coord[1])

def waypoints_to_str(waypoints):
    waypoints_str = "optimize:true"

    for waypoint in waypoints:
        waypoints_str += "|" + coord_to_str(waypoint)

    print(waypoints_str)
    return waypoints_str

@app.route("/")
def mapview():
    pokemons = [
        [33.678, -116.243],
        [33.679, -116.244], 
        [33.680, -116.250],
        [33.681, -116.239],
        [33.678, -116.289]
    ]

    # polyline = {}
    # polyline['stroke_weight'] = 20
    # polyline['stroke_opacity'] = 1.0
    # polyline['stroke_color'] = '#0AB0DE'
    # polyline['path'] = [{'lat':00.00}, {'lng':-50.000}, {'lat':50.00, 'lng':60.00}]

    # path1 = [(24.532, -123.43), (62.34, -12.34), (-34.23, 53.23), (34.23, -12.53)]

    pokemarkers = []
    for pokemon in pokemons:
        pokemarkers.append({
             'lat': pokemon[0],
             'lng': pokemon[1] })


    polyline = {
        'stroke_color': '#0AB0DE',
        'stroke_opacity': 1.0,
        'stroke_weight': 3,
    }


    directions_url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {}
    # params['origin'] = 'Disneyland'
    params['origin'] = coord_to_str(pokemons[0])
    params['destination'] = coord_to_str(pokemons[len(pokemons) - 1])
    params['waypoints'] = waypoints_to_str(pokemons[1:len(pokemons) - 1])
    params['key'] = API_KEY
    r = requests.get(directions_url, params=params, verify=False)
    json = r.json()
    # print("DIRECTIONS", json)
    print("DIRECTIONS")
    print(json)
    print(json['routes'][0]['overview_polyline']['points'])
    overview_polyline = pl.decode(json['routes'][0]['overview_polyline']['points'])
    print(overview_polyline)

    optimal_path = []
    for coord in overview_polyline:
        optimal_path.append({'lat':coord[0] ,'lng':coord[1]})
    # print(len(json['routes'][0]['legs']))

    polyline['path'] = optimal_path



    plinemap = Map(
        identifier="plinemap",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        lat=33.678,
        lng=-116.243,
        markers=pokemarkers,
        polylines=[polyline]
    )

    return render_template(
        'example.html',
        plinemap=plinemap
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
