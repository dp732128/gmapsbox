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
   textsearch = request.args['textsearch']
   print(coords)
   print(textsearch)
   return "Request received" 
    
app.run()
