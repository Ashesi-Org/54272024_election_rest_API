import json
from flask import Flask, request, jsonify
from controllers.ballot import add_vote
from controllers.candidate import register_candidate
from controllers.election import add_election, get_election_by_id, remove_election_by_id
from controllers.voter import add_voter, delete_voter_by_id, get_voter_by_id, update_voter_details

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1> This is the campus voting platform API</h1>"


@app.route('/register', methods=['POST'])
def register_voter():
    
    voter: json = request.get_json()

    added_voter = add_voter(voter)
    if added_voter == False:
        return jsonify({'message': "This voter already exist", 'status': 'error'}), 400

    return jsonify({"message": "Voter registered successfully", "status": "success", "data": added_voter}), 200


@app.route('/remove_voter/<int:id>', methods=['DELETE'])
def remove_voter(id: int):
    delete_voter = delete_voter_by_id(id)
    if delete_voter[0]:
        return jsonify({'message': 'Voter deleted successfully', 'status': 'success'}), 200

    elif delete_voter[0] == False and delete_voter[1] == 400:
        return jsonify({'message': "The 'student_id' key doesn't exist in the dictionary.", 'status': 'error'}), 400
    else:
        return jsonify({'message': 'Voter with that id does not exist', 'status': 'not found'}), 404


@app.route('/update_voter/<int:id>', methods=['PUT'])
def update_voter(id: int):
    voter: json = request.get_json()
    updated_voter = update_voter_details(id, voter)

    if updated_voter[0]:
        return jsonify({"message": "Voter updated successfully", "status": "success", "data": updated_voter[1]}), 200

    else:
        return jsonify({"message": "No student with the given id exist", "status": "error"}), 404


@app.route('/get_voter/<int:id>', methods=['GET'])
def get_voter(id: int):
    voter = get_voter_by_id(id)
    if voter[0]:
        return jsonify({"message": "successfull", "status": "success", "data": voter[1]}), 200

    return jsonify({"message": "No voter with that id exist", "status": "Not found error"}), 404


@app.route('/create_election', methods=['POST'])
def create_election():
    election: json = request.get_json()
    created_election = add_election(election)

    if not created_election[0]:
        return jsonify({"message": "an election with the same id exists", "status": "error"}), 409
    else:

        return jsonify({"message": "Election created successfully", "status": "success", "data": created_election[1]}), 201


@app.route('/get_election/<int:id>', methods=['GET'])
def get_election(id: int):

    election = get_election_by_id(id)
    if election[0]:
        return jsonify({"message": "successfull", "status": "success", "data": election}), 200
    else:
        return jsonify({"message": "No voter with that id exist", "status": "error"}), 404


@app.route('/delete_election/<int:id>', methods=['DELETE'])
def remove_election(id: int):

    delete_election = remove_election_by_id(id)
    if delete_election[0]:
        return jsonify({'message': 'Election deleted successfully', 'status': 'success'}), 200

    elif delete_election[0] == False and delete_election[1] == 400:
        return jsonify({'message': "The 'election_id' key doesn't exist in the dictionary.", 'status': 'error'}), 400
    else:
        return jsonify({'message': 'Election with that id does not exist', 'status': 'not found'}), 404


@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    candidate: json = request.get_json()
    created_candidate = register_candidate(candidate)

    if not created_candidate[0]:
        return jsonify({"message": "candidate already exist", "status": "error"}),400 
    else:

        return jsonify({"message": "Candite created successfully", "status": "success", "data": created_candidate[1]}), 201

    

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    ballot: json = request.get_json()
    casted_ballot = add_vote(ballot)

    if casted_ballot[0]:
        return jsonify({"message": "Vote cast successfully", "status": "success", "data": ballot}), 201
    
    elif not casted_ballot[0] and casted_ballot[1] == "not_voter":
        return jsonify({"message": "Voter not found", "status": "error"}), 404

    elif not casted_ballot[0] and casted_ballot[1] == "not_election":
        return jsonify({"message": "Election not found", "status": "error"}), 404
    
    elif not casted_ballot[0] and casted_ballot[1] == "not_candidate":
        return jsonify({"message": "Candidate not found", "status": "error"}), 404

    elif not casted_ballot[0] and casted_ballot[1] == "voted":
        return jsonify({"message": "Voter has already voted in this election", "status": "error"}), 409



if __name__ == '__main__':
    app.run(port=5000, debug=True)
