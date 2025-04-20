
"""
The version that tracks scores for each column and action
"""
import os
import time
import sys
import re
import regex
import sys
sys.path.append(os.path.abspath("../"))
import json
from pettingzoo.classic import connect_four_v3
import random
import time
from chat_service import get_chat,fix_json
from play_service import (
    play,
    create_hook_functions,
)
import argparse
parser = argparse.ArgumentParser(description="Set model name for player1_model")
parser.add_argument('--model', type=str, required=True, help="Specify the model name (e.g., gpt-4o)")
args = parser.parse_args()
import requests # to fetch scores from engine

# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)


def build_pos_string(move_history):
    """
    Function to get position and send to api
    Returns a string of columns in solver’s 1-based format
    """
    return "".join(str(m + 1) for m in move_history)


def fetch_scores_from_solver(pos_str):
    """
    Sends the current position string (pos_str) to connect4.gamesolver.org
    and returns the 'score' array from the JSON response.

    pos_str: a string of digits (each 1..7), e.g. '4012'
             representing the columns chosen so far, in 1-based indexing.
    """
    url = "http://cnyaojz.com:5000/solve"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ),
        "Referer": "https://connect4.gamesolver.org/",
        "Origin": "https://connect4.gamesolver.org",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    }
    full_url = f"{url}?pos={pos_str}"

    try:
        response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("score", [])
        else:
            print(f"Error fetching scores: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error fetching scores: {e}")
        return []


parser = argparse.ArgumentParser(description="Set model name for player1_model")
parser.add_argument('--model', type=str, required=True, help="Specify the model name (e.g., gpt-4o)")
args = parser.parse_args()

def generate_action_prompt(legal_moves):
    action_prompt = f"""
Now it's your move. Please enter the index of the column where you would like to place your token (0-6 from left to right), except the illegal position. You should serialize the output to a json object with the key "reason" and the value str as the detailed reason for your action, and the key "action" and the value as the index of the column where you would like to place your token. The legal moves are: \n<legal_moves>\n{" ".join([str(move) for move in legal_moves])}\n</legal_moves>\n You must select one legal move from this list. You have to win.  Your output should be {{"reason": "your reason", "action": "action index"}}, and you can only use json valid characters. When you write json, all the elements (including all the keys and values) should be enclosed in double quotes!!!
"""
    return action_prompt

def generate_reasoning_prompt(player_reasoning_action_steps):
    li = [f"Move: {step['action']}\nReason: {step['reason']}" for step in player_reasoning_action_steps[-3:]]
    steps = "\n---------------------------\n".join(li)
    return f"""
Your previous moves and thinking are below  (in the last 3 moves in the order of the oldest to the newest):
<previous_moves>
{steps}
</previous_moves>
"""

def parse_observation(observation_dict, agent):
    """
    This function takes the observation dictionary from the PettingZoo environment
    Returns a text description of the current game state and legal moves
    """

    observation = observation_dict['observation']
    action_mask = observation_dict['action_mask']

    player_0_grid = observation[:, :, 0]
    player_1_grid = observation[:, :, 1]

    if agent == "player_0":
        player_mark = "X "
        opponent_mark = "O "
    elif agent == "player_1":
        player_mark = "O "
        opponent_mark = "X "

    X_places = []
    O_places = []

    grid_description = "Current game state:\n"
    for row in range(6):
        row_description = "r" + str(row) + " "
        for col in range(7):
            if player_0_grid[row, col] == 1:
                row_description += player_mark  
                if agent == "player_0":
                    X_places.append((row, col))
                else:
                    O_places.append((row, col))
            elif player_1_grid[row, col] == 1:
                row_description += opponent_mark  
                if agent == "player_0":
                    O_places.append((row, col))
                else:
                    X_places.append((row, col))
            else:
                row_description += "- "  # Empty cell
        grid_description += row_description.strip() + "\n"
    grid_description += "   " + " ".join(["c0", "c1", "c2", "c3", "c4", "c5", "c6"]) + "\n"

    grid_description += f"""
r0 means row 0, r1 means row 1, and so on.
c0 means column 0, c1 means column 1, and so on.

Token places(row index, column index): 
X tokens are at places: {X_places}
O tokens are at places: {O_places}
"""

    legal_moves_description = "Legal actions (columns where you can drop a token):\n"
    legal_moves = [i for i, is_legal in enumerate(action_mask) if is_legal == 1]
    legal_moves_description += ", ".join([str(col) for col in legal_moves])

    full_description = f"{grid_description}\n{legal_moves_description}"

    return grid_description + "\n", legal_moves_description + "\n", legal_moves

def gen_move(player_messages, player_model):
    content, used_token = get_chat(player_model, player_messages)
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

init_player1_model = {
    "model": args.model,
    "prompt_config": [
        {
            "name": "forced-reasoning",
            "params": {
                "interactive_times": 1,
                "prompt_messages": [
                    "Please reason about the current state. You should analyze all the opponent's moves and your moves, try to reason opponent's thought in detail. Only need to plan and reason now, no need to make move at this stage."
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
                    "Please reason about the current state. You should analyze all the opponent's moves and your moves, try to reason opponent's thought in detail. Only need to plan and reason now, no need to make move at this stage."
                ]
            }
        }
    ]
}

if not os.path.exists("cf_archive"):
    os.mkdir("cf_archive")

for game_index in range(4):
    player1_model = init_player1_model
    player2_model = init_player2_model

    if game_index >= 2:
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
    filename = f"cf_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
    print(filename)
    if os.path.exists(f"cf_archive/{filename}"):
        print(f"Deleting existing file: {filename}")
        os.remove(f"cf_archive/{filename}")

    first_player_initial_prompt = """
    You are playing a game of Connect Four against an opponent. Connect Four is a 2-player turn based game, where players must connect four of their tokens vertically, horizontally or diagonally. The players drop their respective token in a column of a standing grid, where each token will fall until it reaches the bottom of the column or reaches an existing token. Players cannot place a token in a full column, and the game ends when either a player has made a sequence of 4 tokens, or when all 7 columns have been filled. Taking an illegal move ends the game and the player who made the illegal move loses.
    The board is a 6x7 grid, and you are playing as 'X'. The opponent is playing as 'O'. 
    The action space is the set of integers from 0 to 6 (inclusive), from left to right, where the action represents which column a token should be dropped in.
    """

    second_player_initial_prompt = """
    You are playing a game of Connect Four against an opponent. Connect Four is a 2-player turn based game, where players must connect four of their tokens vertically, horizontally or diagonally. The players drop their respective token in a column of a standing grid, where each token will fall until it reaches the bottom of the column or reaches an existing token. Players cannot place a token in a full column, and the game ends when either a player has made a sequence of 4 tokens, or when all 7 columns have been filled. Taking an illegal move ends the game and the player who made the illegal move loses.
    The board is a 6x7 grid, and you are playing as 'O'. The opponent is playing as 'X'. 
    The action space is the set of integers from 0 to 6 (inclusive), from left to right, where the action represents which column a token should be dropped in.
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

    env = connect_four_v3.env(render_mode="rgb_array")
    env.reset(seed=42)
    win = None 
    total_tokens = 0
    game_log = []
    move_history = []

    for agent in env.agent_iter():
        hook_functions = {}
        observation, reward, termination, truncation, info = env.last()
        grid_description, legal_moves_description, legal_moves = parse_observation(observation, agent)
        rewards = env.rewards
        pos_str = build_pos_string(move_history)
        print(rewards)
        print(grid_description)

        if win is not None:
            break

        if win is None:
            if len(list(rewards.keys())) == 1 and rewards[list(rewards.keys())[0]] == 0:
                print("Draw!")
                win = 2
                break
            elif rewards["player_0"] == 1 and rewards["player_1"] == 1:
                print("Draw!")
                win = 2
                break
            elif rewards["player_0"] == 1 and rewards["player_1"] == -1:
                print("Player 1 wins!")
                win = 0
                break
            elif rewards["player_0"] == -1 and rewards["player_1"] == 1:
                print("Player 2 wins!")
                win = 1
                break
            elif rewards["player_0"] == -1 and rewards["player_1"] == 0:
                print("Player 1 illegal move!")
                win = 3
                break
            elif rewards["player_0"] == 0 and rewards["player_1"] == -1:
                print("Player 2 illegal move!")
                win = 4
                break

        illegal_tolerance = 10
        if termination or truncation:
            action = None
        else:
            # Get the solver scores first!
            solver_scores = fetch_scores_from_solver(pos_str)
            print(solver_scores)

            if agent == 'player_0':
                if player1_model_name == "human":
                    print(grid_description + "\n" + generate_action_prompt(legal_moves))
                    move = int(input("You are playing as 'X', Enter your move: "))
                    action = move
                else:
                    first_player_messages = first_player_messages[:2]
                    hook_functions = create_hook_functions(
                        player1_model,
                        first_player_reasoning_action_steps,
                        "Your opponent has made the move, and now the state is: \n" + grid_description + "\n",
                        generate_action_prompt(legal_moves)
                    )
                    move, action, win, game_state, added_tokens = play(
                        first_player_messages, 
                        first_player_store_message, 
                        player1_model_name, 
                        first_player_reasoning_action_steps, 
                        grid_description, 
                        legal_moves_description, 
                        legal_moves, 
                        gen_move, 
                        illegal_tolerance,
                        True, 
                        hook_functions,
                        0
                    )
                    total_tokens += added_tokens

            elif agent == 'player_1':
                if player2_model_name == "human":
                    print(grid_description + "\n" + generate_action_prompt(legal_moves))
                    move = int(input("You are playing as 'O', Enter your move: "))
                    action = move 
                else:
                    second_player_messages = second_player_messages[:2]
                    hook_functions = create_hook_functions(
                        player2_model,
                        second_player_reasoning_action_steps,
                        "Your opponent has made the move, and now the state is: \n" + grid_description + "\n",
                        generate_action_prompt(legal_moves)
                    )
                    move, action, win, game_state, added_tokens = play(
                        second_player_messages, 
                        second_player_store_message, 
                        player2_model_name, 
                        second_player_reasoning_action_steps, 
                        grid_description, 
                        legal_moves_description, 
                        legal_moves, 
                        gen_move, 
                        illegal_tolerance,
                        True, 
                        hook_functions,
                        1
                    )
                    total_tokens += added_tokens

        chosen_score = None
        if action is not None:
            move_history.append(action)  
        if action is not None and solver_scores and 0 <= action < len(solver_scores):
            chosen_score = solver_scores[action]
        
        game_log.append({
            "agent": agent,
            "action": action,
            "observation": observation["observation"].tolist(),
            "reward": env.rewards,
            "action_mask": observation["action_mask"].tolist(),
            "solver_scores": solver_scores,
            "chosen_score": chosen_score
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

    if win is None:
        win = 2

    with open(f"cf_archive/cf_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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
            "number_of_requests": len(game_log) / 2,
            "game_log": game_log,
            "first_player_messages": first_player_store_message,
            "second_player_messages": second_player_store_message,
        }, f, indent=4)