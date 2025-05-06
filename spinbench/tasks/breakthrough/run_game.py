import argparse
import time
import json
import sys
import copy
import pyspiel
import os
import json
import regex
from spinbench.tools.chat_service import get_chat
from spinbench.tools.play_service import (
	play,
	create_hook_functions,
)
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import numpy as np
from spinbench.tasks.breakthrough.utils import (
	parse_game_state,
	generate_state_description,
	generate_action_prompt,
	parse_legal_actions,
	gen_move,
	get_initial_player_messages,
)

def run_game(player_models_json, store_folder, total_rounds=4, test_model1=None, test_model2=None):
	assert total_rounds % 2 == 0, "total_rounds should be even"
	if not os.path.exists(store_folder):
		os.makedirs(store_folder)
	if test_model1 is None and test_model2 is None:
		player_list_json = json.load(open(player_models_json,"r"))
		player1_model_list = player_list_json["player1_model_list"]
		player2_model_list = player_list_json["player2_model_list"]
	else:
		player1_model_list = [{"model": test_model1, "prompt_config": []}]
		player2_model_list = [{"model": test_model2, "prompt_config": []}]
	print(len(player1_model_list), len(player2_model_list))
	time.sleep(1)
	for i in range(len(player1_model_list)):
		print(player1_model_list[i]["model"], "vs", player2_model_list[i]["model"])
	assert len(player1_model_list) == len(player2_model_list)

	for model_index in range(len(player1_model_list)):
		for game_index in range(total_rounds):
			try:
				player1_model = player1_model_list[model_index]
				player2_model = player2_model_list[model_index]
				player1_model_name = player1_model["model"]
				player2_model_name = player2_model["model"]
				if game_index < total_rounds // 2:
					pass
				else:
					temp = player1_model
					player1_model = player2_model
					player2_model = temp
					temp = player1_model_name
					player1_model_name = player2_model_name
					player2_model_name = temp

				player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
				player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
				player1_model_save_name = player1_model_save_name.replace("/", "_")
				player2_model_save_name = player2_model_save_name.replace("/", "_")
				print(player1_model_save_name, player2_model_save_name)
				filename = f"{store_folder}/breakthrough_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
				another_filename = f"{store_folder}/breakthrough_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
				if os.path.exists(filename) or os.path.exists(another_filename):
					print("Already played")
					continue
				
				first_player_messages, second_player_messages = get_initial_player_messages()

				first_player_store_message = first_player_messages.copy()
				second_player_store_message = second_player_messages.copy()
				first_player_reasoning_action_steps = []
				second_player_reasoning_action_steps = []

				game= pyspiel.load_game("breakthrough", {"rows": 8, "columns": 8})
				state = game.new_initial_state()
				print(state)
				win = None # 0 is player1, 1 is player2, 2 is Draw, 3 is player1 illegal move, 4 is player2 illegal move
				total_tokens = 0
				game_log = []
				game_state = None
				cnt = 0
				while not state.is_terminal():
					cnt =+ 1
					print("*"*30)
					print("Turn: ", state.current_player())
					print("current returns: ", state.returns())
					player_index = state.current_player()
					print("Current player: ", player_index)
					legal_actions = state.legal_actions()
					player_observation = state.observation_string(player_index)
					print(player_observation)
					print(parse_game_state(player_observation))
					print(parse_legal_actions(state, state.legal_actions()))

					if player_index == 0:
						m = first_player_messages
						sm = first_player_store_message
						player_model = player1_model
						player_model_name = player1_model_name
						player_reasoning_action_steps = first_player_reasoning_action_steps
					else:
						m = second_player_messages
						sm = second_player_store_message
						player_model = player2_model
						player_model_name = player2_model_name
						player_reasoning_action_steps = second_player_reasoning_action_steps
					m = m[:2]
					hook_functions = create_hook_functions(player_model, player_reasoning_action_steps, generate_state_description(player_observation), generate_action_prompt(parse_legal_actions(state, state.legal_actions())))
					move, action, win, game_state, added_tokens = play(m, sm, player_model_name, player_reasoning_action_steps, None, None, legal_actions, gen_move, 4, True, hook_functions, player_index)
					total_tokens += added_tokens
					print("Action: ", action)
					game_log.append({
						"state": player_observation,
						"player_index": player_index,
						"action": int(action),
						"returns": list(map(int, state.returns())),
						"legal_actions": legal_actions,
						"serialized_state": state.serialize(),
					})
					state.apply_action(action)
				returns = list(map(int, state.returns()))
				print("Game over, Returns:", returns)

				player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
				player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
				player1_model_save_name = player1_model_save_name.replace("/", "_")
				player2_model_save_name = player2_model_save_name.replace("/", "_")
				print(player1_model_save_name, player2_model_save_name)
				# save the chat log for two players
				with open(f"{store_folder}/breakthrough_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
					json.dump({
						"player1_model": player1_model,
						"player2_model": player2_model,
						"returns": returns,
						"timestamp": cnt,
						"total_tokens": total_tokens,
						"illegal_tolerance": 4,
						"number_of_requests": len(game_log)/2,
						"game_log": game_log,
						"first_player_messages": first_player_store_message,
						"second_player_messages": second_player_store_message,
						"game_state": state.to_string(),
					}, f, indent=4)
			except Exception as e:
				print(e)
				continue

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--player_models_json", type=str, help="Path to the player models JSON file")
	parser.add_argument("--store_folder", type=str, required=True, help="Path to the folder where results will be stored")
	parser.add_argument("--total_rounds", type=int, default=6)
	parser.add_argument("--test_model1", type=str, default=None, help="Tested model name 1")
	parser.add_argument("--test_model2", type=str, default=None, help="Tested model name 2")
	args = parser.parse_args()

	if args.player_models_json is None:
		assert args.test_model1 is not None and args.test_model2 is not None, "If player_models_json is None, test_model1 and test_model2 should be provided"

	run_game(args.player_models_json, args.store_folder, args.total_rounds, args.test_model1, args.test_model2)

# example usage:
# python -m spinbench.tasks.breakthrough.run_game --store_folder ./results/breakthrough --test_model1="o4-mini" --test_model2="o1-mini" 
