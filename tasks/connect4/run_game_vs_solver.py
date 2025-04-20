import os
import time
import regex
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import json
from pettingzoo.classic import connect_four_v3
import random
import requests
import time
from tools.chat_service import get_chat,fix_json
from utils.play_service import (
    play,
    create_hook_functions,
)

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
    and returns a text description of the current game state and legal moves.
    """
    # Extract observation and action mask
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

    # Create text description for the current game state
    grid_description = "Current game state:\n"
    for row in range(6):
        row_description = "r" + str(row) + " "
        for col in range(7):
            if player_0_grid[row, col] == 1:
                row_description += player_mark  # Represent player 0's token with 'X'
                if agent == "player_0":
                    X_places.append((row, col))
                else:
                    O_places.append((row, col))
            elif player_1_grid[row, col] == 1:
                row_description += opponent_mark  # Represent player 1's token with 'O'
                if agent == "player_0":
                    O_places.append((row, col))
                else:
                    X_places.append((row, col))
            else:
                row_description += "- "  # Empty cell with '-'
        grid_description += row_description.strip() + "\n"
    grid_description += "   "+" ".join(["c0", "c1", "c2", "c3", "c4", "c5", "c6"]) + "\n"

    grid_description += f"""
r0 means row 0, r1 means row 1, and so on.
c0 means column 0, c1 means column 1, and so on.

Token places(row index, column index): 
X tokens are at places: {X_places}
O tokens are at places: {O_places}
"""

    # Create text description for legal moves
    legal_moves_description = "Legal actions (columns where you can drop a token):\n"
    legal_moves = [i for i, is_legal in enumerate(action_mask) if is_legal == 1]
    legal_moves_description += ", ".join([str(col) for col in legal_moves])

    # Combine the two descriptions
    full_description = f"{grid_description}\n{legal_moves_description}"
    
    return grid_description + "\n", legal_moves_description + "\n", legal_moves


def fetch_scores_from_solver(pos_str):
    """
    Sends the current position string (pos_str) to connect4.gamesolver.org
    and returns the 'score' array from the JSON response.

    pos_str: a string of digits (each 1..7), e.g. '4012'
             representing the columns chosen so far, in 1-based indexing.
    """
    url = "http://localhost:5000/solve"
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

player_list_json = json.load(open("solver-list-single.json","r"))
player1_model_list = player_list_json["player1_model_list"]
player2_model_list = player_list_json["player2_model_list"]

print(len(player1_model_list))
print(len(player2_model_list))
for i in range(len(player1_model_list)):
    print(player1_model_list[i]["model"], "vs", player2_model_list[i]["model"])
    
assert len(player1_model_list) == len(player2_model_list)

for model_index in range(len(player1_model_list)):
    for game_index in range(10):
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
        filename = f"cf_solver/cf_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
        reverse_filename = f"cf_solver/cf_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
        if os.path.exists(filename) or os.path.exists(reverse_filename):
            print("File exists", filename)
            time.sleep(1)
            continue

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
        win = None # 0 is player1, 1 is player2, 2 is Draw, 3 is player1 illegal move, 4 is player2 illegal move
        total_tokens = 0
        
        game_log = []
        pos_str = ""  # Track all moves so far in 1-based notation

        for agent in env.agent_iter():
            hook_functions = {}
            observation, reward, termination, truncation, info = env.last()
            grid_description, legal_moves_description, legal_moves = parse_observation(observation, agent)
            print(type(legal_moves[0]))
            print(grid_description)
            rewards = env.rewards
            print(rewards)
            if win != None:
                break
            if win == None:
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
                if agent == "player_0":
                    # Check the *model name* for player 0
                    if player1_model_name == "our_solver":
                        score_list = fetch_scores_from_solver(pos_str)
                        if not score_list:
                            move = legal_moves[0]
                        else:
                            max_score = max(score_list)
                            max_score_index_list = [i for i, j in enumerate(score_list) if j == max_score]
                            max_index = random.choice(max_score_index_list)
                            move = max_index  
                        action = move
                        pos_str += str(move + 1)
                    elif player1_model_name == "random":
                        move = random.choice(legal_moves)
                        action = move
                        pos_str += str(move + 1)
                    else:
                        # lm gen_move
                        first_player_messages = first_player_messages[:2]
                        hook_functions = create_hook_functions(
                            player1_model,
                            first_player_reasoning_action_steps,
                            "Your opponent has made the move, and now the state is:\n" + grid_description + "\n",
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
                        pos_str += str(move + 1)

                elif agent == "player_1":
                    # Check the *model name* for player 1
                    if player2_model_name == "our_solver":
                        score_list = fetch_scores_from_solver(pos_str)
                        if not score_list:
                            move = legal_moves[0]
                        else:
                            max_score = max(score_list)
                            max_score_index_list = [i for i, j in enumerate(score_list) if j == max_score]
                            max_index = random.choice(max_score_index_list)
                            move = max_index

                        action = move
                        pos_str += str(move + 1)
                    elif player2_model_name == "random":
                        move = random.choice(legal_moves)
                        action = move
                        pos_str += str(move + 1)
                    else:
                        # lm gen_move
                        second_player_messages = second_player_messages[:2]
                        hook_functions = create_hook_functions(
                            player2_model,
                            second_player_reasoning_action_steps,
                            "Your opponent has made the move, and now the state is:\n" + grid_description + "\n",
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

                        # Update pos_str for solver's record
                        pos_str += str(move + 1)

            game_log.append({
                "agent": agent,
                "action": action,
                "observation": observation["observation"].tolist(),
                "reward": env.rewards,
                "action_mask": observation["action_mask"].tolist(),
            })
            try:
                env.step(move)
            except Exception as e:
                print("Error stepping the environment", e)
                break
        env.close()


        player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
        player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
        player1_model_save_name = player1_model_save_name.replace("/", "_")
        player2_model_save_name = player2_model_save_name.replace("/", "_")
        print(player1_model_save_name, player2_model_save_name)
        if win == None:
            win = 2
        # save the chat log for two players
        with open(f"cf_solver/cf_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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
                "game_log": game_log,
                "first_player_messages": first_player_store_message,
                "second_player_messages": second_player_store_message,
            }, f, indent=4)