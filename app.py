from flask import Flask, render_template, request
from directions import tomtom_getpoints
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

        directions_JSON = tomtom_getpoints(start, destination)
        
        return render_template('index.html', directions=directions_JSON)
    else:
        return render_template('index.html', directions=None) 

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')