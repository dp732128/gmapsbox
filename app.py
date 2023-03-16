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
   # Split the string by the "--" delimiter
   coords = coords[:-2]
   coords = coords.replace(")","")
   print(coords)
   coord_strings = coords.split("--")
      # Extract the search query
   search_query = coord_strings[0]

   # Extract the latitude and longitude values for each coordinate string
   coordinates = []
   for coord_string in coord_strings[1:]:
       lat, long = coord_string.split(",+")
       lat = float(lat)
       long = float(long)
       coordinates.append((lat, long))

   # Print the results
   print("Search Query:", search_query)
   print("Coordinates:")
   for coord in coordinates:
       print(coord)

   # Extract latitude and longitude values separately
   latitudes = [coord[0] for coord in coordinates]
   longitudes = [coord[1] for coord in coordinates]

   # Get north, south, east, and west most values
   north = max(latitudes)
   south = min(latitudes)
   east = max(longitudes)
   west = min(longitudes)

   # Print the results
   print("North:", north)
   print("South:", south)
   print("East:", east)
   print("West:", west)
   

   
   # Do stuff with coords, note the textsearch is bundled in, format returned is "textsearch--nwcoords--swcoords--etc..."
   # Recommend doing the Google Maps box stuff in here - trying the normal csv export to Colab or returning values/file to this front end
   print("Received request with coords:", coords)
   return "Success"

    
app.run()
