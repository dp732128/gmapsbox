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
   '''

    Takes a list of location details and converts to csv format then writes to location

    Takes in the Coords and Fields from the webpage. Splits the coords into the coords for the box and the search query and takes the field values.
    Does a search based on the coordinate values and the search query. Brings back details depending on what fields were asked for.
    
    '''
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
   
   box_search = MF.all(north,south,east,west,10,search_query,"AIzaSyChwMaYXlEXc0HpfCKJXUX2wPczmXWAmTw")
   print(box_search)
   
   all_details = []
   for place in box_search:
      single = MF.get_place_details_new(place,"AIzaSyChwMaYXlEXc0HpfCKJXUX2wPczmXWAmTw",fields)
      all_details.append(single)
   
   filename = "place_details.csv"
   if(len(all_details)>0):
      print("TOTAL RESULTS:"+str(len(all_details)))
      write_fields = all_details[0]
      MF.write_to_csv_new(filename,all_details,write_fields)
      print("Written to csv at: "+filename)

      fields_split = fields.split(",")
      ratings = []
      if("reviews" in fields_split):
         for location in all_details:
            if(location["reviews"] is not None):
               for review in location["reviews"]:
                     #print("location is:")
                     #print(location)
                     review_new = {"name":location["name"]}
                     review_new["place_id"] = location["place id"]
                     #review["company"] = (location["name"])
                     review_new.update(review)
                     review_new['text'] = review_new['text'].replace("\n"," ")
                     ratings.append(review_new)

         MF.write_to_csv_new("reviews.csv",ratings,ratings[0])
         print("Review written to: reviews.csv")





   else:
      print("NO RESULTS")
   
   print("Received request with coords:", coords)
   #return send_file("download.csv", as_attachment=True)
   return("success")
   #return("hi")
   
   #key = AIzaSyChwMaYXlEXc0HpfCKJXUX2wPczmXWAmTw
   # Do stuff with coords, note the textsearch is bundled in, format returned is "textsearch--nwcoords--swcoords--etc..."
   # Recommend doing the Google Maps box stuff in here - trying the normal csv export to Colab or returning values/file to this front end

    
app.run()
