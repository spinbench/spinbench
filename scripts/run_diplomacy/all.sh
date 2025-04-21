# power list
power_list="AUSTRIA ENGLAND FRANCE GERMANY ITALY RUSSIA TURKEY"

# model list

# # 2 1 1 1 1 1
# model1="gpt-4o_1"
# model2="claude-3-5-haiku-20241022_1"
# model3="o1-preview_1"
# model4="gpt-4-turbo_1"
# model5="deepseek-reasoner_1"
# model6="o1_1"
# model_list=(\
# ${model1} \
# ${model6} \
# ${model3} \
# ${model5} \
# ${model2} \
# ${model4} \
# ${model2} \
# )
# winning_centers="18"

# # 2 2 1 1 1
# model1="gpt-4o_1"
# model2="claude-3-5-haiku-20241022_1"
# model3="o1-preview_1"
# model4="gpt-4-turbo_1"
# model5="deepseek-reasoner_1"
# model_list=(\
# ${model1} \
# ${model1} \
# ${model3} \
# ${model5} \
# ${model2} \
# ${model4} \
# ${model2} \
# )
# winning_centers="18"

# # 2 2 2 1
model1="gpt-4-turbo_1"
model2="claude-3-5-haiku-20241022_1"
model3="gpt-4o_1"
model4="deepseek-reasoner_1"
model_list=(\
${model1} \
${model1} \
${model2} \
${model2} \
${model3} \
${model4} \
${model3} \
)
winning_centers="18"


# 4 3
# model1="gpt-4o_1"
# model2="o1_1"
# model_list=(\
# ${model1} \
# ${model1} \
# ${model1} \
# ${model1} \
# ${model2} \
# ${model2} \
# ${model2} \
# )
# winning_centers="25"

# # 2 2 3
# model1="gpt-4-turbo_1"
# model2="o1_1"
# model3="gpt-4o_1"
# model_list=(\
# ${model3} \
# ${model3} \
# ${model3} \
# ${model1} \
# ${model1} \
# ${model2} \
# ${model2} \
# )
# winning_centers="20"

# model_list=(\
# "bot" \
# "bot" \
# "o3-mini" \
# "bot" \
# "bot" \
# "bot" \
# "bot" \
# )
# winning_centers="18"

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
--save_folder="-no-neg"