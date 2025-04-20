import random
import os
import json
import regex
from tools.chat_service import get_chat
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)

######################################
############ prompt utils ############
######################################

first_player_initial_prompt = """
You are playing a game of Tic-Tac-Toe against an opponent. Tic-tac-toe is a simple turn based strategy game where 2 players, X and O, take turns marking spaces on a 3 x 3 grid. The first player to place 3 of their marks in a horizontal, vertical, or diagonal line is the winner. Taking an illegal move ends the game and the player who made the illegal move loses.
The board is a 3x3 grid, and you are playing as 'X'. The opponent is playing as 'O'. The board is indexed as follows:
Action Space: 
Each action from 0 to 8 represents placing either an X or O in the corresponding cell. The cells are indexed as follows:

0 | 3 | 6
_________

1 | 4 | 7
_________

2 | 5 | 8
"""

second_player_initial_prompt = """
You are playing a game of Tic-Tac-Toe against an opponent. Tic-tac-toe is a simple turn based strategy game where 2 players, X and O, take turns marking spaces on a 3 x 3 grid. The first player to place 3 of their marks in a horizontal, vertical, or diagonal line is the winner.
The board is a 3x3 grid, and you are playing as 'O'. The opponent is playing as 'X'. The board is indexed as follows:
Action Space: 
Each action from 0 to 8 represents placing either an X or O in the corresponding cell. The cells are indexed as follows:

0 | 3 | 6
_________

1 | 4 | 7
_________

2 | 5 | 8
"""

def get_initial_player_messages():
	first_player_messages = [
		{
			"role": "user",
			"content": first_player_initial_prompt,
		},
		{
			"role": "assistant",
			"content": "Sure, let's start. "
		},
	] 
	second_player_messages = [
		{
			"role": "user",
			"content": second_player_initial_prompt,
		},
		{
			"role": "assistant",
			"content": "Sure, let's start. "
		},
	]
	return first_player_messages, second_player_messages

def generate_action_prompt(legal_moves):
	action_prompt = """

	0 | 3 | 6
	_________

	1 | 4 | 7
	_________

	2 | 5 | 8

	Now it's your move. Please enter the index of the cell where you would like to place your mark (0-8), you should enter a number between 0 and 8 based on the cell index shown above. You should serialize the output to a json object with the key "reason" and the value string as the detailed reason for your action, and the key "action" and the value as the index of the cell where you would like to place your mark.
	Your output should be in this format: {"reason": string, "action": int}, and you can only use json valid characters. When you write json, all the elements (including all the keys and values) should be enclosed in double quotes!!!
	"""
	return action_prompt + f"\nLegal moves: {legal_moves} You must select one legal move from this list. You have to win.\n"

def generate_reasoning_prompt(player_reasoning_action_steps):
	li = [f"Move: {step['action']}\nReason: {step['reason']}" for step in player_reasoning_action_steps[-3:]]
	steps = "\n---------------------------\n".join(li)
	return f"""
Your previous moves and thinking are below  (in the last 3 moves in the order of the oldest to the newest):
<previous_moves>
{steps}
</previous_moves>
"""

def parse_observation(observation_dict, agent):
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

######################################
########### running utils ############
######################################

def gen_move(player_messages, player_model):
	content, used_token = get_chat(player_model, player_messages)
	try:
		parsed_json = None
		matches = json_pattern.findall(content)
		for match in matches:
			try:
				parsed_json = json.loads(match)
				print("Valid JSON Found:", parsed_json)
			except Exception as e:
				print("Invalid JSON Found:", match)
				parsed_json = json.loads(match)
		action = int(parsed_json["action"])
		reason = parsed_json["reason"]
		move = action
	except Exception as e:
		print(e)
		move = None
		action = None
		reason = None
	return move, content, used_token, action, reason


######################################
########### solver utils #############
######################################


def is_board_full(board_2d):
	"""
	Returns True if the board has no empty cells, False otherwise.
	"""
	for row in range(3):
		for col in range(3):
			if board_2d[row][col] == ' ':
				return False
	return True

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

	for move_idx in legal_moves:
		r, c = divmod(move_idx, 3)
		board_2d[r][c] = 'X'
		val = minimax(board_2d, is_maximizing=False)  # Next turn: O
		board_2d[r][c] = ' '
		if val > best_val:
			best_val = val
			best_moves = [move_idx]
		elif val == best_val:
			best_moves.append(move_idx)
	random.shuffle(best_moves)
	best_move = best_moves[0] if best_moves else None
	return best_move

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
	
	for move_idx in legal_moves:
		r, c = divmod(move_idx, 3)
		board_2d[r][c] = 'O'
		val = minimax(board_2d, is_maximizing=True)  # Next turn: X
		board_2d[r][c] = ' '
		if val < best_val:
			best_val = val
			best_moves = [move_idx]
		elif val == best_val:
			best_moves.append(move_idx)
	random.shuffle(best_moves)
	best_move = best_moves[0] if best_moves else None
	return best_move


def getLegalMoves(board_array):
	legal_moves = []
	for row in range(3):
		for col in range(3):
			if board_array[row][col] == ' ':
				move_idx = row * 3 + col  # Mapping (row, col) to index
				legal_moves.append(move_idx)
	return legal_moves


def detectWin(board_2d, player_mark):
	"""
	Checks if the given player has won the game.

	:param board_2d: 3x3 list of lists containing ' ', 'X', or 'O'.
	:param player_mark: 'X' or 'O'.
	:return: True if the player has won, False otherwise.
	"""
	# Check rows
	for row in board_2d:
		if all(cell == player_mark for cell in row):
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
