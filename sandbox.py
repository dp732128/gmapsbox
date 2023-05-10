import Maps_Functions as MP
import math

def split_bounds_exact(north, south, east, west, box_side_length_km):
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
    lat_cutoffs = int((north - south)/box_lat)
    lng_cutoffs = int((east - west)/box_lng)

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

def all_exact(north, south, east, west, box_side_length_km, search, api_key):
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
    boxes = split_bounds_exact(north, south, east, west, box_side_length_km)
    print(boxes)


    location_list = [(box[-2], box[-1]) for box in boxes]
    #For each box
    for box in boxes:


        # Calculate the radius in meters
        radius = box_side_length_km/(2 * math.sin(math.radians(45))) * 1000

        #Get place_ids for one box search
        one_location_place_ids = MP.get_place_ids_one_location(api_key, box[-2], box[-1], radius, search)
        print("results 1 box:")
        print(len(one_location_place_ids))

        #If 60 results come back, ae: the return results was capped out by the google api
        if len(one_location_place_ids) > 59:
            # Recursively call the function for smaller boxes
            recursive_results = all_exact(box[0], box[1], box[2], box[3], (box_side_length_km/2), search, api_key)

            #Add each result from the recursive call to the list
            for result in recursive_results:
                all_place_ids.append(result)
        else:
            # Append the place IDs of the current box
            for location in one_location_place_ids:
                all_place_ids.append(location)

    #Remove duplicate locations
    all_place_ids = MP.remove_duplicates(all_place_ids)

    #return list of place ids
    return all_place_ids

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
    boxes = MP.split_bounds(north, south, east, west, box_side_length_km)
    print(boxes)


    location_list = [(box[-2], box[-1]) for box in boxes]
    #For each box
    for box in boxes:


        # Calculate the radius in meters
        radius = box_side_length_km/(2 * math.sin(math.radians(45))) * 1000

        #Get place_ids for one box search
        one_location_place_ids = MP.get_place_ids_one_location(api_key, box[-2], box[-1], radius, search)
        print("results 1 box:")
        print(len(one_location_place_ids))

        #If 60 results come back, ae: the return results was capped out by the google api
        if len(one_location_place_ids) > 59:
            # Recursively call the function for smaller boxes
            recursive_results = all_exact(box[0], box[1], box[2], box[3], (box_side_length_km/2), search, api_key)

            #Add each result from the recursive call to the list
            for result in recursive_results:
                all_place_ids.append(result)
        else:
            # Append the place IDs of the current box
            for location in one_location_place_ids:
                all_place_ids.append(location)

    #Remove duplicate locations
    all_place_ids = MP.remove_duplicates(all_place_ids)

    #return list of place ids
    return all_place_ids
all(54.1,54,-1.9,-2,20,"Food","AIzaSyChwMaYXlEXc0HpfCKJXUX2wPczmXWAmTw")