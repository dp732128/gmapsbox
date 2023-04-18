import requests
import Maps_Functions as MF

fields_in = "name,formatted_address,post_code,geometry,place_id,county"
def get_place_details_new(place_id, api_key,fields_in):
    '''
    
    Get the place details of a location from google

    Arguments:
    place_id -- The place id for a place on google
    api_key -- Key used to allow access to Google api
    ***Want to take in Fields, to decide what things to get details of.***

    Returns:

    A dictionary containing various fields and their value. Example: {'name':'Happy shop','address':'Happy street, new york', etc ...}
    
    '''

    #Split fields for use later in the code
    fields_split = fields_in.split(",")
    print(fields_split)

    fields_out = []
    for field in fields_split:
        if(field != "county" and field != "post_code"):
            fields_out.append(field)
        else:
            fields_out.append("address_components")
    print(fields_out)
    fields_set = set(fields_out)
    print(fields_set)
    fields_out_str = ', '.join(fields_set)




    #Send request to the Google places API  
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}&fields={fields_out_str}"
    response = requests.get(url).json()
    print(response)
    result = response["result"]
    print(result)
    #print(response)
    place_details = {}
    if("name"in fields_split):
        place_details["name"] = result.get("name")
    if("formatted_address" in fields_split):
        place_details["address"] = result.get("formatted_address")
    if("address_component" in fields_split):
            for address_component in response["result"]["address_components"]:
                if('postal_code' in address_component['types']):
                    place_details["post code"] = address_component["long_name"]
    if('website' in fields_split):
        place_details["website"] = result.get("website")
    if("phone" in fields_split):
         place_details["phone number"] = result.get("formatted_phone_number")
    if("county" in fields_split):
         #place_details["county"] = MF.get_administrative_region(place_id,api_key)
        for address_component in response["result"]["address_components"]:
            if('administrative_area_level_2' in address_component['types']):
                place_details["county"] = address_component["long_name"]
    if("geometry" in fields_split):
        for component in response["result"]["geometry"]:
            if('location') in component:
                place_details["lat"] = response["result"]["geometry"]["location"]["lat"]
                place_details["lng"] = response["result"]["geometry"]["location"]["lng"]




    if("place_id" in fields_split):
        place_details["place id"] = place_id
    
    

        
        


    #Continue from hereeeee
    
    
    print(place_details)



    #Return place details including county details
    return place_details

key = "AIzaSyChwMaYXlEXc0HpfCKJXUX2wPczmXWAmTw"
place = "ChIJWzJ3pQRceUgRiWQgaRF5uvg"
halls = "ChIJRTc3mHymfkgRaaB81GAAGXU"

data = get_place_details_new(halls,key,fields_in)
print(data)