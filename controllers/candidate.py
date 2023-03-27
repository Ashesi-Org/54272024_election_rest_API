import os
import json


file_name = os.getcwd() + "/data/candidates.txt"

def register_candidate(candidate:json):
    with open(file_name, 'r') as f:
        if os.stat(file_name).st_size == 0:
            data: dict = {
                'candidates': []
            }
        elif os.stat(file_name).st_size != 0:
            data = json.load(f)
    for student in data['candidates']:
        if student['candidate_id'] == candidate['candidate_id']:
            return False, {}
    data['candidates'].append(candidate)

    # Write the updated data back to the file
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

    return True, candidate
