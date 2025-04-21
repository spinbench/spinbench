import random
import requests
import os
import json
from tools.chat_service import get_chat,fix_json
import regex
from tools.chat_service import get_chat
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)

######################################
############ prompt utils ############
######################################

first_player_initial_prompt = """
You are playing a game of Connect Four against an opponent. Connect Four is a 2-player turn based game, where players must connect four of their tokens vertically, horizontally or diagonally. The players drop their respective token in a column of a standing grid, where each token will fall until it reaches the bottom of the column or reaches an existing token. Players cannot place a token in a full column, and the game ends when either a player has made a sequence of 4 tokens, or when all 7 columns have been filled. Taking an illegal move ends the game and the player who made the illegal move loses.
The board is a 6x7 grid, and you are playing as 'X'. The opponent is playing as 'O'. 
The action space is the set of integers from 0 to 6 (inclusive), from left to right, where the action represents which column a token should be dropped in.
"""

second_player_initial_prompt = """
You are playing a game of Connect Four against an opponent. Connect Four is a 2-player turn based game, where players must connect four of their tokens vertically, horizontally or diagonally. The players drop their respective token in a column of a standing grid, where each token will fall until it reaches the bottom of the column or reaches an existing token. Players cannot place a token in a full column, and the game ends when either a player has made a sequence of 4 tokens, or when all 7 columns have been filled. Taking an illegal move ends the game and the player who made the illegal move loses.
The board is a 6x7 grid, and you are playing as 'O'. The opponent is playing as 'X'. 
The action space is the set of integers from 0 to 6 (inclusive), from left to right, where the action represents which column a token should be dropped in.
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
	action_prompt = f"""
Now it's your move. Please enter the index of the column where you would like to place your token (0-6 from left to right), except the illegal position. You should serialize the output to a json object with the key "reason" and the value str as the detailed reason for your action, and the key "action" and the value as the index of the column where you would like to place your token. The legal moves are: \n<legal_moves>\n{" ".join([str(move) for move in legal_moves])}\n</legal_moves>\n You must select one legal move from this list. You have to win.  Your output should be {{"reason": "your reason", "action": "action index"}}, and you can only use json valid characters. When you write json, all the elements (including all the keys and values) should be enclosed in double quotes!!!
"""
	return action_prompt

######################################
########### running utils ############
######################################

def check_win(rewards):
	win = None
	if len(list(rewards.keys())) == 1 and rewards[list(rewards.keys())[0]] == 0:
		print("Draw!")
		win = 2
	elif rewards["player_0"] == 1 and rewards["player_1"] == 1:
		print("Draw!")
		win = 2
	elif rewards["player_0"] == 1 and rewards["player_1"] == -1:
		print("Player 1 wins!")
		win = 0
	elif rewards["player_0"] == -1 and rewards["player_1"] == 1:
		print("Player 2 wins!")
		win = 1
	elif rewards["player_0"] == -1 and rewards["player_1"] == 0:
		print("Player 1 illegal move!")
		win = 3
	elif rewards["player_0"] == 0 and rewards["player_1"] == -1:
		print("Player 2 illegal move!")
		win = 4
	return win

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
				parsed_json = json.loads(fix_json(match))
		action = int(parsed_json["action"])
		reason = parsed_json["reason"]
		move = action
	except Exception as e:
		print(e)
		move = None
		action = None
		reason = None
	return move, content, used_token, action, reason

def parse_observation(observation_dict, agent):
	"""
	This function takes the observation dictionary from the PettingZoo environment
	and returns a text description of the current game state and legal moves.
	"""
	# Extract observation and action mask
	observation = observation_dict['observation']
	action_mask = observation_dict['action_mask']
	
	player_0_grid = observation[:, :, 0]
	player_1_grid = observation[:, :, 1]

	if agent == "player_0":
		player_mark = "X "
		opponent_mark = "O "
	elif agent == "player_1":
		player_mark = "O "
		opponent_mark = "X "

	X_places = []
	O_places = []

	# Create text description for the current game state
	grid_description = "Current game state:\n"
	for row in range(6):
		row_description = "r" + str(row) + " "
		for col in range(7):
			if player_0_grid[row, col] == 1:
				row_description += player_mark  # Represent player 0's token with 'X'
				if agent == "player_0":
					X_places.append((row, col))
				else:
					O_places.append((row, col))
			elif player_1_grid[row, col] == 1:
				row_description += opponent_mark  # Represent player 1's token with 'O'
				if agent == "player_0":
					O_places.append((row, col))
				else:
					X_places.append((row, col))
			else:
				row_description += "- "  # Empty cell with '-'
		grid_description += row_description.strip() + "\n"
	grid_description += "   "+" ".join(["c0", "c1", "c2", "c3", "c4", "c5", "c6"]) + "\n"

	grid_description += f"""
r0 means row 0, r1 means row 1, and so on.
c0 means column 0, c1 means column 1, and so on.

Token places(row index, column index): 
X tokens are at places: {X_places}
O tokens are at places: {O_places}
"""

	# Create text description for legal moves
	legal_moves_description = "Legal actions (columns where you can drop a token):\n"
	legal_moves = [i for i, is_legal in enumerate(action_mask) if is_legal == 1]
	legal_moves_description += ", ".join([str(col) for col in legal_moves])

	# Combine the two descriptions
	full_description = f"{grid_description}\n{legal_moves_description}"
	
	return grid_description + "\n", legal_moves_description + "\n", legal_moves

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
        response = requests.get(full_url)
        if response.status_code == 200:
            data = response.json()
            return data.get("score", [])
        else:
            print(f"Error fetching scores: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error fetching scores: {e}")
        return []
