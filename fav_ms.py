from flask import Flask, request, jsonify
import json
import os

# create a new flask object
app = Flask(__name__)


# bind route to function
@app.route("/add_location", methods=["POST"])
def add_location():
    # get city and state from the request data
    city = request.json.get('city')
    state = request.json.get('state')

    # create a dictionary with the location data
    location = {'city': city, 'state': state}

    try:
        # read the contents of the file
        with open("locations.json", "r") as f:
            contents = f.read()
            if contents.strip():
                # the file is not empty, so load the JSON data
                places = json.loads(contents)
            else:
                # the file is empty, so create a new dictionary to store the data
                places = {'locations': []}
    except FileNotFoundError:
        # create a new dictionary to store the location data
        places = {'locations': []}

    # add the new location to the list
    places["locations"].append(location)

    # write the updated contents back to the file
    with open("locations.json", "w") as f:
        json.dump(places, f, indent=2)

    # return a success message to the client
    return f"Added {city}, {state} to the locations list.", 200


@app.route("/get_locations", methods=["GET"])
def get_locations():
    with open("locations.json", "r") as f:
        data = json.load(f)
        f.flush()
    # return the contents as JSON response
    return data


@app.route("/delete_location", methods=["DELETE"])
def delete_location():
    # get city and state from the request data
    data = request.json
    city, state = data.get("city"), data.get("state")

    # read the contents of the file
    with open("locations.json", "r") as f:
        places = json.load(f)
        f.close()

    # remove the specified location from the list by looping through the locations
    # and checking for a match - if item doesn't match, append to the list, thus removing
    # the city, state that we wanted to delete
    new_locations = []
    for place in places["locations"]:
        if place["city"] != city or place["state"] != state:
            new_locations.append(place)
    places["locations"] = new_locations

    # write the updated contents back to the file
    with open("locations.json", "w") as f:
        json.dump(places, f)
        f.flush()
    return f"Deleted {city}, {state} from the file. ", 200


@app.route('/clear_data', methods=['DELETE'])
def clear_data():
    # check if the file exists
    if not os.path.exists('locations.json'):
        return {'message': 'File does not exist.'}, 404

    # clear the file contents
    with open('locations.json', 'w') as f:
        # updated lines##
        places = {'locations': []}
        json.dump(places, f, indent=2)
        ##########
    return {'message': 'Data cleared successfully.'}, 200


# run function
if __name__ == "__main__":
    app.run(port=5000)
