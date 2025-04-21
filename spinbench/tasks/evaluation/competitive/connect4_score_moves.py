import json
import glob
import time
import argparse
from tqdm import tqdm
import requests

def fetch_scores_from_solver(pos_str):
    """
    Sends the current position string (pos_str) to connect4.gamesolver.org
    and returns the 'score' array from the JSON response.

    pos_str: a string of digits (each 1..7), e.g. '4012'
             representing the columns chosen so far, in 1-based indexing.
    """
    url = "http://localhost:5000/solve"
    full_url = f"{url}?pos={pos_str}"

    try:
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("score", [])
        else:
            print(f"Error fetching scores: {response.status_code} - {response.text}")
            time.sleep(10)
            return []
    except Exception as e:
        print(f"Error fetching scores: {e}")
        time.sleep(10)
        return []


def score_connect4_inplace(json_path):
    """
    Reads the given JSON file, iterates through 'game_log' moves,
    fetches solver scores for the *current* position (i.e. after the
    previous moves have been applied), and adds a 'score' array to each entry.

    Overwrites the original JSON file with the updated data.
    """
    # 1) Read the original JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # If there's no "game_log", do nothing
    game_log = data.get("game_log", [])

    if "score" in game_log[0]:
        print(f"Already scored the game in {json_path}")
        return data

    # 2) Build up pos_str as we go along:n.
    pos_str = ""

    for i, entry in enumerate(game_log, start=1):
        is_last_move = (i == len(game_log))

        # print(f"Processing move #{i}: {entry}")
        action = entry.get("action")
        if action is None:
            continue

        if not is_last_move:
            # Normal scoring for all but the last move
            col = action + 1
            # pos_str += str(col)
            solver_scores = fetch_scores_from_solver(pos_str)
            pos_str += str(col)
        else:
            # Force the last move's scores to be all -18
            solver_scores = [-18] * 7

        if not solver_scores:
            print(f"Error fetching scores for move #{i}, action={action}")
            break
        

        entry["score"] = solver_scores
        solver_scores_sorted = sorted(list(solver_scores), reverse=True)
        # Add the specific score of the action to the entry
        if 0 <= action < len(solver_scores):
            entry["action_score"] = solver_scores[action]
            entry["top_move_index"] = solver_scores_sorted.index(solver_scores[action])
        else:
            entry["action_score"] = None  # Handle invalid action index
            entry["top_move_index"] = None

    # 3) Overwrite the original JSON file
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch scores for Connect4 moves.")
    parser.add_argument('--json_folder', type=str, required=True, help='Path to the folder containing JSON files.')
    args = parser.parse_args()
    json_folder = args.json_folder
    json_files = glob.glob(f"{json_folder}/*.json")
    for json_path in tqdm(json_files):
        print(json_path)
        updated_data = score_connect4_inplace(json_path)
        # print("Scores in the updated game_log:")
        # for i, entry in enumerate(updated_data.get("game_log", [])):
        #     if "score" in entry:
        #         print(f" Move #{i}, action={entry['action']}, score={entry['score']}")