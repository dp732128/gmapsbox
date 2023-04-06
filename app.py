import flask
from flask import render_template, request, redirect, url_for, send_from_directory, send_file
import csv
import math
import time
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def index():
   print('Request for index page received')
   return render_template('basic.html')


def split_bounds(north, south, east, west, box_side_length_km):

    #Calculate central lat/lng values
    avg_lat = (north +south)/2
    avg_lng = (east + west)/2

    #Give length of integer change of 1 for lat and lng in km (So a change in lat of 12 to 13 covers 111.2 km)
    lat_in_km = 111.2
    lng_in_km = 111.2 * math.cos(math.radians(avg_lat))

    #Calculate side length of boxes in lat/lng change
    box_lat = box_side_length_km/lat_in_km
    box_lng = box_side_length_km/lng_in_km

    #Calculate the number of coordinate cutoffs for lat/lng directions for the boxes
    #add one so you overrun to make sure you full emcompass the box defined in the function parameters
    lat_cutoffs = int((north - south)/box_lat)+1
    lng_cutoffs = int((east - west)/box_lng)+1

    #create the boxes by dividing the region into smaller boxes
    boxes = []
    for i in range(lat_cutoffs):
        for j in range(lng_cutoffs):
            box_north = north - (i * box_lat)
            box_south = box_north - box_lat
            box_east = east - (j * box_lng)
            box_west = box_east - box_lng

            avg_lat = (box_north + box_south) / 2
            avg_lng = (box_east + box_west) / 2

            #Create box with north, south, east, west values and central lat/lng values
            boxes.append((box_north, box_south, box_east, box_west, avg_lat, avg_lng))

    return boxes


def get_place_ids(api_key, location_list, radius, keyword):
    # Create an empty array to store the place IDs
    place_ids = []

    # Loop through the list of locations
    for location in location_list:
        lat, lng = location

        # Construct the API request URL
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&keyword={keyword}&key={api_key}"

        # Send the API request
        response = requests.get(url)

        # Sleep to avoid overloading Google API
        time.sleep(3)

        # Check if the API request was successful
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            # Loop through the results and add the place_id to the array if it hasn't already been added
            for result in results:
                place_id = result["place_id"]
                if place_id not in place_ids:
                    place_ids.append(place_id)

            # Check if there are more pages of results
            next_page_token = data.get("next_page_token")
            while next_page_token:
                # Construct the API request URL for the next page of results
                url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={api_key}"

                # Send the API request for the next page of results
                response = requests.get(url)

                # Sleep to avoid overloading Google API
                time.sleep(3)

                # Check if the API request was successful
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])

                    # Loop through the results and add the place_id to the array if it hasn't already been added
                    for result in results:
                        place_id = result["place_id"]
                        if place_id not in place_ids:
                            place_ids.append(place_id)

                    # Check if there are more pages of results
                    next_page_token = data.get("next_page_token")
                else:
                    print("API request failed with status code", response.status_code)
                    break
        else:
            print("API request failed with status code", response.status_code)

    # Return the unique place IDs
    return place_ids
   
def get_place_ids_one_location(api_key, lat, lng, radius, keyword):
    # Create an empty array to store the place IDs
    place_ids = []

    # Construct the API request URL
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&keyword={keyword}&key={api_key}"

    # Send the API request
    response = requests.get(url)

    # Sleep to avoid overloading Google API
    time.sleep(5)

    # Check if the API request was successful
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        # Loop through the results and add the place_id to the array if it hasn't already been added
        for result in results:
            place_id = result["place_id"]
            if place_id not in place_ids:
                place_ids.append(place_id)

        # Check if there are more pages of results
        next_page_token = data.get("next_page_token")
        while next_page_token:
            # Construct the API request URL for the next page of results
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={api_key}"

            # Send the API request for the next page of results
            response = requests.get(url)

            # Sleep to avoid overloading Google API
            time.sleep(5)

            # Check if the API request was successful
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                # Loop through the results and add the place_id to the array if it hasn't already been added
                for result in results:
                    place_id = result["place_id"]
                    if place_id not in place_ids:
                        place_ids.append(place_id)

                # Check if there are more pages of results
                next_page_token = data.get("next_page_token")
            else:
                print("API request failed with status code", response.status_code)
                break
    else:
        print("API request failed with status code", response.status_code)

    # Return the unique place IDs
    return place_ids
   
def remove_duplicates(places):
    # Convert the list to a set to remove duplicates
    unique_places = set(places)
    # Convert the set back to a list
    return list(unique_places)

def write_to_csv_new(file_name, details_list):
    with open(file_name, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "address", "phone_number", "website", "county","postal_code","first_post"])
        writer.writeheader()
        for row in details_list:
            writer.writerow(row)

def all(north, south, east, west, box_side_length_km, search, api_key):

    #Create the list to store place ids
    all_place_ids = []
    #Call the split bounds function to create smaller boxes
    boxes = split_bounds(north, south, east, west, box_side_length_km)


    location_list = [(box[-2], box[-1]) for box in boxes]
    #For each box
    for box in boxes:


        # Calculate the radius in meters
        radius = box_side_length_km/(2 * math.sin(math.radians(45))) * 1000

        #Get place_ids for one box search
        one_location_place_ids = get_place_ids_one_location(api_key, box[-2], box[-1], radius, search)

        #If 60 results come back, ae: the return results was capped out by the google api
        if len(one_location_place_ids) > 59:
            # Recursively call the function for smaller boxes
            recursive_results = all(box[0], box[1], box[2], box[3], (box_side_length_km/2), search, api_key)

            #Add each result from the recursive call to the list
            for result in recursive_results:
                all_place_ids.append(result)
        else:
            # Append the place IDs of the current box
            for location in one_location_place_ids:
                all_place_ids.append(location)

    #Remove duplicate locations
    all_place_ids = remove_duplicates(all_place_ids)

    #return list of place ids
    return all_place_ids


def get_administrative_region(place_id,api_key):

  #Send Request to Google places API
  url = f"https://maps.googleapis.com/maps/api/geocode/json?place_id={place_id}&key={api_key}"
  response = requests.get(url).json()
  #Take the county info out of the response
  for address_component in response["results"][0]["address_components"]:
    if "administrative_area_level_2" in address_component["types"]:

      #Return county name the place is located in
      return address_component["long_name"]




   
def get_place_details_new(place_id, api_key):
    #Send request to the Google places API  
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url).json()
    #print(response)

    for address_component in response["result"]["address_components"]:
       if "postal_code" in address_component["types"]:
            post_code = address_component["long_name"]

    #Get relevent data points from response
    place_details = {
        "name": response["result"].get("name"),
        "address": response["result"].get("formatted_address"),
        "phone_number": response["result"].get("formatted_phone_number"),
        "website": response["result"].get("website"),

        #Also get county info from seperate function
        "county": get_administrative_region(place_id, api_key),

        "postal_code":post_code,
        #"post_code": get_postal_code(place_id, api_key)
        "first_post":post_code.split()[0]
        
    }

    #Return place details including county details
    return place_details


@app.route('/getcoords', methods=['GET'])
def get_coords():
   print(request.args)
   coords = request.args['coords']
   print("original coords",coords)
   # Split the string by the "--" delimiter
   coords = coords[:-2]
   coords = coords.replace(")","")
   coord_strings = coords.split("--")
      # Extract the search query
   search_query = coord_strings[0]
   print(search_query)

   # Extract the latitude and longitude values for each coordinate string
   coordinates = []
   for coord_string in coord_strings[1:]:
       lat, long = coord_string.split(",")
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
   
   box_search = all(north,south,east,west,10,search_query,"AIzaSyDyHYFGmruIyKYmcBw6iKPIYZdfx1fV_AM")
   print(box_search)
   
   all_details = []
   for place in box_search:
      single = get_place_details_new(place,"AIzaSyDyHYFGmruIyKYmcBw6iKPIYZdfx1fV_AM")
      all_details.append(single)
   
   print(all_details)
   filename = "download.csv"
   write_to_csv_new(filename,all_details)
   
   print("Received request with coords:", coords)
   return send_file("/content/gmapsbox/download.csv", as_attachment=True)
   #return("hi")
   
   # Do stuff with coords, note the textsearch is bundled in, format returned is "textsearch--nwcoords--swcoords--etc..."
   # Recommend doing the Google Maps box stuff in here - trying the normal csv export to Colab or returning values/file to this front end

    
app.run()
