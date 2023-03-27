import os
import json

elections_data = os.getcwd() + "/data/elections.txt"
voters_data = os.getcwd() + "/data/voters.txt"
ballots_data = os.getcwd() + "/data/ballots.txt"
candidates_data = os.getcwd() + "/data/candidates.txt"


def add_vote(ballot:json):

    with open(voters_data, 'r') as f:
        v_data = json.load(f)

    with open(candidates_data, 'r') as f1:
        c_data = json.load(f1)


    with open(elections_data, 'r') as f2:
        e_data = json.load(f2)

    with open(ballots_data, 'r') as f3:
        if os.stat(ballots_data).st_size == 0:
            b_data: dict = {
                'ballots': []
            }
        elif os.stat(ballots_data).st_size != 0:
            b_data = json.load(f3)

    # Check if the voter exists
    voter_exists: bool = False
    for voter in v_data['voters']:
        if voter['student_id'] == ballot['student_id']:
            voter_exists = True
            break
    if not voter_exists:
        return False, "not_voter"

    # Check if the election exists
    election_exists: bool = False
    for election in e_data['elections']:
        if election['election_id'] == ballot['election_id']:
            election_exists = True
            break
    if not election_exists:
        return False, "not_election"

    # Check if the candidate exists
    candidate_exists: bool = False
    for candidate in c_data['candidates']:
        if candidate['candidate_id'] == ballot['candidate_id']:
            candidate_exists = True
            candidate['vote_for'] += 1  # increase candidate's vote count
            break
    if not candidate_exists:
        return False, "not_candidate"

    # Check if the voter has already voted in this election
    for existing_vote in b_data['ballots']:
        if existing_vote['student_id'] == ballot['student_id'] and existing_vote['election_id'] == ballot['election_id']:
            return False, 'voted'

    # Record the vote
    b_data['ballots'].append(ballot)

    # Write the updated data back to the file
    with open(ballots_data, 'w') as f:
        json.dump(b_data, f, indent=4)

    return True, ballot


