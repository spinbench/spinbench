from tqdm import tqdm
import argparse
from stockfish import Stockfish
import json
import glob

def score_moves(stockfish_path, json_folder):
	stockfish = Stockfish(stockfish_path)
	stockfish.set_skill_level(20)
	stockfish.update_engine_parameters({
		"Threads": 8,       
		"Skill Level": 20,
		"Move Overhead": 10,
		"Hash": 2048,
	})
	json_files = glob.glob(f"{json_folder}/*.json")
	for game_file in tqdm(json_files):
		if "o1" not in game_file:
			continue
		game = json.load(open(game_file,"r"))
		game_log = game["game_log"]
		for log in game_log:
			stockfish.set_fen_position(log["board"])
			top_moves = stockfish.get_top_moves(10)
			top_moves = [i["Move"] for i in top_moves]
			try:
				top_move_index = top_moves.index(log["action"])
			except:
				top_move_index = -1
			log["top_moves"] = top_moves
			log["top_move_index"] = top_move_index
		game["game_log"] = game_log
		json.dump(game, open(game_file,"w"), indent=2,ensure_ascii=False)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Score moves using Stockfish.")
	parser.add_argument('--stockfish_path', type=str, required=True, help='Path to the Stockfish binary.')
	parser.add_argument('--json_folder', type=str, required=True, help='Path to the folder containing JSON files.')
	args = parser.parse_args()
	stockfish_path = args.stockfish_path
	json_folder = args.json_folder
	score_moves(stockfish_path, json_folder)
	print("Scoring completed.")