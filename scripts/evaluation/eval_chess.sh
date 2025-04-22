# generate step scores for chess
python -m spinbench.tasks.evaluation.competitive.chess_score_moves \
    --stockfish_path="/home/jianzhu/LLm-pddl-benchmark/stockfish/stockfish-ubuntu-x86-64-avx2" \
    --json_folder="/home/jianzhu/spinbench/saves/chess"