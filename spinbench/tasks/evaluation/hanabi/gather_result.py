import json
import os
import argparse

def compute_result(store_folder, result_name, total_rounds=5, output_file="results/hanabi_results.json"):
    if not os.path.exists(store_folder):
        raise FileNotFoundError(f"Store folder {store_folder} does not exist.")
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    total_token_used = 0
    reward = 0
    counted_games = 0
    for idx in range(total_rounds):
        filename = f"{result_name}_{idx}.json"
        if not os.path.exists(f"{store_folder}/{filename}"):
            print(f"File {filename} does not exist, skipping.")
            continue
        counted_games += 1
        with open(f"{store_folder}/{filename}", "r") as f:
            data = json.load(f)
            try:
                total_token_used += data["total_token_used"]
            except KeyError:
                print(f"Key 'total_token_used' not found in {filename}.")
            print(f"File {filename} loaded successfully.")
            game_log = data["game_log"]
            if len(game_log) > 0:
                reward += game_log[-1][-1][0]

    if counted_games == 0:
        print("No games counted, exiting.")
        return
    
    print("Results:")
    print("result name: ", result_name)
    print("Total games counted: ", counted_games)
    print("Total token used: ", total_token_used)
    print("Average reward: ", reward / counted_games)
    json.dump(
        {
            "result_name": result_name,
            "total_games_counted": counted_games,
            "total_token_used": total_token_used,
            "average_reward": reward / counted_games
        },
        open(output_file, "w"),
        indent=2
    )
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gather results from multiple rounds of Hanabi games.")
    parser.add_argument("--store_folder", type=str, required=True, help="Folder to store the results.")
    parser.add_argument("--result_name", type=str, required=True, help="Name of the result files.")
    parser.add_argument("--total_rounds", type=int, default=5, help="Total number of rounds to compute results for.")
    parser.add_argument("--output_file", type=str, default="results/hanabi_results.json", help="Output filename for results.")
    args = parser.parse_args()

    compute_result(args.store_folder, args.result_name, args.total_rounds, args.output_file)