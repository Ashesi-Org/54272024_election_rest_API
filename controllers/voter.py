import json
import os

file_name = os.getcwd() + "/data/voters.txt"


def add_voter(voter):
    with open(file_name, 'r') as f:
        if os.stat(file_name).st_size == 0:
            data: dict = {
                'voters': []
            }
        else:
            data = json.load(f)

    for student in data['voters']:
        if student['student_id'] == voter['student_id']:
            return False
    data['voters'].append(voter)

    # Write the updated data back to the file
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

    return voter


def delete_voter_by_id(id:int):

    record: json = None
    with open(file_name, 'r+') as f:
        data: json = json.load(f)
        # Remove the voter with the given id from the data dictionary
        for voter in data['voters']:
            if 'student_id' in voter:
                if voter['student_id'] == id:
                    record = voter
                    data['voters'].remove(voter)
                    break
            else:
                return False, 400

        if not data['voters']:
            del data['voters']

        # Write the updated data back to the txt file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    if record:
        return True, record
    else:
        return False, 404



def update_voter_details(id: int, updated_voter:json):
    temp = None
    with open(file_name, 'r+') as f:
        data: json = json.load(f)
        for i, voter in enumerate(data['voters']):
            if voter['student_id'] == id:
                data['voters'][i] = updated_voter
                temp = updated_voter
                break
            # return False, {}

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    if not temp:
        return False, {}
    else:

        return True, updated_voter


def get_voter_by_id(id: int):
    # Load the data from the txt file
    with open(file_name, 'r') as f:
        data = json.load(f)

    for voter in data['voters']:
        if voter['student_id'] == id:
            return  True, voter

    return False, {}
