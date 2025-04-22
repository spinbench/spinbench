# generate general evaluation metrics
python -m spinbench.tasks.evaluation.diplomacy.eval \
    --game_folder="saves/diplomacy/gpt-4o_1-basic-skill" \
    --output_file="saves/diplomacy/gpt-4o_1-basic-skill/eval.json"

# generate negotiation evaluation metrics
python -m spinbench.tasks.evaluation.diplomacy.eval_neg \
    --neg_config_file="/home/jianzhu/spinbench/configs/neg_eval_config.json"