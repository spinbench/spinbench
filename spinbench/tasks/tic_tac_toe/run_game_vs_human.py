from pettingzoo.classic import tictactoe_v3
import time
from openai import OpenAI
import os
import re
import json
import regex
import sys
sys.path.append(os.path.abspath("../"))
from spinbench.tools.chat_service import get_chat, fix_json
from spinbench.tools.play_service import (
	play,
	create_hook_functions,
)
from spinbench.tasks.tic_tac_toe.utils import (
	generate_action_prompt,
	parse_observation,
	gen_move,
	get_initial_player_messages,
	check_win,
)
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import argparse

def generate_reasoning_prompt(player_reasoning_action_steps):
	li = [f"Move: {step['action']}\nReason: {step['reason']}" for step in player_reasoning_action_steps[-3:]]
	steps = "\n---------------------------\n".join(li)
	return f"""
Your previous moves and thinking are below  (in the last 3 moves in the order of the oldest to the newest):
<previous_moves>
{steps}
</previous_moves>
"""

def run_game_vs_human(store_folder, model, total_rounds = 4):

	init_player1_model = {
		"model": model,
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

	if not os.path.exists(store_folder):
		os.makedirs(store_folder)

	for game_index in range(total_rounds):
		player1_model = init_player1_model
		player2_model = init_player2_model
		
		if game_index >= total_rounds//2:
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
		filename = f"{store_folder}/ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
		reverse_filename = f"{store_folder}/ttt_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
		if os.path.exists(f"{filename}") or os.path.exists(f"{reverse_filename}"):
			print("File exists")
			continue

		first_player_messages, second_player_messages = get_initial_player_messages()
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
				win = check_win(rewards)
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
		with open(f"{store_folder}/ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Set model name for player1_model")
	parser.add_argument('--model', type=str, required=True, help="Specify the model name (e.g., gpt-4o)")
	parser.add_argument('--store_folder', type=str, required=True, help="Specify the folder to save the game logs")
	parser.add_argument('--total_rounds', type=int, default=4, help="Specify the number of rounds to play")
	# Parse the arguments
	args = parser.parse_args()
	run_game_vs_human(args.store_folder, args.model, args.total_rounds)