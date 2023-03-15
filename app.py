import flask
from flask import render_template, request, redirect, url_for, send_from_directory
import csv

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def index():
   print('Request for index page received')
   return render_template('basic.html')


@app.route('/getcoords', methods=['GET'])
def get_coords():
   coords = request.args['coords']
   
   print(coords)
   
   # Split the string by the "--" delimiter
   coords = coords[:-2]
   coords = coords.replace(")","")
   print(coords)
   
   # Do stuff with coords, note the textsearch is bundled in, format returned is "textsearch--nwcoords--swcoords--etc..."
   # Recommend doing the Google Maps box stuff in here - trying the normal csv export to Colab or returning values/file to this front end
   
   return "Request received" 
    
app.run()
