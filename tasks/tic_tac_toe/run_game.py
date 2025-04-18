from pettingzoo.classic import tictactoe_v3
import os
import json
import regex
from utils.chat_service import get_chat
from utils.play_service import (
	play,
	create_hook_functions,
)
from tasks.tic_tac_toe.utils import (
	generate_action_prompt,
	parse_observation,
	gen_move,
)
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
player_list_json = json.load(open("solver-list-deepseek.json","r"))
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
			filename = f"ttt_archive/ttt_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
			if os.path.exists(filename):
				old_status = json.load(open(filename, "r"))["status"]
				if "illegal move!" in old_status:
					print("File exists, but illegal move, continue", filename)
					pass
				else:
					print("File exists", filename)
					# time.sleep(1)
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
		except Exception as e:
			print(e)
			continue