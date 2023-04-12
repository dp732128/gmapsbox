import requests
import Maps_Functions as MP


def get_place_details_new(place_id, api_key):
    '''
    
    Get the place details of a location from google

    Arguments:
    place_id -- The place id for a place on google
    api_key -- Key used to allow access to Google api

    Returns:

    A dictionary containing various 
    
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
        "county": MP.get_administrative_region(place_id, api_key),

        "postal_code":post_code,
        #"post_code": get_postal_code(place_id, api_key)
        "first_post":post_code.split()[0]
        
    }

    #Return place details including county details
    return place_details

key = "AIzaSyChwMaYXlEXc0HpfCKJXUX2wPczmXWAmTw"
place = "ChIJWzJ3pQRceUgRiWQgaRF5uvg"

data = get_place_details_new(place,key)
print(data)