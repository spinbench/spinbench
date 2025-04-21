import json
import argparse
import sys
import copy
import pyspiel
import os
import json
import regex
from tools.chat_service import get_chat
from tools.play_service import (
	play,
	create_hook_functions,
)
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import numpy as np
from tasks.hanabi.utils import (
	parse_game_state,
	generate_state_description,
	generate_action_prompt,
	parse_legal_actions,
	gen_move,
	gen_initial_prompt,
)

def run_game(player_models_json, store_folder, result_name, total_round=5):
	player_models = json.load(open(player_models_json,"r")) # list
	player_num = len(player_models)
	if player_num < 5:
		hand_size = 5
	else:
		hand_size = 4
	for idx in range(total_round):
		total_token_used = 0
		filename = result_name+"_"+str(idx)+".json"

		if os.path.exists(f"{store_folder}/{filename}"):
			print("File exists, skipping", filename)
			continue

		log_file = result_name+"_"+str(idx)+".log"
		# output stream to log_file
		if log_file:
			sys.stdout = open(f"{store_folder}/{log_file}", "w")

		index_messages = {
			i: [
				{
					"role": "user",
					"content": gen_initial_prompt()
				}
			] for i in range(player_num)
		}

		# initial prompt
		for i in range(player_num):
			content, used_token = get_chat(player_models[i]["model"], index_messages[i])
			index_messages[i].append({
				"role": "assistant",
				"content": content,
			})
			total_token_used += used_token

		index_store_messages = copy.deepcopy(index_messages)

		game_log = []
		game = pyspiel.load_game("hanabi", {"players": len(player_models),"hand_size": hand_size})
		state = game.new_initial_state()
		cnt = 0
		print(state)
		while not state.is_terminal():
			cnt += 1
			print("*"*30)
			print("cnt: ", cnt)
			print("current returns: ", state.returns())
			legal_actions = state.legal_actions()
			if state.is_chance_node():
				# Sample a chance event outcome.
				print("Chance Node")
				outcomes_with_probs = state.chance_outcomes()
				action_list, prob_list = zip(*outcomes_with_probs)
				action = np.random.choice(action_list, p=prob_list)
				state.apply_action(action)
			else:
				player_index = state.current_player()
				print("State: ", state)
				print("Current Player: ", player_index)
				player_observation = state.observation_string(player_index)
				print(parse_game_state(player_observation))
				print(parse_legal_actions(state, legal_actions))
				index_messages[player_index] = index_messages[player_index][:2]
				hook_functions = create_hook_functions(player_models[player_index], None, generate_state_description(player_observation), generate_action_prompt(parse_legal_actions(state, legal_actions)))
				move, action, win, game_state, added_tokens = play(index_messages[player_index], index_store_messages[player_index], player_models[player_index]["model"], [], None, None, legal_actions, gen_move, 5, True, hook_functions, player_index)
				total_token_used += added_tokens
				print("Action: ", action)
				game_log.append((int(action), state.returns()))
				state.apply_action(action)

		returns = state.returns()
		print("Returns: ", returns)

		# save the chat log
		json.dump({
			"player_models": player_models,
			"total_round": total_round,
			"total_token_used": total_token_used,
			"cnt": cnt,
			"returns": returns,
			"index_store_messages": index_store_messages,
			"game_log": game_log,
		}, open(f"{store_folder}/{filename}", "w"), indent=2, ensure_ascii=False)

		if log_file:
			sys.stdout.close()
			sys.stdout = sys.__stdout__

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--player_models_json", type=str, required=True, help="Path to the player models JSON file")
	parser.add_argument("--store_folder", type=str, required=True, help="Path to the folder where results will be stored")
	parser.add_argument("--result_name", type=str, required=True, help="Name of the result file")
	parser.add_argument("--total_round", type=int, default=5)
	args = parser.parse_args()

	run_game(args.player_models_json, args.store_folder, args.result_name, args.total_round)