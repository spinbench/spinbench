# power list
power_list="AUSTRIA ENGLAND FRANCE GERMANY ITALY RUSSIA TURKEY"

tested_model="gpt-4o_1"
model_list=(\
"bot" \
"bot" \
${tested_model} \
"bot" \
"bot" \
"bot" \
"bot" \
)
winning_centers="18"

# generate the model str: m1,m2,m3,m4,m5,m6,m7
model_str=$(IFS=,; echo "${model_list[*]}")

# start a new game
python -m spinbench.tasks.diplomacy.run_game \
--num_powers=7 \
--winning_centers=${winning_centers} \
--max_tokens=10000000 \
--max_years=1920 \
--model_names=$model_str \
--temperature=0.9 \
--top_p=1.0 \
--state_file=diplomacy_game_state.json \
--enable_negotiation=0 \
--negotiation_rounds=3 \
--save_folder=saves/diplomacy/${tested_model}-basic-skill