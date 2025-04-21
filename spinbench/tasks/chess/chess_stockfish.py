import chess
import time
import os
from stockfish import Stockfish
import regex
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import json
import time
from spinbench.tools.play_service import (
	play,
	create_hook_functions,
)
from spinbench.tasks.chess.utils import (
	generate_action_prompt,
	get_initial_player_messages,
	format_board,
	gen_move, 
)

stockfish = Stockfish("PATH_TO_STOCKFISH_EXECUTABLE")

def run_game_vs_stockfish(store_folder, player_list, total_round=4):
	assert total_round % 2 == 0, "total_round should be even"
	if not os.path.exists(store_folder):
		os.makedirs(store_folder)
	player_list_json = json.load(open(player_list,"r"))
	player1_model_list = player_list_json["player1_model_list"]
	player2_model_list = player_list_json["player2_model_list"]
	print(len(player1_model_list))
	print(len(player2_model_list))
	time.sleep(1)
	for i in range(len(player1_model_list)):
		print(player1_model_list[i]["model"], "vs", player2_model_list[i]["model"])
	assert len(player1_model_list) == len(player2_model_list)

	for model_index in range(len(player1_model_list)):
		for game_index in range(total_round):
			player1_model = player1_model_list[model_index]
			player2_model = player2_model_list[model_index]
			player1_model_name = player1_model["model"]
			player2_model_name = player2_model["model"]
			if game_index < total_round // 2:
				pass
			else:
				temp = player1_model
				player1_model = player2_model
				player2_model = temp
				temp = player1_model_name
				player1_model_name = player2_model_name
				player2_model_name = temp

			if "prompt_config" in player1_model:
				player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
				player1_model_save_name = player1_model_save_name.replace("/", "_")
			elif "elo" in player1_model:
				player1_model_save_name = player1_model_name + "-elo-" + str(player1_model["elo"])
			elif "level" in player1_model:
				player1_model_save_name = player1_model_name + "-level-" + str(player1_model["level"])

			if "prompt_config" in player2_model:
				player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
				player2_model_save_name = player2_model_save_name.replace("/", "_")
			elif "elo" in player2_model:
				player2_model_save_name = player2_model_name + "-elo-" + str(player2_model["elo"])
			elif "level" in player2_model:
				player2_model_save_name = player2_model_name + "-level-" + str(player2_model["level"])

			print(player1_model_save_name, player2_model_save_name)
			filename = f"{store_folder}/chess_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
			another_filename = f"{store_folder}/chess_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
			print(filename)
			if os.path.exists(filename) or os.path.exists(another_filename):
				print("File exists", filename)
				continue

			first_player_messages, second_player_messages = get_initial_player_messages()

			first_player_reasoning_action_steps = [
				# {
				# 	"action": "e2e4",
				# 	"reason": "I am playing e4 to control the center of the board and open up lines for my queen and bishop. This move is a standard opening move in chess, known as the King's Pawn Opening.",
				# }
			]
			second_player_reasoning_action_steps = []


			first_player_store_message = first_player_messages.copy()
			second_player_store_message = second_player_messages.copy()

			board = chess.Board()
			cnt = 0
			win = None # 0 is player1, 1 is player2, 2 is Draw, 3 is player1 illegal move, 4 is player2 illegal move
			total_tokens = 0
			game_log = []
			game_state = None
			while True:
				hook_functions = {}
				cnt += 1
				board_state = format_board(str(board))
				fen_board = board.fen()
				outcome = board.outcome()
				stockfish.set_fen_position(fen_board)
				print(board)
				print("outcome: ", outcome)
				if outcome != None:
					termination = outcome.termination
					game_state = termination.name
					winner = outcome.winner
					result = outcome.result()
					if winner == True:
						print("Player 1 (white) wins!")
						win = 0
					elif winner == False:
						print("Player 2 (black) wins!")
						win = 1
					elif winner == None:
						print("Draw!")
						win = 2
					break
				turn = board.turn
				legal_moves = board.legal_moves
				illegal_tolerance = 10 # if the model makes an illegal move, it will try again 3 times
				if turn == True: # white
					if player1_model_name == "stockfish":
						print("stockfish")
						if "elo" in player1_model:
							elo = player1_model["elo"]
							stockfish.set_elo_rating(elo)
						elif "level" in player1_model:
							level = player1_model["level"]
							stockfish.set_skill_level(level)
						else:
							raise Exception("Stockfish model must have elo or level")
						best_move_by_stockfish = stockfish.get_best_move()
						move = chess.Move.from_uci(best_move_by_stockfish)
					else:
						first_player_messages = first_player_messages[:2]
						hook_functions = create_hook_functions(player1_model, first_player_reasoning_action_steps, "\nPlease look at the current board state represented by ascii and FEN and make your next move:\n <FEN>\nFEN: " + board.fen() +  "\n</FEN>\n\n<board_state>\n\n2D board: \n" + format_board(str(board)) + "\n</board_state>\n\n", generate_action_prompt([move.uci() for move in board.legal_moves]))
						move, action, win, game_state, added_tokens = play(first_player_messages, first_player_store_message, player1_model_name, first_player_reasoning_action_steps, board, "", legal_moves, gen_move,illegal_tolerance, True, hook_functions,0,board=board,legal_move_list=[move.uci() for move in legal_moves])
						total_tokens += added_tokens
				elif turn == False: # black
					if player2_model_name == "stockfish":
						print("stockfish")
						if "elo" in player2_model:
							elo = player2_model["elo"]
							stockfish.set_elo_rating(elo)
						elif "level" in player2_model:
							level = player2_model["level"]
							stockfish.set_skill_level(level)
						else:
							raise Exception("Stockfish model must have elo or level")
						best_move_by_stockfish = stockfish.get_best_move()
						move = chess.Move.from_uci(best_move_by_stockfish)
					else:
						second_player_messages = second_player_messages[:2]
						hook_functions = create_hook_functions(player2_model, second_player_reasoning_action_steps, "\nPlease look at the current board state represented by ascii and FEN and make your next move:\n <FEN>\nFEN: " + board.fen() +  "\n</FEN>\n\n<board_state>\n\n2D board: \n" + format_board(str(board)) + "\n</board_state>\n\n", generate_action_prompt([move.uci() for move in board.legal_moves]))
						move, action, win, game_state, added_tokens = play(second_player_messages, second_player_store_message, player2_model_name, second_player_reasoning_action_steps, board, "", legal_moves, gen_move,illegal_tolerance, False, hook_functions,1,board=board,legal_move_list=[move.uci() for move in legal_moves])
						total_tokens += added_tokens
				game_log.append({
					"board": board.fen(),
					"agent": "white" if turn == True else "black",
					"action": str(move),
				})
				if win != None:
					break
				try:
					board.push(move)
				except Exception as e:
					print(e)
					break
				stockfish.set_fen_position(board.fen())

			# save the chat log for two players
			if "prompt_config" in player1_model:
				player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
				player1_model_save_name = player1_model_save_name.replace("/", "_")
			elif "elo" in player1_model:
				player1_model_save_name = player1_model_name + "-elo-" + str(player1_model["elo"])
			elif "level" in player1_model:
				player1_model_save_name = player1_model_name + "-level-" + str(player1_model["level"])

			if "prompt_config" in player2_model:
				player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
				player2_model_save_name = player2_model_save_name.replace("/", "_")
			elif "elo" in player2_model:
				player2_model_save_name = player2_model_name + "-elo-" + str(player2_model["elo"])
			elif "level" in player2_model:
				player2_model_save_name = player2_model_name + "-level-" + str(player2_model["level"])
			print(player1_model_save_name, player2_model_save_name)
			with open(f"{store_folder}/chess_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
					json.dump({
						"status": game_state,
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