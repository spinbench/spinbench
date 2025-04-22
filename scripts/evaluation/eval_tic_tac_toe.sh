# generate step score for tic tac toe games
python -m spinbench.tasks.evaluation.competitive.tictactoe_score_moves \
    --json_folder="/home/jianzhu/spinbench/saves/tic_tac_toe"

# compute solver win rate
python -m spinbench.tasks.evaluation.competitive.collect-solver-winrate \
    --directory="/home/jianzhu/spinbench/saves/tic_tac_toe"