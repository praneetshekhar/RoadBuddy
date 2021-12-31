from flask import Flask, render_template, request
from directions import tomtom_getpoints
from pollution import routePollutionScore
import pandas as pd
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start-point']
        destination = request.form['destination']
        start = start.replace(',', '')
        destination = destination.replace(',', '')

        direction_JSONbeads = tomtom_getpoints(start, destination)
        
        route1_score = routePollutionScore(direction_JSONbeads["optimizedRoute1"])
        route2_score = routePollutionScore(direction_JSONbeads["optimizedRoute2"])
        if route1_score < route2_score:
            route = 1
            directions = direction_JSONbeads['optimizedRoute1'].to_json()
        else:
            route = 2
            directions = direction_JSONbeads['optimizedRoute2'].to_json()
                
        print(route)
        return render_template('index.html', directions_JSON=json.loads(directions))
    else:
        return render_template('index.html', directions_JSON=None) 

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')