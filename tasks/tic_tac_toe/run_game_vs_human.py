from pettingzoo.classic import tictactoe_v3
import time
from openai import OpenAI
import os
import re
import json
import regex
import sys
sys.path.append(os.path.abspath("../"))
from tools.chat_service import get_chat, fix_json
from tools.play_service import (
	play,
	create_hook_functions,
)
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import argparse
parser = argparse.ArgumentParser(description="Set model name for player1_model")
parser.add_argument('--model', type=str, required=True, help="Specify the model name (e.g., gpt-4o)")
args = parser.parse_args()

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

init_player1_model = {
	"model": args.model,
	"prompt_config": [
		{
			"name": "forced-reasoning",
			"params": {
				"interactive_times": 1,
				"prompt_messages": [
					"Please reason about the current state. You should analyze all the opponent's moves and your moves, try to reason opponent's thought in detail. Only need to plan and reason now, no need to make move at this stage."
				]
			}
		}
	]
}
init_player2_model = {
	"model": "human",
	"prompt_config": [
		{
			"name": "forced-reasoning",
			"params": {
				"interactive_times": 1,
				"prompt_messages": [
					"Please reason about the current state. You should analyze all the opponent's moves and your moves, try to reason opponent's thought in detail. Only need to plan and reason now, no need to make move at this stage."
				]
			}
		}
	]
}

if not os.path.exists("ttt_archive"):
	os.makedirs("ttt_archive")

for game_index in range(4):
	player1_model = init_player1_model
	player2_model = init_player2_model
	
	if game_index >= 2:
		player1_model, player2_model = player2_model, player1_model

	player1_model_name = player1_model["model"]
	player2_model_name = player2_model["model"]
	if "o1" in player1_model_name:
		player1_model["prompt_config"] = []
	if "o1" in player2_model_name:
		player2_model["prompt_config"] = []
	player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
	player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
	player1_model_save_name = player1_model_save_name.replace("/", "_")
	player2_model_save_name = player2_model_save_name.replace("/", "_")
	filename = f"ttt_archive/ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
	print(filename)
	if os.path.exists(f"{filename}"):
		continue

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
	first_player_reasoning_action_steps = []
	second_player_reasoning_action_steps = []
	first_player_store_message = first_player_messages.copy()
	second_player_store_message = second_player_messages.copy()

	env = tictactoe_v3.env(render_mode=None)
	env.reset(seed=42)
	cnt = 0
	win = None # 0 is player1, 1 is player2, 2 is Draw, 3 is player1 illegal move, 4 is player2 illegal move
	total_tokens = 0
	game_log = []
	for agent in env.agent_iter():
		hook_functions = {}
		cnt += 1
		observation, reward, termination, truncation, info = env.last()
		board_state, legal_moves, legal_moves_list = parse_observation(observation, agent)
		rewards = env.rewards
		print(rewards)
		print(board_state)
		if win != None:
			break
		if win == None:
			if len(list(rewards.keys())) == 1 and rewards[list(rewards.keys())[0]] == 0:
				print("Draw!")
				win = 2
			elif rewards["player_1"] == 1 and rewards["player_2"] == 1:
				print("Draw!")
				win = 2
			elif rewards["player_1"] == 1 and rewards["player_2"] == -1:
				print("Player 1 wins!")
				win = 0
			elif rewards["player_1"] == -1 and rewards["player_2"] == 1:
				print("Player 2 wins!")
				win = 1
			elif rewards["player_1"] == -1 and rewards["player_2"] == 0:
				print("Player 1 illegal move!")
				win = 3
			elif rewards["player_1"] == 0 and rewards["player_2"] == -1:
				print("Player 2 illegal move!")
				win = 4
		illegal_tolerance = 10
		if termination or truncation:
			action = None
		else:
			if agent == 'player_1':
				# first_player
				if player1_model_name == "human":
					print(board_state + "\n" + generate_action_prompt(legal_moves))
					action = int(input("You are playing as 'X', Enter your move: "))
				else:
					first_player_messages = first_player_messages[:2]
					hook_functions = create_hook_functions(player1_model, first_player_reasoning_action_steps, board_state, generate_action_prompt(legal_moves))
					move, action, win, game_state, added_tokens = play(first_player_messages, first_player_store_message, player1_model_name, first_player_reasoning_action_steps, board_state, legal_moves, legal_moves_list, gen_move, illegal_tolerance, True, hook_functions,0)
					total_tokens += added_tokens
			elif agent == 'player_2':
				# second_player
				if player2_model_name == "human":
					print(board_state + "\n" + generate_action_prompt(legal_moves))
					action = int(input("You are playing as 'O', Enter your move: "))
				else:
					second_player_messages = second_player_messages[:2]
					hook_functions = create_hook_functions(player2_model, second_player_reasoning_action_steps, board_state, generate_action_prompt(legal_moves))
					move, action, win, game_state, added_tokens = play(second_player_messages, second_player_store_message, player2_model_name, second_player_reasoning_action_steps, board_state, legal_moves, legal_moves_list, gen_move, illegal_tolerance, True, hook_functions,1)
					total_tokens += added_tokens
		game_log.append({
			"agent": agent,
			"action": action,
			"observation": observation["observation"].tolist(),
			"reward": env.rewards,
			"action_mask": observation["action_mask"].tolist(),
		})
		try:
			env.step(action)
		except Exception as e:
			print(e)
			break
	env.close()

	player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
	player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
	player1_model_save_name = player1_model_save_name.replace("/", "_")
	player2_model_save_name = player2_model_save_name.replace("/", "_")
	print(player1_model_save_name, player2_model_save_name)
	# save the chat log for two players
	with open(f"ttt_archive/ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
		json.dump({
			"status": {
				0: "Player 1 wins!",
				1: "Player 2 wins!",
				2: "Draw!",
				3: "Player 1 illegal move!",
				4: "Player 2 illegal move!",
			}[win],
			"winner": {
				0: "Player 1",
				1: "Player 2",
				2: "Draw",
				3: "Player 2",
				4: "Player 1",
			}[win],
			"player1_model": player1_model,
			"player2_model": player2_model,
			"total_tokens": total_tokens,
			"illegal_tolerance": illegal_tolerance,
			"number_of_requests": len(game_log)/2,
			"first_player_messages": first_player_store_message,
			"second_player_messages": second_player_store_message,
			"game_log": game_log,
		}, f, indent=4)