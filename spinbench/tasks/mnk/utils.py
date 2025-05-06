from spinbench.tools.chat_service import get_chat, fix_json
import regex
import json

json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)

def parse_game_state(state_str, m, n, k):
	"""
	Parse an m×n k-in-a-row game state into structured and textual descriptions.
	Args:
		state_str (str): Multiline string of the board using '.', 'x', and 'o'.
		m (int): Number of rows.
		n (int): Number of columns.
		k (int): Number in a row needed to win.
	Returns:
		tuple:
		  - dict: Structured representation with:
			  * m, n, k
			  * board (list of list of str)
			  * x_positions, o_positions (lists of (row, col))
			  * x_count, o_count
			  * next_player ('x' or 'o')
		  - str: Textual description
	"""
	# Build board
	lines = state_str.strip().splitlines()
	board = [list(line.ljust(n, '.'))[:n] for line in lines]

	# Locate pieces
	x_positions = []
	o_positions = []
	for i, row in enumerate(board):
		for j, ch in enumerate(row):
			if ch == 'x':
				x_positions.append((i, j))
			elif ch == 'o':
				o_positions.append((i, j))

	# Counts
	x_count = len(x_positions)
	o_count = len(o_positions)

	# Determine next player
	next_player = 'x' if x_count == o_count else 'o'

	# Legal moves: empty cells

	# Structured dict
	structured = {
		'm': m,
		'n': n,
		'k': k,
		'board': board,
		'x_positions': x_positions,
		'o_positions': o_positions,
		'x_count': x_count,
		'o_count': o_count,
		'next_player': next_player,
	}

	# Text description
	desc = []
	desc.append(f"Board size: {m} rows × {n} cols; need {k} in a row to win.")
	desc.append(f"Crosses ('x'): {x_count} at positions {x_positions}")
	desc.append(f"Noughts ('o'): {o_count} at positions {o_positions}")
	desc.append(f"Next to move: '{next_player}'")
	desc.append("Current board:")
	for i, row in enumerate(board):
		row_str = ' '.join(ch for ch in row)
		desc.append(f" Row {i}: {row_str}")
	text_desc = "\n".join(desc)

	return structured, text_desc

first_player_initial_prompt = """
You are a master of the m,n,k-game (an abstract strategy game generalizing Tic-Tac-Toe).
The board has m rows and n columns, and the goal is to connect k of your pieces in a straight line (horizontal, vertical, or diagonal).
Players take turns placing one of their pieces on any empty cell. First player uses 'x', second player uses 'o'.
The winner is the player who first gets k stones of their own color in a row, horizontally, vertically, or diagonally. If the board fills without a winner, the game is a draw.
You play as the first player, 'x'. On the board, your pieces are 'x', your opponent’s are 'o', and empty cells are '.'.
Think strategically about your placement to build towards k in a line while blocking your opponent.
"""

second_player_initial_prompt = """
You are a master of the m,n,k-game (an abstract strategy game generalizing Tic-Tac-Toe).
The board has m rows and n columns, and the goal is to connect k of your pieces in a straight line (horizontal, vertical, or diagonal).
Players take turns placing one of their pieces on any empty cell. First player uses 'x', second player uses 'o'.
The winner is the player who first gets k stones of their own color in a row, horizontally, vertically, or diagonally. If the board fills without a winner, the game is a draw.
You play as the second player, 'o'. On the board, your pieces are 'o', your opponent’s are 'x', and empty cells are '.'.
Think strategically about your placement to build towards k in a line while blocking your opponent.
"""

def get_initial_player_messages():
	first_player_messages = [
		{
			"role": "user",
			"content": first_player_initial_prompt,
		},
		{
			"role": "assistant",
			"content": "Sure, let's start.",
		},
	]
	second_player_messages = [
		{
			"role": "user",
			"content": second_player_initial_prompt,
		},
		{
			"role": "assistant",
			"content": "Sure, let's start.",
		},
	]
	return first_player_messages, second_player_messages

def generate_state_description(observation: str, m,n,k) -> str:
	json_desc, text_desc = parse_game_state(observation, m, n, k)
	return f"""
Below is the current detailed state information. 

Game state:
{text_desc}

JSON representation of the game state:
{json_desc}
"""

def generate_action_prompt(legal_moves_dict: dict, m: int, n: int, k: int) -> str:
	"""
	Build a chain-of-thought prompt for the m,n,k-game given its legal moves.
	
	Args:
		legal_moves_dict (dict): Mapping from action id to action description (e.g. "(row,col)").
		m (int): Number of rows.
		n (int): Number of columns.
		k (int): Number needed to win.
	
	Returns:
		str: A detailed CoT prompt ending with the serialized legal moves.
	"""
	moves_list = json.dumps(legal_moves_dict, indent=2)
	return f"""
Please think step by step based on the current m={m}, n={n}, k={k} game state.

# Think step by step

1. Evaluate Immediate Win Opportunities
- For each legal move, simulate placing your token and check if it completes a line of length {k} in any direction (horizontal, vertical, diagonal).
- If such a move exists, it wins the game instantly.

2. Block Opponent’s Threats
- Identify any cell where your opponent could play next turn to achieve {k} in a line.
- Prioritize moves that directly occupy or interrupt those threat lines.

3. Build Multiple Threats
- Seek placements that create two or more simultaneous 'k−1' alignments, forcing opponent into defensive play.
- Favor moves that intersect shared lines, maximizing future winning routes.

4. Control Key Regions
- Center and near-center cells often yield more directional options; consider them for flexibility.
- On larger boards, aim to dominate long open lines or central diagonals.

5. Maintain Balance Between Attack and Defense
- Avoid moves that open up a direct winning threat for the opponent on their next turn.
- Preserve existing your token's alignments; don't scatter pieces too thinly.

Now it’s your turn. From the list of legal actions below, choose the one you deem best. 

Output **exactly** a JSON object with two keys:  
- `"reason"`: your concise rationale (in several sentences).  
- `"action"`: the integer action id corresponding to your chosen move.

The legal actions are:
{moves_list}

Your output must be valid JSON, using double quotes for keys and string values."""


def parse_legal_actions(state, legal_actions):
	mapping = {}
	for a in legal_actions:
		mapping[a] = state.action_to_string(state.current_player(), a)
	return mapping


def gen_move(player_messages, player_model):
	content, used_token = get_chat(player_model, player_messages)
	for m in player_messages:
		print(m["role"])
		print(m["content"])
		print("*"*30)
	print("model's response:",content)
	print("*"*30)
	try:
		parsed_json = None
		matches = json_pattern.findall(content)
		for match in matches:
			try:
				parsed_json = json.loads(match)
				print("Valid JSON Found:", parsed_json)
			except Exception as e:
				print("Invalid JSON Found:", match)
				parsed_json = json.loads(fix_json(match))
		action = int(parsed_json["action"])
		reason = parsed_json["reason"]
		move = action
	except Exception as e:
		print(e)
		move = None
		action = None
		reason = None
	return move, content, used_token, action, reason