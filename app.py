import flask
from flask import render_template, request, redirect, url_for, send_from_directory, send_file
import csv
import math
import time
import requests
import Maps_Functions as MF


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def index():
   print('Request for index page received')
   return render_template('basic.html')


@app.route('/getcoords', methods=['GET'])
def get_coords():
   print(request.args)
   coords = request.args['coords']
   fields = request.args['fields']
   print("original coords",coords)
   # Split the string by the "--" delimiter
   coords = coords[:-2]
   coords = coords.replace(")","")
   coord_strings = coords.split("--")
      # Extract the search query
   search_query = coord_strings[0]
   print(search_query)

   print("Fields selected:")
   print(fields)
   field_list = fields.split(",")
   print(field_list)

   # Extract the latitude and longitude values for each coordinate string
   coordinates = []
   for coord_string in coord_strings[1:]:
       lat, long = coord_string.split(",")
       lat = float(lat)
       long = float(long)
       coordinates.append((lat, long))

   # Print the results
   print("Search Query:", search_query)

   # Extract latitude and longitude values separately
   latitudes = [coord[0] for coord in coordinates]
   longitudes = [coord[1] for coord in coordinates]

   # Get north, south, east, and west most values
   north = max(latitudes)
   south = min(latitudes)
   east = max(longitudes)
   west = min(longitudes)

   # Print the results
   print("Searching over box with Coordinates:")
   print("North:", north)
   print("South:", south)
   print("East:", east)
   print("West:", west)
   
   box_search = MF.all(north,south,east,west,10,search_query,"")
   print(box_search)
   
   all_details = []
   for place in box_search:
      single = MF.get_place_details_new(place,"")
      all_details.append(single)
   
   print(all_details)
   filename = "download.csv"
   MF.write_to_csv_new(filename,all_details)
   
   print("Received request with coords:", coords)
   return send_file("download.csv", as_attachment=True)
   #return("hi")
   
   #key = AIzaSyChwMaYXlEXc0HpfCKJXUX2wPczmXWAmTw
   # Do stuff with coords, note the textsearch is bundled in, format returned is "textsearch--nwcoords--swcoords--etc..."
   # Recommend doing the Google Maps box stuff in here - trying the normal csv export to Colab or returning values/file to this front end

    
app.run()
