from flask import Flask, render_template, request
from directions import mapbox_navigate, mapquest_api
#from pollution import pollutants
#import pprint

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start-point']
        destination = request.form['destination']
        #route generation
        #direction_JSONbeads = mapbox_navigate(start, destination)
        direction_JSONbeads = mapquest_api(start, destination)
        return render_template('index.html', directions_JSON=direction_JSONbeads)
    else:
        return render_template('index.html', directions_JSON=None) 

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


#def least_polluted_route():

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run()