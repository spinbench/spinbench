import matplotlib.pyplot as plt
import os
import argparse
import sys
import numpy as np
import copy
import json
import glob

def compute_top_score(json_folder, output_folder=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    json_files = glob.glob(json_folder + "/*.json")
    result = {}
    top_index = {"best": 0, "others": 0}
    for game_file in json_files:
        game = json.load(open(game_file, "r"))
        model = game["player1_model"]["model"] if game["player1_model"]["model"] != "our_solver" else game["player2_model"]["model"]
        inspect = "player_1" if game["player1_model"]["model"] != "our_solver" else "player_2"
        if model not in result:
            result[model] = copy.deepcopy(top_index)
        game_log = game["game_log"]
        for log in game_log:
            if log["action"] is None:
                continue
            try:
                best_moves = log["best_moves"]
            except KeyError:
                print(type(log["action"]))
                print(log["action"])
                print(game_log.index(log), game_file, len(game_log))
                exit(0)

            if log["agent"] == inspect:
                if log["action"] in best_moves:
                    result[model]["best"] += 1
                else:
                    result[model]["others"] += 1
    for model in result:
        this_sum = sum(result[model].values())
        result[model]["best"] = result[model]["best"] / this_sum
        result[model]["others"] = result[model]["others"] / this_sum
    json.dump(result, open(os.path.join(output_folder, "tictactoe_best_move_percentage.json"), "w"), indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute top score from JSON files.")
    parser.add_argument('--json_folder', type=str, required=True, help='Path to the folder containing JSON files.')
    parser.add_argument('--output_folder', type=str, required=True, help='Path to save the json result and the figure.')
    args = parser.parse_args()
    json_folder = args.json_folder
    output_folder = args.output_folder
    compute_top_score(json_folder, output_folder)