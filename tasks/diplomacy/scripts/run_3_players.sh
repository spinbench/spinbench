# power list
power_list="AUSTRIA ENGLAND FRANCE GERMANY ITALY RUSSIA TURKEY"

# 2 2 3
model1="gpt-4-turbo_1"
model2="o1_1"
model3="gpt-4o_1"
model_list=(\
${model3} \
${model3} \
${model3} \
${model1} \
${model1} \
${model2} \
${model2} \
)
winning_centers="20"

# generate the model str: m1,m2,m3,m4,m5,m6,m7
model_str=$(IFS=,; echo "${model_list[*]}")

# start a new game
python run_game.py \
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
--save_folder="223-no-neg"