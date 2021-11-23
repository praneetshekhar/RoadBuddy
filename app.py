from flask import Flask, render_template, request
from directions import geocode, mapbox_navigate
import pprint

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start-point']
        destination = request.form['destination']
        direction_JSONbeads = {'0': geocode(start), '1': geocode(destination)}
        return render_template('index.html', directions_JSON=direction_JSONbeads)
    else:
        return render_template('index.html', directions_JSON=None) 

if __name__ == "__main__":
    app.run(host='0.0.0.0')