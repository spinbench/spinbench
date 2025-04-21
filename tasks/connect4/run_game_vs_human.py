
"""
The version that tracks scores for each column and action
"""
import os
import regex
import sys
import json
from pettingzoo.classic import connect_four_v3
import time
from tools.play_service import (
    play,
    create_hook_functions,
)
from tasks.connect4.utils import (
	generate_action_prompt,
	gen_move,
	get_initial_player_messages,
	check_win,
	parse_observation,
    fetch_scores_from_solver,
)
import argparse

# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)


def build_pos_string(move_history):
    """
    Function to get position and send to api
    Returns a string of columns in solver’s 1-based format
    """
    return "".join(str(m + 1) for m in move_history)

def generate_reasoning_prompt(player_reasoning_action_steps):
    li = [f"Move: {step['action']}\nReason: {step['reason']}" for step in player_reasoning_action_steps[-3:]]
    steps = "\n---------------------------\n".join(li)
    return f"""
Your previous moves and thinking are below  (in the last 3 moves in the order of the oldest to the newest):
<previous_moves>
{steps}
</previous_moves>
"""

def run_game_vs_human(store_folder, total_rounds=4, model_name="gpt-4o"):
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

    for game_index in range(total_rounds):
        player1_model = init_player1_model
        player2_model = init_player2_model

        if game_index >= total_rounds // 2:
            player1_model, player2_model = player2_model, player1_model

        player1_model_name = player1_model["model"]
        player2_model_name = player2_model["model"]
        player1_model_save_name = player1_model_name + "-" + "-".join([i["name"] for i in player1_model["prompt_config"]])
        player2_model_save_name = player2_model_name + "-" + "-".join([i["name"] for i in player2_model["prompt_config"]])
        player1_model_save_name = player1_model_save_name.replace("/", "_")
        player2_model_save_name = player2_model_save_name.replace("/", "_")
        filename = f"{store_folder}/cf_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json"
        reverse_filename = f"{store_folder}/cf_{game_index}_{player2_model_save_name}_{player1_model_save_name}.json"
        if os.path.exists(filename) or os.path.exists(reverse_filename):
            print("File exists")
            continue

        first_player_messages, second_player_messages = get_initial_player_messages()

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
                win = check_win(rewards)
                if win is not None:
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

        with open(f"{store_folder}/cf_{game_index}_{player1_model_save_name}_{player2_model_save_name}.json", "w") as f:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set model name for player1_model")
    parser.add_argument('--model', type=str, required=True, help="Specify the model name (e.g., gpt-4o)")
    parser.add_argument('--store_folder', type=str, required=True, help="Folder to store the game results")
    parser.add_argument('--total_rounds', type=int, default=10, help="Total rounds to play")
    # Parse the arguments
    args = parser.parse_args()
    model_name = args.model
    store_folder = args.store_folder
    total_rounds = args.total_rounds
    run_game_vs_human(store_folder, total_rounds, model_name)
