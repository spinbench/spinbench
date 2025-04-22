# generate the average score for hanabi games
python -m spinbench.tasks.evaluation.hanabi.gather_result \
    --store_folder="/home/jianzhu/spinbench/saves/hanabi" \
    --result_name="2gemini-2.5-pro-preview" \
    --total_rounds=5 