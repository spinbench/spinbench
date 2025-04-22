import matplotlib.pyplot as plt
import numpy as np
import copy
import json
from matplotlib import cm
from matplotlib.colors import ListedColormap
import glob
import argparse

def compute_top_score(json_folder, figure_path=None):
    json_files = glob.glob(json_folder + "/*.json")
    d = {
        "white": 0,
        "black": 1,
    }
    # Plot settings
    plt.rcParams.update({
        'font.size': 12,  # Increase default font size
        'axes.titlesize': 14,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12
    })
    result = {

    }
    top_index = {
        # 0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        0: 0, # others
    }
    for game_file in json_files:
        game = json.load(open(game_file,"r"))
        model = game["player1_model"]["model"] if game["player1_model"]["model"] != "stockfish" else game["player2_model"]["model"]
        inspect = "white" if game["player1_model"]["model"] != "stockfish" else "black"
        if model not in result:
            result[model] = copy.deepcopy(top_index)
        game_log = game["game_log"]
        for log in game_log:
            if log["agent"] == inspect:
                if log["top_move_index"] == -1:
                    result[model][0] += 1
                    continue
                for k in result[model].keys():
                    if k >= log["top_move_index"]+1:
                        result[model][k] += 1
                # result[model][log["top_move_index"]+1] += 1


    for model in result:
        this_sum = sum(result[model].values())
        this_sum = result[model][10] + result[model][0]
        for i in range(0,11):
            result[model][i] = result[model][i]/this_sum
        print(model)
        print(result[model][0])

    # Adjusting bar width and layout for eight models
    models = list(result.keys())
    indices = np.arange(0, 6)
    width = 0.08  # Narrower bar width for more models
    colors = plt.cm.tab20.colors  # Use a colormap to get more distinct colors
    custom_colors = {
        "o1": "#F38181",
        "o1-mini": "#46CDCF",
        "GPT-4o": "#95E1D3"
    }

    print(result)

    if not figure_path:
        return

    # Only print the first 6

    # Plot bars for each model
    plt.figure(figsize=(8, 4))

    for i, model in enumerate(models):
        # Rearrange the values to place '0' (renamed "others") at the end
        values = [result[model][index] for index in range(1, 7)]  # Exclude '0'
        print(model)
        color = custom_colors.get(model, plt.cm.tab20.colors[i % len(plt.cm.tab20.colors)])
        print(color)
        # others = result[model].get(0, 0)  # Get value for '0', default to 0 if not present
        # values.append(others)  # Add 'others' at the end
        plt.bar(indices + i * width - (width * len(models) / 2), values, width, label=model, color=color)

    # Add labels, title, and legend
    plt.xlabel("Top Move Index")
    plt.ylabel("Normalized Frequency")
    plt.title("Comparison of Top Move Indices Across Models", fontsize=16,pad=80)
    plt.xticks(indices, [str(i) for i in range(1, 7)])  # Change last label to 'others'
    # plt.legend(title="Models", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.legend(title="Models", loc='lower center',bbox_to_anchor=(0.5, 1.02), fontsize=10, ncol=3)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adjust layout to accommodate legend
    plt.tight_layout()
    plt.savefig(figure_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot top moves.")
    parser.add_argument('--json_folder', type=str, required=True, help='Path to the folder containing JSON files.')
    parser.add_argument('--figure_path', type=str, default=None, help='Path to save the figure.')
    args = parser.parse_args()
    json_folder = args.json_folder
    figure_path = args.figure_path
    compute_top_score(json_folder, figure_path)