import json
import regex
import chess
from spinbench.tools.chat_service import get_chat, fix_json
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)

######################################
############ prompt utils ############
######################################

first_player_initial_prompt = f"""
You are playing a text game of Chess against an opponent. Chess is a two-player strategy board game played on an 8x8 board. The goal of the game is to checkmate the opponent's king. On the board, your pieces are represented by uppercase letters and the opponent's pieces are represented by lowercase letters. You are a chest master playing a text based game of chess.
"""

second_player_initial_prompt = f"""
You are playing a text game of Chess against an opponent. Chess is a two-player strategy board game played on an 8x8 board. The goal of the game is to checkmate the opponent's king. On the board, your pieces are represented by lowercase letters and the opponent's pieces are represented by uppercase letters. You are a chest master playing a text based game of chess.
"""

def get_initial_player_messages():
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
    return first_player_messages, second_player_messages


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


def generate_action_prompt(legal_moves):
			return f"""
	Please enter your move in Universal Chess Interface (UCI) format. For example, to move a pawn from e2 to e4, you would enter \"e2e4\". You should state your reason first, and serialize the output to a json object with the key "reason" and the value as a string of your reason, the key "action" and the value as a UCI string representing your move. The legal moves are: \n<legal_moves>\n{" ".join(legal_moves)}\n</legal_moves>\n You must select one legal move from this list and respond with the UCI format of the move you choose. Do not generate any move outside of this list. You have to win. In your reason and action, you can only use UCI format to describe. Your output should be in this format: {{"reason": "your reason", "action": "your action"}}, and you can only use json valid characters. When you write json, all the elements (including all the keys and values) should be enclosed in double quotes!!!
	"""

######################################
########### running utils ############
######################################

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

