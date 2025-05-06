from spinbench.tools.chat_service import get_chat
import regex
import json

json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)

def parse_game_state(state_str):
	"""
	Parse the game state observation string into a detailed representation.
	
	Args:
		state_str (str): The raw observation string.
		
	Returns:
		dict: A structured representation containing:
			- objective (int): The player's coin objective (0=a,1=b,2=c,...).
			- colors (list of str): List of coin colors in order.
			- collected (dict): Mapping of player -> dict of color -> count collected.
			- board (list of list of str): 2D grid of contents.
			- player_positions (dict): Mapping of player index -> (row, col).
			- coin_positions (dict): Mapping of color -> list of (row, col).
	"""
	lines = state_str.strip().splitlines()
	
	# Parse the objective
	objective = int(lines[0].strip())
	
	# Parse the header line for coin colors
	color_line = lines[1].strip()
	colors = color_line.split()
	
	# Parse collected table
	collected = {}
	idx = 2
	while lines[idx].startswith("player"):
		parts = lines[idx].split()
		player = parts[0]
		counts = list(map(int, parts[1:]))
		collected[player] = dict(zip(colors, counts))
		idx += 1
	
	# Now lines[idx] should be the top border of the board
	# Determine board width from border line e.g. +--------+
	border = lines[idx]
	width = len(border) - 2
	idx += 1
	
	# Parse board rows until the next border line
	board = []
	player_positions = {}
	coin_positions = {color: [] for color in colors}
	row = 0
	while not lines[idx].startswith("+"):
		line = lines[idx]
		# Extract content between '|' characters
		content = line[1:-1]
		# Pad or trim to expected width
		if len(content) < width:
			content = content.ljust(width)
		elif len(content) > width:
			content = content[:width]
		row_cells = list(content)
		board.append(row_cells)
		
		# Record positions
		for col, ch in enumerate(row_cells):
			if ch.isdigit():  # player
				player_positions["player"+str(ch)] = (row, col)
			elif ch.isalpha():  # coin
				# Lowercase letter; map to color by index (ord - ord('a'))
				color_idx = ord(ch) - ord('a')
				if 0 <= color_idx < len(colors):
					coin_positions[colors[color_idx]].append((row, col))
		row += 1
		idx += 1

	# Build text description
	lines_desc = []
	lines_desc.append(f"Objective color: {colors[objective]}")
	lines_desc.append("Collected coins so far:")
	for player, counts in collected.items():
		cnt_str = ", ".join(f"{col} = {cnt}" for col, cnt in counts.items())
		lines_desc.append(f" - {player}: {cnt_str}")
	lines_desc.append("Player positions:")
	for p, pos in player_positions.items():
		lines_desc.append(f" - {p} at row {pos[0]}, column {pos[1]}")
	lines_desc.append("Remaining coins on the board:")
	for col in colors:
		pos_list = ", ".join(str(pos) for pos in coin_positions[col])
		lines_desc.append(f" - {col}-coins at {pos_list}")
	lines_desc.append("Board layout (rows 0–7, cols 0–7; '.' = empty):")
	for r, row_cells in enumerate(board):
		row_str = " ".join(ch if ch != ' ' else '.' for ch in row_cells)
		player_mark = ""
		for p, pos in player_positions.items():
			if pos[0] == r:
				player_mark = f"  ← {p} at {pos}"
				break
		lines_desc.append(f" Row {r}: {row_str}{player_mark}")
	
	text_description = "\n".join(lines_desc)
	
	return {
		"objective": colors[objective],
		"collected": collected,
		"board": board,
		"player_positions": player_positions,
		"coin_positions": coin_positions,
	}, text_description


def generate_state_description(observation):
	json_desc, text_desc = parse_game_state(observation)
	return f"""
Below is the current detailed state information. 

Game state:
{text_desc}

JSON representation of the game state:
{json_desc}
"""


def gen_initial_prompt():
	return """
You are an expert in the Coin Game—a fully cooperative multi-agent task on an 8×8 grid. Two agents work together to collect coins of two 'positive' colors while avoiding a third 'negative' color. Your aim is to maximize the shared reward by combining your own goal color with your partner’s.

Game Overview:
- Grid: 8 rows × 8 columns.
- Coins: 12 total, 4 of each color (a, b, c).
- Goals: At start, you and your teammate are each secretly assigned one 'Self' color (e.g. you → color a, teammate → color b). The remaining color is 'Neither' and yields a penalty if collected.
- Turns: 20 steps total (10 per agent), alternating moves.
- Actions: move up, down, left, right, or stand.
- Collection: Stepping onto a coin removes it and attributes it to the collector.

Reward (end of game):
	R = (self coins)**2 + (other coins)**2 − (neither coins)**2
Where:
	- self coins: you and your teammate’s Self coins collected.
	- other coins: you and your teammate’s Other coins collected.
	- neither coins: you and your teammate’s Neither coins collected.
- The goal is to maximize the squared reward at the end of 20 steps.

Key Objectives:
1. **Collect Self & Other coins**:  
   • Maximize both your own and your teammate’s goal colors—each counts positively.  
2. **Avoid Neither coins**:  
   • Any Neither coin you pick up or your teammate picks up reduces total reward.  
3. **Infer early**:  
   • Observe teammate moves to guess their goal color, then target those coins cooperatively.  
4. **Coordinate movement**:  
   • Plan paths on the grid to reach high‐value coins (Self & Other) efficiently.  
   • Use 'stand' strategically to let your teammate move first when uncertain or to avoid collisions.

Your Role:
Work with your teammate to collect as many Self & Other coins as possible while avoiding Neither coins. Use the board observation to plan moves, infer your partner’s goal, and maximize the squared reward at the end of 20 steps.  
"""


def generate_action_prompt(legal_moves_dict, history_information):
	return f"""
Here is some history information of this game state:
{history_information}

Please think step by step based on the current Coin Game state.

# Think step by step

## 1. Understand Your Own Goal
- You know your assigned color (Self). Identify which coins on the board match your color.
- Prioritize collecting your Self-color coins to increase your share of the 'self' term in the reward.
- Remember: each Self coin you collect contributes squared to the final reward.

## 2. Infer Your Teammate’s Goal Early
- Observe your teammate’s past moves and which coins they have been targeting.
- Hypothesize their goal color (Other) as soon as you see consistent behavior.
- Use that inference to guide your own path: collecting Other-color coins also adds to the total reward.

## 3. Avoid 'Neither' Coins
- Any coin whose color matches neither your Self nor inferred Other is a 'Neither' coin.
- Collecting Neither coins will be penalized (subtracts squared), so you should avoid them at all costs.
- If you’re uncertain about the other’s goal, be especially cautious around ambiguous coins.

## 4. Plan Your Path on the Grid
- Map out distances: compute Manhattan distance from your position to nearby Self and Other coins.
- Balance immediate gains (close Self coins) with high-value cooperative gains (Other coins).
- If two targets are equidistant, prefer the one that helps confirm your teammate’s goal (e.g., if you’re still uncertain).

## 5. Use stand Strategically
- If moving now would put you on a Neither coin or ruin a better future opportunity, consider stand to let your teammate move first.
- Stand can also buy time to gather more information about the other’s goal.

## Legal Actions
You can choose from the following legal actions (mapping of action id to description):
{legal_moves_dict}

Based on the above chain of thought and the list of legal actions, pick the action that maximizes your cooperative reward. Remember to weigh Self vs Other vs Neither.

Your output must be valid JSON with exactly two fields, both in double quotes:
{{"reason": string, "action": int}}
"""


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
				parsed_json = json.loads(match)
		action = int(parsed_json["action"])
		reason = parsed_json["reason"]
		move = action
	except Exception as e:
		print(e)
		move = None
		action = None
		reason = None
	return move, content, used_token, action, reason



def parse_legal_actions(state, legal_actions):
	mapping = {}
	for a in legal_actions:
		mapping[a] = state.action_to_string(state.current_player(), a)
	return mapping

