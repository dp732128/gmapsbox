import requests
import Maps_Functions as MF
import csv

fields_in = "name,formatted_address,post_code,county,geometry,place_id"
def get_place_details_new(place_id, api_key,fields_in):
    '''
    
    Get the place details of a location from google

    Arguments:
    place_id -- The place id for a place on google
    api_key -- Key used to allow access to Google api
    fields_in -- Fields to be requested from the google places api


    Returns:

    A dictionary containing various fields and their value. Example: {'name':'Happy shop','address':'Happy street, new york', etc ...}
    
    '''

    #Takes the fields_in. Splits it and creates a valid field query to put into the google places api request. 
    #Reason for this in an example: Both Post Code and County come from the address components, so cant call the field address_components in fields as could mean either
    fields_split = fields_in.split(",")
    print(fields_split)

    fields_out = []
    for field in fields_split:
        if(field == "place_id"):
            1+1
        elif(field != "county" and field != "post_code"):
            fields_out.append(field)
        else:
            fields_out.append("address_components")
    print(fields_out)
    fields_set = set(fields_out)
    print(fields_set)
    fields_out_str = ','.join(fields_set)
    print(fields_out_str)




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
        place_details["formatted_address"] = result.get("formatted_address")
    if("post_code" in fields_split):
            for address_component in response["result"]["address_components"]:
                if('postal_code' in address_component['types']):
                    place_details["post_code"] = address_component["long_name"]
    if('website' in fields_split):
        place_details["website"] = result.get("website")
    if("phone" in fields_split):
         place_details["phone number"] = result.get("formatted_phone_number")
    if("county" in fields_split):
        for address_component in response["result"]["address_components"]:
            if('administrative_area_level_2' in address_component['types']):
                place_details["county"] = address_component["long_name"]
    if("geometry" in fields_split):
        for component in response["result"]["geometry"]:
            if('location') in component:
                place_details["lat"] = response["result"]["geometry"]["location"]["lat"]
                place_details["lng"] = response["result"]["geometry"]["location"]["lng"]
    if("reviews" in fields_split):
        place_details["reviews"] = result.get("reviews")




    if("place_id" in fields_split):
        place_details["place id"] = place_id
    
    

        
        


    #Continue from hereeeee
    
    
    print(place_details)



    #Return place details including county details
    return place_details

def write_to_csv_new(file_name, details_list,fields):
    '''

    Takes a list of location details and converts to csv format then writes to location

    Arguments:

    file_name -- name to be given to file when created
    details_list -- the list of places and their details to be turned into the csv

    Returns:

    Nothing ***To Change. Either have it return a file or a error code value to indicate success.*** 
    
    
    '''
    with open(file_name, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in details_list:
            writer.writerow(row)

key = "AIzaSyChwMaYXlEXc0HpfCKJXUX2wPczmXWAmTw"
place = "ChIJWzJ3pQRceUgRiWQgaRF5uvg"
halls = "ChIJRTc3mHymfkgRaaB81GAAGXU"


data = get_place_details_new(halls,key,fields_in)
all_details = []
all_details.append(data)
data = get_place_details_new(place,key,fields_in)
all_details.append(data)

fieldnames = all_details[0]
print(fieldnames)
write_to_csv_new("test.csv",all_details,fieldnames)

print(data)
print(all_details)