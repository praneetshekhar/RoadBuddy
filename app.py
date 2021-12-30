from flask import Flask, render_template, request
from directions import tomtom_getpoints
from pollution import routePollutionScore

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start-point']
        destination = request.form['destination']

        direction_JSONbeads = tomtom_getpoints(start, destination)
        
        route1_score = routePollutionScore(direction_JSONbeads["optimizedRoute1"])
        route2_score = routePollutionScore(direction_JSONbeads["optimizedRoute2"])
        if route1_score < route2_score:
            directions = direction_JSONbeads['optimizedRoute1']
        else:
            directions = direction_JSONbeads['optimizedRoute2']
        
        return render_template('index.html', directions_JSON=directions)
    else:
        return render_template('index.html', directions_JSON=None) 

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


#def least_polluted_route():

if __name__ == "__main__":
    app.run(host='0.0.0.0')