#!/usr/bin/env python3
import os
import json
import argparse
import random
from pettingzoo.classic import tictactoe_v3
from spinbench.tasks.tic_tac_toe.utils import (
    solver_parse_observation,
    getLegalMoves,
    check_win,
    minimax,
)

def find_best_move_for_x(board_2d):
	"""
	Returns the best move index (0..8) for 'X' from the current position,
	or None if no legal moves.
	"""
	legal_moves = getLegalMoves(board_2d)
	if not legal_moves:
		return None, {}, [], None
	
	best_val = -float('inf')
	best_move = None
	best_moves = []
	move_scores = {}
	for move_idx in legal_moves:
		r, c = divmod(move_idx, 3)
		board_2d[r][c] = 'X'
		val = minimax(board_2d, is_maximizing=False)  # Next turn: O
		board_2d[r][c] = ' '
		move_scores[move_idx] = val
		if val > best_val:
			best_val = val
			best_moves = [move_idx]
		elif val == best_val:
			best_moves.append(move_idx)
	random.shuffle(best_moves)
	best_move = best_moves[0] if best_moves else None
	return best_move, move_scores, best_moves, best_val

def find_best_move_for_o(board_2d):
	"""
	Returns the best move index (0..8) for 'O' from the current position,
	or None if no legal moves.
	"""
	legal_moves = getLegalMoves(board_2d)
	if not legal_moves:
		return None, {}, [], None
	
	best_val = float('inf')
	best_move = None
	best_moves = []
	move_scores = {}
	
	for move_idx in legal_moves:
		r, c = divmod(move_idx, 3)
		board_2d[r][c] = 'O'
		val = minimax(board_2d, is_maximizing=True)  # Next turn: X
		board_2d[r][c] = ' '
		move_scores[move_idx] = val
		if val < best_val:
			best_val = val
			best_moves = [move_idx]
		elif val == best_val:
			best_moves.append(move_idx)
	random.shuffle(best_moves)
	best_move = best_moves[0] if best_moves else None
	return best_move, move_scores, best_moves, best_val


def run_solver_vs_solver(store_folder, total_rounds=10, p_optimal=1.0, random_side=1):
    assert total_rounds % 2 == 0, "total_rounds must be even"
    os.makedirs(store_folder, exist_ok=True)

    for game_index in range(total_rounds):
        # Alternate starting player each round
        first_agent, second_agent = ('player_1', 'player_2') if game_index < total_rounds // 2 else ('player_2', 'player_1')

        filename = f"{store_folder}/ttt_{game_index}_{first_agent}_vs_{second_agent}.json"
        if os.path.exists(filename):
            print("File exists, skipping:", filename)
            continue

        env = tictactoe_v3.env(render_mode=None)
        env.reset(seed=42 + game_index)
        game_log = []
        win = None

        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            board_state, legal_moves, legal_moves_list = solver_parse_observation(observation, agent)
            # Determine best move for this agent
            if agent == 'player_1':
                best_move, move_scores, best_moves, best_val = find_best_move_for_x(board_state)
            else:
                best_move, move_scores, best_moves, best_val = find_best_move_for_o(board_state)

            # Choose action based on solver policy
            if termination or truncation:
                action = None
                is_best = False
            else:
                # Decide if this agent is the randomized solver
                if (agent == 'player_1' and random_side == 1) or (agent == 'player_2' and random_side == 2):
                    if random.random() < p_optimal:
                        action = best_move
                    else:
                        # pick a random legal move
                        action = random.choice(legal_moves_list)
                else:
                    # deterministic optimal solver
                    action = best_move
                is_best = (action == best_move)

            # Record step
            game_log.append({
                "agent": agent,
                "board_state": board_state,
                "move_scores": move_scores,
                "best_moves": best_moves,
                "best_val": best_val,
                "best_move": best_move,
                "legal_moves": legal_moves,
                "action": action,
                "is_best": is_best,
                "observation": observation['observation'].tolist(),
                "reward": env.rewards,
                "action_mask": observation['action_mask'].tolist(),
            })

            try:
                env.step(action)
            except Exception as e:
                print(f"Error stepping env for agent {agent}: {e}")
                break

            # Check for terminal reward-based win
            win_reward = check_win(env.rewards)
            if win_reward is not None:
                win = win_reward
                break

        env.close()

        # Map win code to human-readable
        status_map = {0: 'Player 1 wins!', 1: 'Player 2 wins!', 2: 'Draw'}
        winner_map = {0: 'player_1', 1: 'player_2', 2: 'draw'}
        result_status = status_map.get(win, 'Unknown')
        result_winner = winner_map.get(win, 'unknown')

        # Save game log
        with open(filename, 'w') as f:
            json.dump({
                "status": result_status,
                "winner": result_winner,
                "total_rounds": total_rounds,
                "random_side": random_side,
                "p_optimal": p_optimal,
                "game_log": game_log
            }, f, indent=4)
        print("Saved game log:", filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run solver vs solver Tic Tac Toe and collect trajectories")
    parser.add_argument(
        "--store_folder", type=str, required=True,
        help="Folder to save the game results"
    )
    parser.add_argument(
        "--total_rounds", type=int, default=10,
        help="Total rounds to play (must be even)"
    )
    parser.add_argument(
        "--p_optimal", type=float, default=1.0,
        help="Probability of selecting the optimal move for the randomized solver (0.0 to 1.0)"
    )
    parser.add_argument(
        "--random_side", type=int, choices=[1,2], default=1,
        help="Which solver to randomize: 1 for player_1, 2 for player_2"
    )
    args = parser.parse_args()
    run_solver_vs_solver(
        args.store_folder,
        total_rounds=args.total_rounds,
        p_optimal=args.p_optimal,
        random_side=args.random_side
    )

# example usage
# python -m spinbench.dataset_collection.tic_tac_toe_solver --store_folder ./solver_games --total_rounds 10 --p_optimal 0.5 --random_side 1
