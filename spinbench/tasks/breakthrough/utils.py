import json
import regex
from spinbench.tools.chat_service import get_chat,fix_json

json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)

def parse_game_state(state_str):
    """
    Parse the breakthrough board state string into a human-readable description.
    Supports observations like:
      Current player:  0
      4bbbb
      3....
      2....
      1wwww
       abcd
    """
    lines = state_str.strip().splitlines()
    # Remove any header lines (e.g., "Current player")
    board_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip lines with non-board info
        if stripped.startswith("Current player") or not stripped:
            continue
        # Collect rank rows and file label line
        board_lines.append(stripped)

    if not board_lines:
        return "No board state available."

    # The last line is file labels, e.g. "abcd"
    file_labels = list(board_lines[-1])
    rank_rows = board_lines[:-1]

    white_positions = []
    black_positions = []
    # Each rank row: first char is rank, rest are cells
    for row in rank_rows:
        rank = row[0]
        cells = row[1:]
        for idx, cell in enumerate(cells):
            if idx >= len(file_labels):
                break
            file = file_labels[idx]
            if cell == 'w':
                white_positions.append(f"{file}{rank}")
            elif cell == 'b':
                black_positions.append(f"{file}{rank}")

    desc_lines = []
    desc_lines.append(f"White pawns at: {', '.join(white_positions) if white_positions else 'none'}." )
    desc_lines.append(f"Black pawns at: {', '.join(black_positions) if black_positions else 'none'}." )
    return "\n".join(desc_lines)

# Initial system prompt for breakthrough

first_player_initial_prompt = """
You are a master of Breakthrough. Breakthrough is an 8x8 abstract strategy game. Each player begins with two rows of pawns: White on ranks 1-2, Black on ranks 7-8. Black moves first.

Moves:
- A pawn may move one step straight forward into an empty square.
- Or diagonally forward into an empty square.
- Or diagonally forward onto an opponent pawn, capturing it.

Objective:
- Be the first to advance any pawn to the opponent's back rank (White to rank 8, Black to rank 1). If all enemy pawns are captured, you also win.

You cannot move backwards or sideways. Work to create breakthroughs and block opponent's advances. Use strategic captures and pawn chains.

You are playing as Black. On the board, your pieces are represented by 'b' and the opponent's pieces are represented by 'w'. You are a master of Breakthrough and you are playing a text based game of Breakthrough.
"""

second_player_initial_prompt = """
You are a master of Breakthrough. Breakthrough is an 8x8 abstract strategy game. Each player begins with two rows of pawns: White on ranks 1-2, Black on ranks 7-8. Black moves first.

Moves:
- A pawn may move one step straight forward into an empty square.
- Or diagonally forward into an empty square.
- Or diagonally forward onto an opponent pawn, capturing it.

Objective:
- Be the first to advance any pawn to the opponent's back rank (White to rank 8, Black to rank 1). If all enemy pawns are captured, you also win.

You cannot move backwards or sideways. Work to create breakthroughs and block opponent's advances. Use strategic captures and pawn chains.

You are playing as White. On the board, your pieces are represented by 'w' and the opponent's pieces are represented by 'b'. You are a master of Breakthrough and you are playing a text based game of Breakthrough.
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

def generate_state_description(observation: str) -> str:
    desc = parse_game_state(observation)
    return f"Below is the current board state for Breakthrough.\n\nGame State:\n{observation}\n\n{desc}\n"


def generate_action_prompt(legal_moves_dict: dict) -> str:
    # COT and action prompt for breakthrough
    moves_list = json.dumps(legal_moves_dict, indent=2)
    return f'''
Please think step by step based on the current state.

# Think step by step

1. Evaluate Winning Moves
- Check if any legal move advances a pawn to the back rank for an immediate win.
- Or captures an opponent pawn creating a path to promotion.

2. Assess Tactical Captures
- Identify diagonal captures that open lines or remove blockaders.
- Consider whether captures expose your pawn to immediate recapture.

3. Advance Key Pawns
- Push central pawns to create multiple threats.
- Avoid isolated side-pawns that can be easily blocked.

4. Defensive Considerations
- Block opponent advanced pawns by interposing or capturing.
- Keep pawn chains intact to support advances.

Now it's your turn. You can choose one of the legal actions provided below. Output your choice exactly as one of the action descriptions.

The legal actions are: (This is a dict of action id and action description)
{moves_list}

Your output must be a JSON object: {{"reason": string, "action": int}}. Use double quotes for all keys and values.'''


def parse_legal_actions(state, legal_actions):
    mapping = {}
    for a in legal_actions:
        mapping[a] = state.action_to_string(state.current_player(), a)
    return mapping


def gen_move(player_messages, player_model):
    content, used_token = get_chat(player_model, player_messages)
    print("player_messages:", player_messages)
    print("model's response:", content)
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