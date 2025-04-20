import json
import argparse
from tqdm import tqdm
import os
import random

def old_parse_observation(observation_dict, agent):
	# Extract the observation planes and the action mask from the observation dictionary
	observation = observation_dict['observation']  # 3x3x2 array
	action_mask = observation_dict['action_mask']  # Legal action mask

	# Initialize variables to store the board and the agent's mark
	board = [['' for _ in range(3)] for _ in range(3)]
	if agent == 'player_1':
		player_mark = 'X'
		opponent_mark = 'O'
	else:
		player_mark = 'O'
		opponent_mark = 'X'

	# Parse the board from the observation
	for row in range(3):
		for col in range(3):
			if observation[row][col][0] == 1:
				board[row][col] = player_mark
			elif observation[row][col][1] == 1:
				board[row][col] = opponent_mark
			else:
				board[row][col] = ' '

	# Convert the board into a text description
	board_description = "\n".join(
		[f"{board[0][0]} | {board[1][0]} | {board[2][0]}\n---------\n"
		 f"{board[0][1]} | {board[1][1]} | {board[2][1]}\n---------\n"
		 f"{board[0][2]} | {board[1][2]} | {board[2][2]}"]
	)

	# Convert the action mask into text description of legal actions
	legal_moves = [i for i, is_legal in enumerate(action_mask) if is_legal == 1]
	legal_moves_list = legal_moves.copy()
	legal_moves_description = f"Legal moves: {', '.join(map(str, legal_moves))}" if legal_moves else "No legal moves available."

	# Create the final description
	description = f"Current player: {agent} ({player_mark})\n" \
				  f"Opponent: {'player_2' if agent == 'player_1' else 'player_1'} ({opponent_mark})\n" \
				  f"Board state:\n{board_description}\n" \
				  f"{legal_moves_description}"
	
	return f"Board state:\n{board_description}\n", f"{legal_moves_description}\n", legal_moves_list


def parse_observation(observation_dict, agent):
	"""
	Returns:
	  board_2d (list of lists) - 3x3 board with ' ', 'X', or 'O'
	  legal_moves (list of int) - same as legal_moves_list
	  legal_moves_list (list of int) - identical to legal_moves, or a copy
	"""
	# 1. Grab the observation planes and action mask
	observation = observation_dict['observation']  # shape: (3,3,2)
	action_mask = observation_dict['action_mask']  # shape: (9,)

	# 2. Initialize a 3x3 board of spaces
	board_2d = [[' ' for _ in range(3)] for _ in range(3)]

	# Determine which mark belongs to the agent vs. opponent
	if agent == 'player_1':
		player_mark = 'X'
		opponent_mark = 'O'
	else:
		player_mark = 'O'
		opponent_mark = 'X'

	# 3. Fill board_2d by checking which plane is 1
	for row in range(3):
		for col in range(3):
			if observation[row][col][0] == 1:
				board_2d[row][col] = player_mark
			elif observation[row][col][1] == 1:
				board_2d[row][col] = opponent_mark
			else:
				board_2d[row][col] = ' '

	# 4. Extract legal moves from the action mask
	#    (These are the indices 0..8 of the board that are allowed)
	legal_moves = [i for i, is_legal in enumerate(action_mask) if is_legal == 1]

	# If you truly need both "legal_moves" and "legal_moves_list", 
	# you can duplicate them or set them to the same reference:
	legal_moves_list = legal_moves[:]  # or the same reference

	# 5. Return them (no strings involved)
	return board_2d, legal_moves, legal_moves_list


def is_board_full(board_2d):
	"""
	Returns True if the board has no empty cells, False otherwise.
	"""
	for row in range(3):
		for col in range(3):
			if board_2d[row][col] == ' ':
				return False
	return True

def detectWin(board_2d, player_mark):
	"""
	Checks if player_mark ('X' or 'O') has won on board_2d.
	"""
	# Check rows
	for row in range(3):
		if all(cell == player_mark for cell in board_2d[row]):
			return True
	# Check columns
	for col in range(3):
		if all(board_2d[row][col] == player_mark for row in range(3)):
			return True
	# Check diagonals
	if all(board_2d[i][i] == player_mark for i in range(3)):
		return True
	if all(board_2d[i][2 - i] == player_mark for i in range(3)):
		return True
	return False

def minimax(board_2d, is_maximizing):
	"""
	A standard minimax that returns:
	  +1 if from this board state, the 'X' player can force a win,
	  -1 if 'O' can force a win,
	   0 otherwise (draw).
	
	is_maximizing (bool): True if the current player to move is 'X';
						  False if the current player is 'O'.
	"""
	# Terminal checks
	if detectWin(board_2d, 'X'):
		return +1
	if detectWin(board_2d, 'O'):
		return -1
	if is_board_full(board_2d):
		return 0  # Draw

	# If it's X's turn => maximize
	if is_maximizing:
		best_score = -float('inf')
		move_score = {}
		for move_idx in getLegalMoves(board_2d):
			r, c = divmod(move_idx, 3)
			board_2d[r][c] = 'X'
			score = minimax(board_2d, False)  # Now 'O' will move
			board_2d[r][c] = ' '
			best_score = max(best_score, score)
		return best_score
	# If it's O's turn => minimize
	else:
		best_score = float('inf')
		for move_idx in getLegalMoves(board_2d):
			r, c = divmod(move_idx, 3)
			board_2d[r][c] = 'O'
			score = minimax(board_2d, True)   # Now 'X' will move
			board_2d[r][c] = ' '
			best_score = min(best_score, score)
		return best_score


def getLegalMoves(board_array):
	legal_moves = []
	for row in range(3):
		for col in range(3):
			if board_array[row][col] == ' ':
				move_idx = row * 3 + col  # Mapping (row, col) to index
				legal_moves.append(move_idx)
	return legal_moves

def find_best_move_for_x(board_2d):
	"""
	Returns the best move index (0..8) for 'X' from the current position,
	or None if no legal moves.
	"""
	legal_moves = getLegalMoves(board_2d)
	if not legal_moves:
		return None
	
	best_val = -float('inf')
	best_move = None
	best_moves = []
	move_scores = {}
	for move_idx in legal_moves:
		r, c = divmod(move_idx, 3)
		board_2d[r][c] = 'X'
		val = minimax(board_2d, is_maximizing=False)  # Next turn: O
		board_2d[r][c] = ' '
		move_scores[move_idx] = val
		if val > best_val:
			best_val = val
			best_moves = [move_idx]
		elif val == best_val:
			best_moves.append(move_idx)
	random.shuffle(best_moves)
	best_move = best_moves[0] if best_moves else None
	return best_move, move_scores, best_moves, best_val

def find_best_move_for_o(board_2d):
	"""
	Returns the best move index (0..8) for 'O' from the current position,
	or None if no legal moves.
	"""
	legal_moves = getLegalMoves(board_2d)
	if not legal_moves:
		return None
	
	best_val = float('inf')
	best_move = None
	best_moves = []
	move_scores = {}
	
	for move_idx in legal_moves:
		r, c = divmod(move_idx, 3)
		board_2d[r][c] = 'O'
		val = minimax(board_2d, is_maximizing=True)  # Next turn: X
		board_2d[r][c] = ' '
		move_scores[move_idx] = val
		if val < best_val:
			best_val = val
			best_moves = [move_idx]
		elif val == best_val:
			best_moves.append(move_idx)
	random.shuffle(best_moves)
	best_move = best_moves[0] if best_moves else None
	return best_move, move_scores, best_moves, best_val

def score_game_log_inplace(json_path):
	"""
	Reads the given JSON file, updates each valid move in the game_log with
	an extra 'score' field, then writes it back to the *same* file.
	
	WARNING: This overwrites the original file.
	"""
	# 1) Read existing JSON
	with open(json_path, 'r') as f:
		data = json.load(f)

	# 2) Go through game_log entries
	game_log = data["game_log"]

	for i, entry in enumerate(game_log):
		action = entry.get("action")
		if action is None:
			# Not an actual move—skip
			continue

		agent = entry["agent"]
		obs_dict = {
			"observation": entry["observation"],
			"action_mask": entry["action_mask"]
		}

		# (A) Parse observation into a 2D board
		board_state, legal_moves, legal_moves_list = parse_observation(obs_dict, agent)
		str_board_state, old_legal_moves, old_legal_moves_list = old_parse_observation(obs_dict, agent)

		# (B) Convert to array
		if agent == "player_1":
			best_move, move_scores, best_moves, best_val = find_best_move_for_x(board_state)
		else:
			best_move, move_scores, best_moves, best_val = find_best_move_for_o(board_state)
			for k in move_scores:
				move_scores[k] *= -1

		# (E) Store the score in the same entry
		entry["board_state"] = board_state
		entry["str_board_state"] = str_board_state
		entry["move_scores"] = move_scores
		entry["best_move"] = best_move
		entry["best_moves"] = best_moves
		entry["best_val"] = best_val

	# 3) Overwrite the original JSON file with updated data
	with open(json_path, 'w') as f:
		json.dump(data, f, indent=2)

	return data


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Score Tic Tac Toe game logs.")
	parser.add_argument('--json_foldeer', type=str, required=True, help='Path to the folder containing JSON files.')
	args = parser.parse_args()
	json_folder = args.json_folder
	json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
	for file in tqdm(json_files):
		json_path = os.path.join(json_folder, file)
		updated_data = score_game_log_inplace(json_path)

	# Print out final scores
	# print(f"\nUpdated the original file: {json_path}")
	# print("Scores in the updated game_log:")
	# for i, entry in enumerate(updated_data["game_log"]):
	#     if "score" in entry:
	#         print(f" Move #{i} => Agent: {entry['agent']}, Action: {entry['action']}, Score: {entry['score']}")
