import os
import json
import sys
from collections import defaultdict
import argparse

def process_directory_for_solver_winrate(dir_path, output_filename="our_solver_winrate.json"):
    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a directory.")
        return

    stats = defaultdict(lambda: {"wins": 0, "draw":0, "total": 0})

    for filename in os.listdir(dir_path):
        if filename.lower().endswith(".json"):
            full_path = os.path.join(dir_path, filename)

            try:
                with open(full_path, "r") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Skipping file {full_path} due to JSON error: {e}")
                continue

            p1_model = data.get("player1_model", {}).get("model", "")
            p2_model = data.get("player2_model", {}).get("model", "")
            winner = data.get("winner", "")

            if p1_model == "our_solver":
                our_solver_is_player1 = True
                opponent_model = p2_model
            elif p2_model == "our_solver":
                our_solver_is_player1 = False
                opponent_model = p1_model
            else:
                continue

            matchup_key = f"Solver vs {opponent_model}"

            stats[matchup_key]["total"] += 1

            if our_solver_is_player1 and winner == "Player 1":
                stats[matchup_key]["wins"] += 1
            elif (not our_solver_is_player1) and winner == "Player 2":
                stats[matchup_key]["wins"] += 1
            elif winner == "Draw":
                stats[matchup_key]["draw"] += 1

    results = {}
    for matchup, record in stats.items():
        wins = record["wins"]
        total = record["total"]
        draw = record["draw"]
        win_rate = (wins / total * 100.0) if total > 0 else 0.0
        results[matchup] = {
            "wins": wins,
            "draws": draw,
            "total": total,
            "win_rate": win_rate
        }

    output_path = os.path.join(dir_path, output_filename)
    try:
        with open(output_path, "w") as out_f:
            json.dump(results, out_f, indent=2)
        print(f"[INFO] Wrote our_solver winrate results to: {output_path}")
    except Exception as e:
        print(f"Error writing to {output_path}: {e}")
        return

    print("Win Rate Summary:")
    for matchup, info in results.items():
        print(f"{matchup}: {info['wins']}/{info['total']} wins = {info['win_rate']:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON files for our_solver winrate.")
    parser.add_argument("--directory", type=str, required=True, help="Directory containing JSON files.")
    args = parser.parse_args()
    input_path = args.directory
    process_directory_for_solver_winrate(input_path)
