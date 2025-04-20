from pettingzoo.classic import tictactoe_v3
import os
import json
import regex
from tools.chat_service import get_chat
from tools.play_service import (
	play,
	create_hook_functions,
)
from tools.project_root import ROOT
from tasks.tic_tac_toe.utils import (
	generate_action_prompt,
	parse_observation,
	gen_move,
	get_initial_player_messages,
)

saves_folder = ROOT / "saves/tic_tac_toe"
if not os.path.exists(saves_folder):
	os.makedirs(saves_folder)

# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
player_list_json = json.load(open(ROOT / "configs/player-list.json","r"))
player1_model_list = player_list_json["player1_model_list"]
player2_model_list = player_list_json["player2_model_list"]
print(len(player1_model_list), len(player2_model_list))
for i in range(len(player1_model_list)):
	print(player1_model_list[i]["model"], "vs", player2_model_list[i]["model"])
assert len(player1_model_list) == len(player2_model_list)
for model_index in range(len(player1_model_list)):
	for game_index in range(10):
		try:
			player1_model = player1_model_list[model_index]
			player2_model = player2_model_list[model_index]
			player1_model_name = player1_model["model"]
			player2_model_name = player2_model["model"]
			if game_index < 5:
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
			filename = saves_folder / f"ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
			if os.path.exists(filename):
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
			with open(saves_folder / f"ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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