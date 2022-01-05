from flask import Flask, render_template, request
from directions import tomtom_getpoints, get_folium_map, clean_coords
import pandas as pd
import json
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start-point']
        destination = request.form['destination']
        #optimization_toggle = request.form['optimization']
        #regexp = re.compile(r'[^a-zA-Z0-9\s]+')
        #start = re.sub("\s+",re.sub(regexp, start, " "), " ")
        #destination = re.sub("\s+",re.sub(regexp, destination, " "), " ")

        directions_Collection = tomtom_getpoints(start, destination)
        if not directions_Collection:
            directions_Collection = ['No directions fetched']
        else:
            directions_df = pd.DataFrame(directions_Collection)
            
            print(directions_df['routePollutionScore'].to_list())
            least_polluted_route_number = directions_df['routePollutionScore'].idxmax()

            least_polluted_route = directions_df['coords'][least_polluted_route_number]
            print(directions_df)
            route_coords_list = clean_coords(pd.DataFrame(least_polluted_route))

            folium_map_object = get_folium_map(route_coords_list, start, destination)
            folium_map_object.save('templates/map.html')
        
        return render_template('index.html', directions=directions_Collection)
    else:
        return render_template('index.html', directions=None) 

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/route')
def render_map():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    