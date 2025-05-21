#!/usr/bin/env python3
import os
import json
import argparse
import random
from pettingzoo.classic import connect_four_v3
from spinbench.tasks.connect4.utils import (
    parse_observation,
    fetch_scores_from_solver,
    check_win
)

def run_solver_vs_solver(store_folder, total_rounds=10, p_optimal=1.0, random_side=1):
    """
    Run solver vs solver Connect Four games, where one side randomly picks non-optimal moves with probability 1-p_optimal.

    Args:
        store_folder (str): Directory to save game logs.
        total_rounds (int): Total number of games to play (must be even).
        p_optimal (float): Probability of choosing the optimal move for the randomized solver.
        random_side (int): Which player to randomize (1 or 2).
    """
    assert total_rounds % 2 == 0, "total_rounds must be even"
    os.makedirs(store_folder, exist_ok=True)

    status_map = {
        0: 'Player 1 wins!',
        1: 'Player 2 wins!',
        2: 'Draw!',
        3: 'Player 1 illegal move!',
        4: 'Player 2 illegal move!',
    }
    winner_map = {
        0: 'player_1',
        1: 'player_2',
        2: 'draw',
        3: 'player_2',
        4: 'player_1',
    }

    for game_index in range(total_rounds):
        # Alternate starting player for fairness
        if game_index < total_rounds // 2:
            first_agent, second_agent = 'player_0', 'player_1'
        else:
            first_agent, second_agent = 'player_1', 'player_0'

        filename = os.path.join(store_folder,
            f"cf_{game_index}_{first_agent}_vs_{second_agent}.json")
        if os.path.exists(filename):
            print(f"Skipping existing file: {filename}")
            continue

        env = connect_four_v3.env(render_mode=None)
        env.reset(seed=42 + game_index)
        game_log = []
        win = None
        pos_str = ""  # track moves for solver API (1-based columns)

        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            # Check for terminal win or draw
            win_code = check_win(env.rewards)
            if win_code is not None:
                win = win_code
                break

            if termination or truncation:
                action = None
                is_best = False
                score_list = None
                top_move_index = None
                best_move = None    
                action_score = None
            else:
                # Get legal moves and solver scores
                _, _, legal_moves = parse_observation(observation, agent)
                # Fetch scores from solver for current position
                score_list = fetch_scores_from_solver(pos_str)
                if score_list:
                    best_score = max(score_list)
                    best_indices = [i for i, s in enumerate(score_list) if s == best_score]
                    best_move = random.choice(best_indices)
                else:
                    # fallback: pick first legal
                    best_move = legal_moves[0]
                # Decide whether to pick optimal or random move
                side = 1 if agent == 'player_0' else 2
                if side == random_side and random.random() > p_optimal:
                    # pick random legal move
                    action = random.choice(legal_moves)
                else:
                    action = best_move
                is_best = (action == best_move)
                # update pos_str for next fetch
                pos_str += str(action + 1)
                if not score_list:
                    print(f"Error fetching scores for {agent}")
                    break
                solver_scores_sorted = sorted(list(score_list), reverse=True)
                if 0 <= action < len(score_list):
                    action_score = score_list[action]
                    top_move_index = solver_scores_sorted.index(score_list[action])
                else:
                    action_score = None  # Handle invalid action index
                    top_move_index = None
                
                

            # Record step
            game_log.append({
                'agent': agent,
                'action': action,
                'is_best': is_best,
                'score': score_list,
                'action_score': action_score,
                'top_move_index': top_move_index,
                'best_move': best_move,
                'observation': observation['observation'].tolist(),
                'reward': env.rewards,
                'action_mask': observation['action_mask'].tolist(),
            })

            # Take the action
            try:
                env.step(action)
            except Exception as e:
                print(f"Error on env.step: {e}")
                break

        env.close()

        # Default draw if no win detected
        if win is None:
            win = 2

        # Save game log
        with open(filename, 'w') as f:
            json.dump({
                'status': status_map.get(win, 'Unknown'),
                'winner': winner_map.get(win, 'unknown'),
                'total_rounds': total_rounds,
                'random_side': random_side,
                'p_optimal': p_optimal,
                'game_log': game_log,
            }, f, indent=4)
        print(f"Saved: {filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run solver vs solver Connect Four and collect trajectories'
    )
    parser.add_argument('--store_folder', required=True,
                        help='Directory to save game logs')
    parser.add_argument('--total_rounds', type=int, default=10,
                        help='Total number of games (even)')
    parser.add_argument('--p_optimal', type=float, default=1.0,
                        help='Probability that randomized solver picks optimal move')
    parser.add_argument('--random_side', type=int, choices=[1,2], default=1,
                        help='Which player to randomize: 1 or 2')
    args = parser.parse_args()
    run_solver_vs_solver(
        args.store_folder,
        total_rounds=args.total_rounds,
        p_optimal=args.p_optimal,
        random_side=args.random_side
    )

# Example Usage
# python -m spinbench.dataset_collection.cf_solver --store_folder ./solver_games --total_rounds 10 --p_optimal 0.9 --random_side 1