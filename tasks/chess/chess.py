import chess
import time
import os
import regex
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import json
import time
from tools.chat_service import get_chat, fix_json
from utils.play_service import (
	play,
	create_hook_functions,
)

def transform_to_uci(board, s):
    # Parse the notation
    piece_symbol = s[0]  # e.g., 'Q' for queen
    target_square = chess.parse_square(s[1:])  # e.g., 'h8' becomes 63 (the index for h8)

    # Find the UCI move
    for move in board.legal_moves:
        if move.to_square == target_square and board.piece_at(move.from_square).symbol().upper() == piece_symbol:
            return move.uci()
    return None

def get_move(board, action):
	try:
		# uci format
		move = chess.Move.from_uci(action)
	except:
		# if the move is not in uci format
		try:
			move = chess.Move.from_uci(transform_to_uci(board, action))
		except:
			try:
				move = chess.Move.from_uci(action[-4:])
			except:
				return None
	return move

def format_board(board_str):
	# r n b q k b n r
	# p p p p p p p p
	# . . . . . . . .
	# . . . . . . . .
	# . . . . . . . .
	# . . . . . . . .
	# P P P P P P P P
	# R N B Q K B N R
	# to
	#   +------------------------+
	# 8 | r  n  b  q  k  b  n  r |
	# 7 | p  p  p  p  p  p  p  p |
	# 6 | .  .  .  .  .  .  .  . |
	# 5 | .  .  .  .  .  .  .  . |
	# 4 | .  .  .  .  .  .  .  . |
	# 3 | .  .  .  .  .  .  .  . |
	# 2 | P  P  P  P  P  P  P  P |
	# 1 | R  N  B  Q  K  B  N  R |
	#   +------------------------+
	# 	  a  b  c  d  e  f  g  h
	result = "   +------------------------+\n"
	rows = board_str.split("\n")
	tokens = [row.split() for row in rows]
	for i in range(8):
		result += f" {8-i} | " + "  ".join(tokens[i]) + " |\n"
	result += "   +------------------------+\n"
	result += "     a  b  c  d  e  f  g  h\n"
	return result


def generate_action_prompt(legal_moves):
			return f"""
	Please enter your move in Universal Chess Interface (UCI) format. For example, to move a pawn from e2 to e4, you would enter \"e2e4\". You should state your reason first, and serialize the output to a json object with the key "reason" and the value as a string of your reason, the key "action" and the value as a UCI string representing your move. The legal moves are: \n<legal_moves>\n{" ".join(legal_moves)}\n</legal_moves>\n You must select one legal move from this list and respond with the UCI format of the move you choose. Do not generate any move outside of this list. You have to win. In your reason and action, you can only use UCI format to describe. Your output should be in this format: {{"reason": "your reason", "action": "your action"}}, and you can only use json valid characters. When you write json, all the elements (including all the keys and values) should be enclosed in double quotes!!!
	"""

def generate_reasoning_prompt(player_reasoning_action_steps):
			li = [f"Move: {step['action']}\nReason: {step['reason']}" for step in player_reasoning_action_steps[-3:]]
			steps = "\n---------------------------\n".join(li)
			return f"""
	Your previous moves and thinking are below:
	<previous_moves>
	{steps}
	</previous_moves>
	Please explain your thinking before making move. 
	Comment on your current tactics so you know your plan for the next move.
	"""

def gen_move(player_messages, player_model,board=None,legal_move_list=None):
	content, used_token = get_chat(player_model, player_messages)
	try:
		matches = json_pattern.findall(content)
		for match in matches:
			try:
				parsed_json = json.loads(match)
				print("Valid JSON Found:", parsed_json)
			except Exception as e:
				print("Invalid JSON Found:", match)
				parsed_json = fix_json(match)
		action = parsed_json["action"]
		reason = parsed_json["reason"]
		move = get_move(board, action)
	except Exception as e:
		print(e)
		move = None
		action = None
		reason = None
	return move, content, used_token, action, reason

player_list_json = json.load(open("player-list.json","r"))
player1_model_list = player_list_json["player1_model_list"]
player2_model_list = player_list_json["player2_model_list"]

print(len(player1_model_list))
print(len(player2_model_list))
time.sleep(1)
for i in range(len(player1_model_list)):
	print(player1_model_list[i]["model"], "vs", player2_model_list[i]["model"])
assert len(player1_model_list) == len(player2_model_list)

for model_index in range(len(player1_model_list)):
	for game_index in range(4):
		try:
			player1_model = player1_model_list[model_index]
			player2_model = player2_model_list[model_index]
			player1_model_name = player1_model["model"]
			player2_model_name = player2_model["model"]
			if game_index < 2:
				pass
			else:
				temp = player1_model
				player1_model = player2_model
				player2_model = temp
				temp = player1_model_name
				player1_model_name = player2_model_name
				player2_model_name = temp

			if "o1" in player1_model_name:
				player1_model["prompt_config"] = []
			if "o1" in player2_model_name:
				player2_model["prompt_config"] = []

			player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
			player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
			player1_model_save_name = player1_model_save_name.replace("/", "_")
			player2_model_save_name = player2_model_save_name.replace("/", "_")
			print(player1_model_save_name, player2_model_save_name)
			filename = f"chess_archive/chess_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
			another_filename = f"chess_archive/chess_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
			print(filename)
			if os.path.exists(filename) or os.path.exists(another_filename):
				old_status = json.load(open(filename, "r"))["status"]
				print(old_status)
				continue
			

			first_player_initial_prompt = f"""
		You are playing a text game of Chess against an opponent. Chess is a two-player strategy board game played on an 8x8 board. The goal of the game is to checkmate the opponent's king. On the board, your pieces are represented by uppercase letters and the opponent's pieces are represented by lowercase letters. You are a chest master playing a text based game of chess.
			"""

			second_player_initial_prompt = f"""
		You are playing a text game of Chess against an opponent. Chess is a two-player strategy board game played on an 8x8 board. The goal of the game is to checkmate the opponent's king. On the board, your pieces are represented by lowercase letters and the opponent's pieces are represented by uppercase letters. You are a chest master playing a text based game of chess.
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
					first_player_messages = first_player_messages[:2]
					hook_functions = create_hook_functions(player1_model, first_player_reasoning_action_steps, "\nPlease look at the current board state represented by ascii and FEN and make your next move:\n <FEN>\nFEN: " + board.fen() +  "\n</FEN>\n\n<board_state>\n\n2D board: \n" + format_board(str(board)) + "\n</board_state>\n\n", generate_action_prompt([move.uci() for move in board.legal_moves]))

					move, action, win, game_state, added_tokens = play(first_player_messages, first_player_store_message, player1_model_name, first_player_reasoning_action_steps, board, "", legal_moves, gen_move,illegal_tolerance, True, hook_functions,0,board=board,legal_move_list=[move.uci() for move in legal_moves])
					total_tokens += added_tokens
				elif turn == False: # black
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
			with open(f"chess_archive/chess_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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