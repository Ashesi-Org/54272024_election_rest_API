import os
import json

file_name = os.getcwd() + "/data/elections.txt"



def add_election(election:json):
    with open(file_name, 'r') as f:
        if os.stat(file_name).st_size == 0:
            data: dict = {
                'elections': []
            }
        elif os.stat(file_name).st_size != 0:
            data = json.load(f)
    for ele in data['elections']:
        if ele['election_id'] == election['election_id']:
            return False, {}
    data['elections'].append(election)

    # Write the updated data back to the file
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

    return True, election


def get_election_by_id(id: int):

    # Load the data from the txt file
    with open(file_name, 'r') as f:
        data:json = json.load(f)

    for election in data['elections']:
        if election['election_id'] == id:
            return  True, election

    return False, {}


def remove_election_by_id(id: int):
    record: json = None
    with open(file_name, 'r+') as f:
        data: json = json.load(f)
        # Remove the voter with the given id from the data dictionary
        for election in data['elections']:
            if 'election_id' in election:
                if election['election_id'] == id:
                    record = election
                    data['elections'].remove(election)
                    break
            else:
                return False, 400

        if not data['elections']:
            del data['elections']

        # Write the updated data back to the txt file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    if record:
        return True, record
    else:
        return False, 404



