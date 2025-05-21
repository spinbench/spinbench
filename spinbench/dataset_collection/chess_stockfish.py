#!/usr/bin/env python3
import os
import json
import argparse
from chess import Board, Move
import random
from stockfish import Stockfish

def run_stockfish_vs_stockfish(store_folder, stockfish_path, total_rounds=10, p_optimal=1.0, random_side=1):
    """
    Run Stockfish vs Stockfish matches, both at skill level 20, and save move trajectories.

    Args:
        store_folder (str): Directory to save game logs.
        stockfish_path (str): Path to the Stockfish executable.
        total_rounds (int): Total number of games to play (must be even).
    """
    assert total_rounds % 2 == 0, "total_rounds must be even"
    os.makedirs(store_folder, exist_ok=True)

    # Prepare two independent Stockfish engines
    sf_white = Stockfish(stockfish_path)
    sf_black = Stockfish(stockfish_path)
    sf_white.set_skill_level(20)
    sf_black.set_skill_level(20)
    sf_white.update_engine_parameters({
        "Threads": 32,       
        "Skill Level": 20,
        "Move Overhead": 10,
        "Hash": 2048,
    })
    sf_black.update_engine_parameters({
        "Threads": 32, 
        "Skill Level": 20,
        "Move Overhead": 10,
        "Hash": 2048,
    })

    status_map = { True: 'White wins!', False: 'Black wins!', None: 'Draw!' }

    for game_index in range(total_rounds):
        # Alternate colors each game
        white_engine = sf_white if game_index % 2 == 0 else sf_black
        black_engine = sf_black if game_index % 2 == 0 else sf_white

        # Reset engines' internal states
        white_engine.set_fen_position(Board().fen())
        black_engine.set_fen_position(Board().fen())

        board = Board()
        game_log = []

        # Play moves until game over
        while not board.is_game_over():
            print(board)
            print("*"*20)
            if board.turn:  # White to move
                best_move_uci = white_engine.get_best_move()
                top_moves = white_engine.get_top_moves(10)
                top_moves = [i["Move"] for i in top_moves]
            else:
                best_move_uci = black_engine.get_best_move()
                top_moves = black_engine.get_top_moves(10)
                top_moves = [i["Move"] for i in top_moves]
            if (random_side == 1 and board.turn) or (random_side == 2 and not board.turn):
                # Randomize the move selection
                if p_optimal < 1.0:
                    if top_moves:
                        best_move_uci = top_moves[0] if random.random() < p_optimal else random.choice(top_moves[1:])
                    else:
                        best_move_uci = None
            else:
                # Use the best move from the engine
                best_move_uci = top_moves[0] if top_moves else None
            if best_move_uci is None:
                print("No legal moves available, exiting.")
                break
            move = Move.from_uci(best_move_uci)
            try:
                top_move_index = top_moves.index(str(best_move_uci))
            except:
                top_move_index = -1
            game_log.append({
                'turn': 'white' if board.turn else 'black',
                'move': best_move_uci,
                'top_moves': top_moves,
                'top_move_index': top_move_index,
                'action': str(move),
                'fen': board.fen()
            })
            board.push(move)

            # Update both engines with the new position
            fen = board.fen()
            white_engine.set_fen_position(fen)
            black_engine.set_fen_position(fen)

        outcome = board.outcome()
        result = status_map[outcome.winner if outcome is not None else None]

        # Save log
        filename = os.path.join(store_folder, f"chess_sf_vs_sf_{game_index}.json")
        with open(filename, 'w') as f:
            json.dump({
                'game_index': game_index,
                'result': result,
                'moves': game_log
            }, f, indent=4)
        print(f"Saved game {game_index}: {result}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run Stockfish vs Stockfish games at level 20'
    )
    parser.add_argument('--store_folder', required=True,
                        help='Directory to save game results')
    parser.add_argument('--stockfish_path', required=True,
                        help='Path to Stockfish executable')
    parser.add_argument('--total_rounds', type=int, default=10,
                        help='Total number of even-numbered games to play')
    parser.add_argument(
        "--p_optimal", type=float, default=1.0,
        help="Probability of selecting the optimal move for the randomized solver (0.0 to 1.0)"
    )
    parser.add_argument(
        "--random_side", type=int, choices=[1,2], default=1,
        help="Which solver to randomize: 1 for player_1, 2 for player_2"
    )
    args = parser.parse_args()
    run_stockfish_vs_stockfish(
        args.store_folder,
        args.stockfish_path,
        total_rounds=args.total_rounds,
        p_optimal=args.p_optimal,
        random_side=args.random_side
    )

# Example usage:
# python -m spinbench.dataset_collection.chess_stockfish --store_folder ./solver_games --stockfish_path /home/jianzhu/spinbench/stockfish --total_rounds 10 --p_optimal 0.4 --random_side 1