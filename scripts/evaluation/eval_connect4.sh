# generate step scores for Connect4
python -m spinbench.tasks.evaluation.competitive.connect4_score_moves \
    --json_folder="/home/jianzhu/spinbench/saves/connect4"

# generate solver win rate for Connect4
python -m spinbench.tasks.evaluation.competitive.collect-solver-winrate \
    --directory="/home/jianzhu/spinbench/saves/connect4"