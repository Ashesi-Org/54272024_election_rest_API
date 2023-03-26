from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# A dictionary to store the data // Find info in schema.txt
data:dict = {
    'voters': [],
    'elections': [],
    'candidates':[],
    'ballots':[]
}

@app.route('/')
def index():
    return "hello world"

@app.route('/register', methods=['POST'])
def register():

    voter:json = request.get_json()
    with open('data.txt', 'r') as f:
        data = json.load(f)
    data['voters'].append(voter)

    # Write the updated data back to the file
    with open('data.txt', 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"message": "Voter registered successfully", "status": "success", "data":voter}), 200




@app.route('/remove_voter/<int:id>', methods=['DELETE'])
def de_register(id:int):

    with open('data.txt', 'r+') as f:
        data:json = json.load(f)
        # Remove the voter with the given id from the data dictionary
        record:json = None
        for voter in data['voters']:
            if 'voter_id' in voter:
                if voter['voter_id'] == id:
                    record = voter
                    data['voters'].remove(voter)
                    break
            else:
                return jsonify({'message': "The 'voter_id' key doesn't exist in the dictionary.", 'status': 'error'})

        if not data['voters']:
            del data['voters']

        # Write the updated data back to the txt file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    if record:
        return jsonify({'message': 'Election deleted successfully', 'status': 'success', 'data': record}), 200
    else:
        return jsonify({'message': 'Election with that id does not exist', 'status': 'not found'}), 404



@app.route('/update_voter/<int:id>', methods=['PUT'])
def update(id:int):
    with open('data.txt', 'r+') as f:
        data:json = json.load(f)
        updated_voter:json = request.get_json()


        for i, voter in enumerate(data['voters']):
            if 'voter_id' in voter:
                if voter['voter_id'] == id:
                    data['voters'][i] = updated_voter
                    break
            else:
                return jsonify({"message": "The 'voter_id' key doesn't exist in the dictionary.", "status": "error"}), 400

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    return jsonify({"message": "Voter updated successfully", "status": "success", "data":updated_voter}), 200


@app.route('/get_voter_by_id/<int:id>', methods=['GET'])
def get_voter(id:int):
        # Load the data from the txt file
    with open('data.txt', 'r') as f:
        data = json.load(f)

    for voter in data['voters']:
        if voter['voter_id'] == id:
            return jsonify({"message": "successfull", "status": "success", "data": voter}), 200
        
    return jsonify({"message": "No voter with that id exist", "status": "Not found error"}), 404


@app.route('/get_allvoters', methods=['GET'])
def get_allvoters():
    # Load the data from the txt file
    with open('data.txt', 'r') as f:
        data:json = json.load(f)

    if len(data['voters']) != 0:
        return json.dumps(data['voters'])
    return jsonify({"message": "No voters found", "status": "completed"}), 202


@app.route('/create_election', methods=['POST'])
def create_election():
    election:json = request.get_json()
    # Loading the existing data from the file
    with open('data.txt', 'r') as f:
        data:json = json.load(f)
    data['elections'].append(election)

    # Write the updated data back to the file
    with open('data.txt', 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"message": "Election created successfully", "status": "success", "data":election}), 200


@app.route('/get_election/<int:id>', methods = ['GET'])
def get_election(id:int):

     # Load the data from the txt file
    with open('data.txt', 'r') as f:
        data = json.load(f)

    for election in data['elections']:
        if election['election_id'] == id:
            return jsonify({"message": "successfull", "status": "success", "data": election}), 200
        
    return jsonify({"message": "No voter with that id exist", "status": "error"}), 404


@app.route('/delete_election/<int:id>', methods=['DELETE'])
def remove_election(id:int):

    with open('data.txt', 'r+') as f:
        data:json = json.load(f)
        # Remove the voter with the given id from the data dictionary
        record:json = None
        for election in data['election']:
            if 'voter_id' in election:
                if election['voter_id'] == id:
                    record = election
                    data['voters'].remove(election)
                    break
            else:
                return jsonify({'message': "The 'voter_id' key doesn't exist in the dictionary.", 'status': 'error'}), 400

        if not data['election']:
            del data['election']

        # Write the updated data back to the txt file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    if record:
        return jsonify({'message': 'Election deleted successfully', 'status': 'success', 'data': record}), 200
    else:
        return jsonify({'message': 'Election with that id does not exist', 'status': 'not found'}), 404






@app.route('/cast_vote/<int:id>', methods=['POST'])
def cast_vote(id:int):
   return



if __name__ == '__main__':
    app.run(debug = True)