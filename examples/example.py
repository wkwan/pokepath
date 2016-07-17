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
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers={
            icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")]
        }
    )

    trdmap = Map(
        identifier="trdmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'icon': icons.alpha.B,
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox': "Hello I am <b style='color:green;'>GREEN</b>!"
            },
            {
                'icon': icons.dots.blue,
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "Hello I am <b style='color:blue;'>BLUE</b>!"
            },
            {
                'icon': '//maps.google.com/mapfiles/ms/icons/yellow-dot.png',
                'lat': 37.4500,
                'lng': -122.1350,
                'infobox': (
                    "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                    "<h2>It is HTML title</h2>"
                    "<img src='//placehold.it/50'>"
                    "<br>Images allowed!"
                )
            }
        ]
    )

    clustermap = Map(
        identifier="clustermap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'lat': 37.4500,
                'lng': -122.1350
            },
            {
                'lat': 37.4400,
                'lng': -122.1350
            },
            {
                'lat': 37.4300,
                'lng': -122.1350
            },
            {
                'lat': 36.4200,
                'lng': -122.1350
            },
            {
                'lat': 36.4100,
                'lng': -121.1350
            }
        ],
        zoom=12,
        cluster=True
    )

    rectangle = {
        'stroke_color': '#0000FF',
        'stroke_opacity': .8,
        'stroke_weight': 5,
        'fill_color': '#FFFFFF',
        'fill_opacity': .1,
        'bounds': {
                  'north': 33.685,
                  'south': 33.671,
                  'east': -116.234,
                  'west': -116.251
        }
    }

    rectmap = Map(
        identifier="rectmap",
        lat=33.678,
        lng=-116.243,
        rectangles=[
            rectangle,
            [33.678, -116.243, 33.671, -116.234],
            (33.685, -116.251, 33.678, -116.243),
            [(33.679, -116.254), (33.678, -116.243)],
            ([33.689, -116.260], [33.685, -116.250]),
        ]
    )

    circle = {
        'stroke_color': '#FF00FF',
        'stroke_opacity': 1.0,
        'stroke_weight': 7,
        'fill_color': '#FFFFFF',
        'fill_opacity': .8,
        'center': {
                  'lat': 33.685,
                  'lng': -116.251
        },
        'radius': 2000,
    }

    circlemap = Map(
        identifier="circlemap",
        lat=33.678,
        lng=-116.243,
        circles=[
            circle,
            [33.685, -116.251, 1000],
            (33.685, -116.251, 1500),
        ]
    )


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
        lat=33.678,
        lng=-116.243,
        markers=pokemarkers,
        polylines=[polyline]
    )

    polygon = {
        'stroke_color': '#0AB0DE',
        'stroke_opacity': 1.0,
        'stroke_weight': 3,
        'fill_color': '#ABC321',
        'fill_opacity': .5,
        'path': [{'lat': 33.678, 'lng': -116.243},
                 {'lat': 33.679, 'lng': -116.244},
                 {'lat': 33.680, 'lng': -116.250},
                 {'lat': 33.681, 'lng': -116.239},
                 {'lat': 33.678, 'lng': -116.243}]
    }



    path1 = [(33.665, -116.235), (33.666, -116.256),
             (33.667, -116.250), (33.668, -116.229)]

    path2 = ((33.659, -116.243), (33.660, -116.244),
             (33.649, -116.250), (33.644, -116.239))

    path3 = ([33.688, -116.243], [33.680, -116.244],
             [33.682, -116.250], [33.690, -116.239])

    path4 = [[33.690, -116.243], [33.691, -116.244],
             [33.692, -116.250], [33.693, -116.239]]


    pgonmap = Map(
        identifier="pgonmap",
        lat=33.678,
        lng=-116.243,
        polygons=[polygon, path1, path2, path3, path4]
    )

    return render_template(
        'example.html',
        mymap=mymap,
        sndmap=sndmap,
        trdmap=trdmap,
        rectmap=rectmap,
        circlemap=circlemap,
        plinemap=plinemap,
        pgonmap=pgonmap,
        clustermap=clustermap
    )


@app.route('/fullmap')
def fullmap():

    polyline = {
        'stroke_color': '#0AB0DE',
        'stroke_opacity': 1.0,
        'stroke_weight': 3,
        'path': [{'lat': 33.678, 'lng': -116.243},
                 {'lat': 33.679, 'lng': -116.244},
                 {'lat': 33.680, 'lng': -116.250},
                 {'lat': 33.681, 'lng': -116.239},
                 {'lat': 33.678, 'lng': -116.243}]
    }

    path1 = [(33.665, -116.235), (33.666, -116.256),
             (33.667, -116.250), (33.668, -116.229)]

    path2 = ((33.659, -116.243), (33.660, -116.244),
             (33.649, -116.250), (33.644, -116.239))

    path3 = ([33.688, -116.243], [33.680, -116.244],
             [33.682, -116.250], [33.690, -116.239])

    path4 = [[33.690, -116.243], [33.691, -116.244],
             [33.692, -116.250], [33.693, -116.239]]


    fullmap = Map(
        identifier="fullmap",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'icon': '//maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox': "Hello I am <b style='color:green;'>GREEN</b>!"
            },
            {
                'icon': '//maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "Hello I am <b style='color:blue;'>BLUE</b>!"
            },
            {
                'icon': icons.dots.yellow,
                'title': 'Click Here',
                'lat': 37.4500,
                'lng': -122.1350,
                'infobox': (
                    "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                    "<h2>It is HTML title</h2>"
                    "<img src='//placehold.it/50'>"
                    "<br>Images allowed!"
                )
            }
        ],
        polylines=[polyline, path1, path2, path3, path4]
        # maptype = "TERRAIN",
        # zoom="5"
    )
    return render_template('example_fullmap.html', fullmap=fullmap)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
