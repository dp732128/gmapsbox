import math
import csv
import requests
import time


def split_bounds(north, south, east, west, box_side_length_km):
    """
    Split a large georgraphic box into smaller boxes

    Arguments:
    north -- the north lat for the geographic box
    south -- the south lat for the geographic box
    east -- the east long for the geographic box
    west -- the west long for the geographic box
    box_side_length_km -- the size you want the smaller boxes to be (box_side_lenth_km of 10 would mean each smaller box is 10 square kilometers big)

    Returns:
    
    An array of boxes with north,south,east,west and lat long average values 
    
    """

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
    '''
    
    Do a google maps search over a list of locations and compile the results

    Arguments:
    api_key -- the key used for the google maps api
    location_list -- a set of locations (in the form of lat,long)
    radius -- the radius for the google maps search
    keyword -- the search word for the search

    Returns:

    A list of place_ids recognized by google. (these can be used to request details)
    
    '''




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
    '''
    
    Do a google maps search over a list of locations and compile the results

    Arguments:
    api_key -- the key used for the google maps api
    lat -- The latitude value for the search point
    lng -- the longatide value for the search point
    radius -- the radius for the google maps search
    keyword -- the search word for the search

    Returns:

    A list of place_ids recognized by google for this search location. (these can be used to request details)
    
    '''
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
        print(data)

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
    '''
    Takes a list of places and removes duplicates

    Arguments:
    places -- a list of place ids

    Returns 

    The place ids list with duplicates removed
    
    
    '''
    # Convert the list to a set to remove duplicates
    unique_places = set(places)
    # Convert the set back to a list
    return list(unique_places)

def write_to_csv_new(file_name, details_list):
    '''

    Takes a list of location details and converts to csv format then writes to location

    Arguments:

    file_name -- name to be given to file when created
    details_list -- the list of places and their details to be turned into the csv

    Returns:

    Nothing ***To Change. Either have it return a file or a error code value to indicate success.*** 
    
    
    '''
    with open(file_name, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "address", "phone_number", "website", "county","postal_code","first_post"])
        writer.writeheader()
        for row in details_list:
            writer.writerow(row)

def all(north, south, east, west, box_side_length_km, search, api_key):
    '''
    Searches for all of a given search query in a geographic area. 

    Arguments:
    north -- north lat of the geographic area
    south -- south lat of the geographic area
    east -- east long of the geographic area
    west -- west long of the geographic area
    box_side_length_km -- Initial box search size. **Deprecated and probably not nessesary - fix later**
    search -- search value to use over google maps
    api_key -- api key to allow use of google maps api

    Returns:

    A list of place ids corresponding to matches within the geographic area.
    
    
    '''

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
  '''

  Gets the administrative region of a location is situated in

  Arguments:

  place_id -- The place id to find the region of
  api_key -- Key used to allow access to Google api

  Returns:

  A string name of administrative region
  
  
  '''

  #Send Request to Google places API
  url = f"https://maps.googleapis.com/maps/api/geocode/json?place_id={place_id}&key={api_key}"
  response = requests.get(url).json()
  #Take the county info out of the response
  for address_component in response["results"][0]["address_components"]:
    if "administrative_area_level_2" in address_component["types"]:

      #Return county name the place is located in
      return address_component["long_name"]

   
def get_place_details_new(place_id, api_key):
    '''
    
    Get the place details of a location from google

    Arguments:
    place_id -- The place id for a place on google
    api_key -- Key used to allow access to Google api
    ***Want to take in Fields, to decide what things to get details of.***

    Returns:

    A dictionary containing various fields and their value. Example: {'name':'Happy shop','address':'Happy street, new york', etc ...}
    
    '''
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
