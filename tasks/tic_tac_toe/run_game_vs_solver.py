from pettingzoo.classic import tictactoe_v3
import os
import json
import argparse
import regex
from tools.play_service import (
	play,
	create_hook_functions,
)
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
from tasks.tic_tac_toe.utils import (
	generate_action_prompt,
	parse_observation,
	gen_move,
	find_best_move_for_x,
	find_best_move_for_o,
	get_initial_player_messages,
	check_win,
)

# old version
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

def run_game_vs_solver(saves_folder, player_list, total_rounds=10):
	assert total_rounds % 2 == 0, "total_rounds must be even"
	if not os.path.exists(saves_folder):
		os.makedirs(saves_folder)
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
				filename = f"{saves_folder}/ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
				reverse_filename = f"{saves_folder}/ttt_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
				if os.path.exists(filename) or os.path.exists(reverse_filename):
					print("File exists", filename)
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
					old_board_state, old_legal_moves, old_legal_moves_list = old_parse_observation(observation, agent)
					print("board state: ", old_board_state)
					rewards = env.rewards
					print(rewards)
					if win != None:
						break
					if win == None:
						win = check_win(rewards)
					illegal_tolerance = 10
					if termination or truncation:
						action = None
					else:
						if agent == 'player_1':
							# First_player
							if player1_model_name == 'our_solver':
								# move_for = +1  # 'X'
								best_move = find_best_move_for_x(board_state)
								action = best_move
							else:
								# LLM-based approach
								first_player_messages = first_player_messages[:2]
								print("Debug before or after 1")
								hook_functions = create_hook_functions(
									player1_model,
									first_player_reasoning_action_steps,
									old_board_state,
									generate_action_prompt(old_legal_moves)
								)
								print("Debug before or after 2")
								move, action, win, game_state, added_tokens = play(
									first_player_messages,
									first_player_store_message,
									player1_model_name,
									first_player_reasoning_action_steps,
									old_board_state,
									old_legal_moves,
									old_legal_moves_list,
									gen_move,
									illegal_tolerance,
									True,
									hook_functions,
									0
								)
								print("Debug before or after 3")
								total_tokens += added_tokens

						elif agent == 'player_2':
							print("DEBUG: agent=", agent, " player2_model_name=", player2_model_name)
							if player2_model_name == 'our_solver':
								# move_for = -1  # 'O'
								best_move = find_best_move_for_o(board_state)
								action = best_move
							else:
								# LLM-based approach for player_2
								second_player_messages = second_player_messages[:2]
								hook_functions = create_hook_functions(
									player2_model,
									second_player_reasoning_action_steps,
									old_board_state,
									generate_action_prompt(old_legal_moves)
								)
								move, action, win, game_state, added_tokens = play(
									second_player_messages,
									second_player_store_message,
									player2_model_name,
									second_player_reasoning_action_steps,
									old_board_state,
									old_legal_moves,
									old_legal_moves_list,
									gen_move,
									illegal_tolerance,
									True,
									hook_functions,
									1
								)
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
				with open(f"{saves_folder}/ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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
				import traceback
				traceback.print_exc()
				print(e)
				continue

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run Tic Tac Toe game")
	parser.add_argument(
		"--saves_folder",
		type=str,
		required=True,
		help="Folder to save the game results",
	)
	parser.add_argument(
		"--player_list",
		type=str,
		required=True,
		help="Path to the JSON file containing player models",
	)
	parser.add_argument(
		"--total_rounds",
		type=int,
		default=10,
		help="Total rounds to play",
	)
	args = parser.parse_args()
	saves_folder = args.saves_folder
	player_list = args.player_list
	total_rounds = args.total_rounds
	run_game_vs_solver(saves_folder, player_list, total_rounds)