from pettingzoo.classic import tictactoe_v3
import os
import json
import regex
from spinbench.tools.chat_service import get_chat
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
import argparse

def run_game(store_folder, player_list, total_rounds=10, illtor=10):
	assert total_rounds % 2 == 0, "total_rounds must be even"
	if not os.path.exists(store_folder):
		os.makedirs(store_folder)
	player_list_json = json.load(open(player_list,"r"))
	player1_model_list = player_list_json["player1_model_list"]
	player2_model_list = player_list_json["player2_model_list"]
	print(len(player1_model_list), len(player2_model_list))
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

				filename = store_folder / f"ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
				reverse_filename = store_folder / f"ttt_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
				if os.path.exists(filename) or os.path.exists(reverse_filename):
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
					print(board_state)
					rewards = env.rewards
					print(rewards)

					if win != None:
						break
					if win == None:
						win = check_win(rewards)

					illegal_tolerance = illtor
					if termination or truncation:
						action = None
					else:
						if agent == 'player_1':
							# first_player
							first_player_messages = first_player_messages[:2]
							hook_functions = create_hook_functions(player1_model, first_player_reasoning_action_steps, board_state, generate_action_prompt(legal_moves))
							move, action, win, game_state, added_tokens = play(first_player_messages, first_player_store_message, player1_model_name, first_player_reasoning_action_steps, board_state, legal_moves, legal_moves_list, gen_move, illegal_tolerance, True, hook_functions,0)
							total_tokens += added_tokens
						elif agent == 'player_2':
							# second_player
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
				with open(store_folder / f"ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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
			except Exception as e:
				print(e)
				continue

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run Tic Tac Toe game")
	parser.add_argument(
		"--store_folder",
		type=str,
		required=True,
		help="Path to the folder where game results will be saved",
	)
	parser.add_argument(
		"--player_list",
		type=str,
		required=True,
		help="Path to the JSON file containing player list",
	)
	parser.add_argument(
		"--total_rounds",
		type=int,
		default=10,
		help="Total number of rounds to play",
	)
	parser.add_argument(
		"--illegal_tolerance",
		type=int,
		default=10,
		help="Illegal move tolerance",
	)
	args = parser.parse_args()
	store_folder = args.store_folder
	player_list = args.player_list
	total_rounds = args.total_rounds
	illegal_tolerance = args.illegal_tolerance

	if not os.path.exists(store_folder):
		os.makedirs(store_folder)
	
	run_game(store_folder, player_list, total_rounds, 	illegal_tolerance)