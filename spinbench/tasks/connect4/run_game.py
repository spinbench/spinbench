import os
import regex
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import json
from pettingzoo.classic import connect_four_v3
import time
from spinbench.tools.play_service import (
	play,
	create_hook_functions,
)
from spinbench.tasks.connect4.utils import (
	generate_action_prompt,
	gen_move,
	get_initial_player_messages,
	check_win,
	parse_observation,
)
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

def run_game(store_folder, player_list, total_rounds=10, illtor=10):
	assert total_rounds % 2 == 0, "total_rounds should be even"
	if not os.path.exists(store_folder):
		os.makedirs(store_folder)
	player_list_json = json.load(open(player_list,"r"))
	player1_model_list = player_list_json["player1_model_list"]
	player2_model_list = player_list_json["player2_model_list"]
	print(len(player1_model_list))
	print(len(player2_model_list))
	for i in range(len(player1_model_list)):
		print(player1_model_list[i]["model"], "vs", player2_model_list[i]["model"])
	assert len(player1_model_list) == len(player2_model_list)

	for model_index in range(len(player1_model_list)):
		for game_index in range(total_rounds):
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
			filename = f"{store_folder}/cf_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
			reverse_filename = f"{store_folder}/cf_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
			if os.path.exists(filename) or os.path.exists(reverse_filename):
				continue

			first_player_messages, second_player_messages = get_initial_player_messages()
			first_player_reasoning_action_steps = []
			second_player_reasoning_action_steps = []

			first_player_store_message = first_player_messages.copy()
			second_player_store_message = second_player_messages.copy()

			env = connect_four_v3.env(render_mode="rgb_array")
			env.reset(seed=42)
			win = None # 0 is player1, 1 is player2, 2 is Draw, 3 is player1 illegal move, 4 is player2 illegal move
			total_tokens = 0
			
			game_log = []

			for agent in env.agent_iter():
				hook_functions = {}
				observation, reward, termination, truncation, info = env.last()
				grid_description, legal_moves_description, legal_moves = parse_observation(observation, agent)
				print(type(legal_moves[0]))
				print(grid_description)
				rewards = env.rewards
				print(rewards)
				if win != None:
					break
				if win == None:
					win = check_win(rewards)
					if win != None:
						break
				illegal_tolerance = illtor
				if termination or truncation:
					action = None
				else:
					if agent == 'player_0':
						first_player_messages = first_player_messages[:2]
						hook_functions = create_hook_functions(player1_model, first_player_reasoning_action_steps, "Your opponent has made the move, and now the state is: \n" + grid_description + "\n", generate_action_prompt(legal_moves))
						move, action, win, game_state, added_tokens = play(first_player_messages, first_player_store_message, player1_model_name, first_player_reasoning_action_steps, grid_description, legal_moves_description, legal_moves, gen_move, illegal_tolerance,True, hook_functions,0)
						total_tokens += added_tokens
					elif agent == 'player_1':
						second_player_messages = second_player_messages[:2]
						hook_functions = create_hook_functions(player2_model, second_player_reasoning_action_steps, "Your opponent has made the move, and now the state is: \n" + grid_description + "\n", generate_action_prompt(legal_moves))
						move, action, win, game_state, added_tokens = play(second_player_messages, second_player_store_message, player2_model_name, second_player_reasoning_action_steps, grid_description, legal_moves_description, legal_moves, gen_move, illegal_tolerance,True, hook_functions,1)
						total_tokens += added_tokens
				game_log.append({
					"agent": agent,
					"action": action,
					"observation": observation["observation"].tolist(),
					"reward": env.rewards,
					"action_mask": observation["action_mask"].tolist(),
				})
				try:
					env.step(move)
				except Exception as e:
					print(e)
					break
			env.close()

			player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
			player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
			player1_model_save_name = player1_model_save_name.replace("/", "_")
			player2_model_save_name = player2_model_save_name.replace("/", "_")
			print(player1_model_save_name, player2_model_save_name)
			if win == None:
				win = 2
			# save the chat log for two players
			with open(f"{store_folder}/cf_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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
					"game_log": game_log,
					"first_player_messages": first_player_store_message,
					"second_player_messages": second_player_store_message,
				}, f, indent=4)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run connect four game")
	parser.add_argument('--store_folder', type=str, required=True, help="Folder to store the game results")
	parser.add_argument('--player_list', type=str, required=True, help="Path to the player list JSON file")
	parser.add_argument('--total_rounds', type=int, default=10, help="Total rounds to play")
	parser.add_argument('--illegal_tolerance', type=int, default=10, help="Illegal move tolerance")
	args = parser.parse_args()

	store_folder = args.store_folder
	player_list = args.player_list
	total_rounds = args.total_rounds
	illegal_tolerance = args.illegal_tolerance

	run_game(store_folder, player_list, total_rounds, illegal_tolerance)