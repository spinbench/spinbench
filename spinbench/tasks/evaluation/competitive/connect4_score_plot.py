import matplotlib.pyplot as plt
import os
import argparse
import sys
import numpy as np
import copy
import json
import glob

def compute_top_score(json_folder, output_folder=None):
    # Load JSON files
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    json_files = glob.glob(json_folder + "/*.json")
    result = {}
    top_index = {i: 0 for i in range(1, 8)} # first 4

    for game_file in json_files:
        if "winrate" in game_file:
            continue
        game = json.load(open(game_file, "r"))
        model = game["player1_model"]["model"] if game["player1_model"]["model"] != "our_solver" else game["player2_model"]["model"]
        inspect = "player_0" if game["player1_model"]["model"] != "our_solver" else "player_1"
        if model not in result:
            result[model] = copy.deepcopy(top_index)
        game_log = game["game_log"]
        for log in game_log:
            if log["agent"] == inspect:
                for k in result[model].keys():
                    if k >= log["top_move_index"] + 1:
                        result[model][k] += 1
                # result[model][log["top_move_index"] + 1] += 1

    for model in result:
        this_sum = sum(result[model].values())
        this_sum = result[model][7]
        for i in range(1, 8):
            result[model][i] = result[model][i] / this_sum
    json.dump(result, open(os.path.join(output_folder, "connect4_top_move_percentage.json"), "w"), indent=2)

    # Plot settings
    plt.rcParams.update({
        'font.size': 12,  # Increase default font size
        'axes.titlesize': 14,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12
    })

    # order the result keys inside the dictionary
    result = dict(sorted(result.items()))
    models = list(result.keys())
    indices = np.arange(1, 5)  # X-axis positions
    width = 0.06  # Narrower bar width for more compactness
    colors = plt.cm.tab20.colors  # Use a colormap for distinct colors
    custom_colors = {
        "o1": "#F38181",
        "o1-mini": "#46CDCF",
        "GPT-4o": "#95E1D3"
    }

    plt.figure(figsize=(8, 4))  # Smaller figure size

    for i, model in enumerate(models):
        values = [result[model].get(index, 0) for index in range(1, 5)]
        color = custom_colors.get(model, plt.cm.tab20.colors[i % len(plt.cm.tab20.colors)])
        plt.bar(indices + i * width - (width * len(models) / 2), values, width, label=model, color=color)

    plt.xlabel("Top Move Index", fontsize=14)
    plt.ylabel("Normalized Frequency", fontsize=14)
    plt.title("Comparison of Top Move Indices Across Models", fontsize=16,pad=68)
    plt.xticks(indices, [str(i) for i in range(1, 5)])
    # plt.legend(title="Models", loc='upper right', fontsize=10, ncol=3)  # Compact legend
    plt.legend(
        title="Models",
        loc='lower center',  # Position legend at the bottom-center of bbox
        bbox_to_anchor=(0.5, 1.02),  # Adjust the position above the plot
        fontsize=8,
        ncol=5  # Number of columns in the legend
    )
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "connect4_top_move_percentage.pdf"), dpi=300)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute top score from JSON files.")
    parser.add_argument('--json_folder', type=str, required=True, help='Path to the folder containing JSON files.')
    parser.add_argument('--output_folder', type=str, required=True, help='Path to save the figure.')
    args = parser.parse_args()
    json_folder = args.json_folder
    output_folder = args.output_folder
    compute_top_score(json_folder, output_folder)