from flask import Flask, render_template, render_template_string, request
from directions import geocode, mapbox_navigate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start-point']
        destination = request.form['destination']
        direction_JSONbeads = {'0': geocode(start), '1': geocode(destination)}
        return direction_JSONbeads
        #return render_template_string("get response from Directions API")

    else:
        return render_template('index.html') 

if __name__ == "__main__":
    app.run(host='0.0.0.0')