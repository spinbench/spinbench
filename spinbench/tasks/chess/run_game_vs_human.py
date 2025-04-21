import chess
import os
import regex
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import sys
sys.path.append(os.path.abspath("../"))
import json
import time
from spinbench.tools.play_service import (
	play,
	create_hook_functions,
)
from spinbench.tasks.chess.utils import (
	generate_action_prompt,
	generate_reasoning_prompt,
	get_initial_player_messages,
	format_board,
	get_move,
	gen_move, 
)
import argparse

def run_game_vs_human(model_name, store_folder, total_round=4):
	assert total_round % 2 == 0, "total_round should be even"
	if not os.path.exists(store_folder):
		os.makedirs(store_folder)

	init_player1_model = {
				"model": model_name,
				"prompt_config": [
					{
						"name": "forced-reasoning",
						"params": {
							"interactive_times": 1,
							"prompt_messages": [
								"Please reason about the current state. You should analyze all the opponent's moves and your moves, try to reason opponent's thought in detail. Only need to reason now, no need to make move at this stage."
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
								"Please reason about the current state. You should analyze all the opponent's moves and your moves, try to reason opponent's thought in detail. Only need to reason now, no need to make move at this stage."
							]
						}
					}
				]
			}

	for game_index in range(total_round):
		try:
			player1_model = init_player1_model
			player2_model = init_player2_model
			if game_index > total_round // 2:
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
			filename = f"{store_folder}/chess_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
			if os.path.exists(filename):
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
			win = None # 0 is player1, 1 is player2, 2 is Draw, 3 is player1 illegal move, 4 is player2 illegal move
			total_tokens = 0
			game_log = []
			game_state = None
			while True:
				hook_functions = {}
				outcome = board.outcome()
				print(board)
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
				illegal_tolerance = 10
				if turn == True: # white
					if player1_model_name == "human":
						print("\nPlease look at the current board state represented by ascii and FEN and make your next move:\n <FEN>\nFEN: " + board.fen() +  "\n</FEN>\n\n<board_state>\n\n2D board: \n" + format_board(str(board)) + "\n</board_state>\n\n"+ generate_action_prompt([move.uci() for move in board.legal_moves]))
						action = input("You are playing as uppercase letters, Enter your uci move: ")
						move = get_move(board, action)
					else:
						first_player_messages = first_player_messages[:2]
						hook_functions = create_hook_functions(player1_model, first_player_reasoning_action_steps, "\nPlease look at the current board state represented by ascii and FEN and make your next move:\n <FEN>\nFEN: " + board.fen() +  "\n</FEN>\n\n<board_state>\n\n2D board: \n" + format_board(str(board)) + "\n</board_state>\n\n", generate_action_prompt([move.uci() for move in board.legal_moves]))
						move, action, win, game_state, added_tokens = play(first_player_messages, first_player_store_message, player1_model_name, first_player_reasoning_action_steps, board, "", legal_moves, gen_move,illegal_tolerance, True, hook_functions,0,board=board,legal_move_list=[move.uci() for move in legal_moves])
						total_tokens += added_tokens
				elif turn == False: # black
					if player2_model_name == "human":
						print("\nPlease look at the current board state represented by ascii and FEN and make your next move:\n <FEN>\nFEN: " + board.fen() +  "\n</FEN>\n\n<board_state>\n\n2D board: \n" + format_board(str(board)) + "\n</board_state>\n\n"+ generate_action_prompt([move.uci() for move in board.legal_moves]))
						action = input("You are playing as lowercase letters, Enter your uci move: ")
						move = get_move(board, action)
					else:
						second_player_messages = second_player_messages[:2]
						hook_functions = create_hook_functions(player2_model, second_player_reasoning_action_steps, "\nPlease look at the current board state represented by ascii and FEN and make your next move:\n <FEN>\nFEN: " + board.fen() +  "\n</FEN>\n\n<board_state>\n\n2D board: \n" + format_board(str(board)) + "\n</board_state>\n\n", generate_action_prompt([move.uci() for move in board.legal_moves]))
						move, action, win, game_state, added_tokens = play(second_player_messages, second_player_store_message, player2_model_name, second_player_reasoning_action_steps, board, "", legal_moves, gen_move,illegal_tolerance, False, hook_functions,1,board=board,legal_move_list=[move.uci() for move in legal_moves])
						total_tokens += added_tokens
				game_log.append({
					"board": board.fen(),
					"agent": "white" if turn == True else "black",
					"action": action,
				})
				if win != None:
					break
				try:
					board.push(move)
				except Exception as e:
					print(e)
					break
			player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
			player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
			player1_model_save_name = player1_model_save_name.replace("/", "_")
			player2_model_save_name = player2_model_save_name.replace("/", "_")
			print(player1_model_save_name, player2_model_save_name)
			# save the chat log for two players
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
		except Exception as e:
			print(e)
			continue

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--model_name", type=str, required=True, help="The model name to use for the game.")
	parser.add_argument("--store_folder", type=str, required=True, help="The folder to store the game results.")
	parser.add_argument("--total_round", type=int, default=4, help="The total number of rounds to play.")
	args = parser.parse_args()
	run_game_vs_human(args.model_name, args.store_folder, args.total_round)