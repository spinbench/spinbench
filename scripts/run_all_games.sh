# Run the result in the main table in the paper, for o4-mini
# Requires setting the OPENAI_API_KEY environment variable
# all configs are in configs folder
# You have to follow the installation first

# The script will run all the tasks and save the trajectories in the saves folder
# The evaluation results will be saved in the results folder

################################
######### Tic Tac Toe ##########
################################

## LLM vs solver
python -m spinbench.tasks.tic_tac_toe.run_game_vs_solver \
    --store_folder="saves/o4-mini-2025-04-16/tic_tac_toe_LLM_vs_solver" \
    --tested_model="o4-mini-2025-04-16" \
    --total_rounds=10

## Evaluation: annotate each move with the solver's score
python -m spinbench.tasks.evaluation.competitive.tictactoe_score_moves \
    --json_folder="saves/o4-mini-2025-04-16/tic_tac_toe_LLM_vs_solver"

# Evaluation: gather the scores and compute the result
python -m spinbench.tasks.evaluation.competitive.tictactoe_score_plot \
    --json_folder="saves/o4-mini-2025-04-16/tic_tac_toe_LLM_vs_solver" \
    --output_folder="results/o4-mini-2025-04-16"

## Evaluation: compute the game statistics. In the result, win rate is SOLVER's winrate
python -m spinbench.tasks.evaluation.competitive.collect_solver_winrate \
    --directory="saves/o4-mini-2025-04-16/tic_tac_toe_LLM_vs_solver" \
    --output_file="results/o4-mini-2025-04-16/tic_tac_toe_LLM_vs_solver_winrate.json"

################################
########## Connect 4 ###########
################################

## launch the solver service in a separate terminal
(
cd spinbench/tasks/connect4/
python c4solver.py --port 5000
) &

## LLM vs solver
python -m spinbench.tasks.connect4.run_game_vs_solver \
    --store_folder="saves/o4-mini-2025-04-16/connect4_LLM_vs_solver" \
    --tested_model="o4-mini-2025-04-16" \
    --total_rounds=10

# Evaluation: annotate each move with the solver's score
python -m spinbench.tasks.evaluation.competitive.connect4_score_moves \
    --json_folder="saves/o4-mini-2025-04-16/connect4_LLM_vs_solver"

# Evaluation: gather the scores and compute the result
python -m spinbench.tasks.evaluation.competitive.connect4_score_plot \
    --json_folder="saves/o4-mini-2025-04-16/connect4_LLM_vs_solver" \
    --output_folder="results/o4-mini-2025-04-16"

# Evaluation: compute the game statistics. In the result, win rate is SOLVER's winrate
python -m spinbench.tasks.evaluation.competitive.collect_solver_winrate \
    --directory="saves/o4-mini-2025-04-16/connect4_LLM_vs_solver" \
    --output_file="results/o4-mini-2025-04-16/connect4_LLM_vs_solver_winrate.json"

## Close the solver web service
child_pid=$!
kill -9 $child_pid


################################
############ Chess #############
################################


## LLM vs stockfish
python -m spinbench.tasks.chess.chess_stockfish \
    --store_folder="saves/o4-mini-2025-04-16/chess_LLM_vs_stockfish" \
    --tested_model="o4-mini-2025-04-16" \
    --stockfish_level=20 \
    --stockfish_path="./stockfish" \
    --total_rounds=4

## Evaluation: annotate each move with the solver's score
python -m spinbench.tasks.evaluation.competitive.chess_score_moves \
    --stockfish_path="./stockfish" \
    --json_folder="saves/o4-mini-2025-04-16/chess_LLM_vs_stockfish"

## Evaluation: gather the scores and compute the result
python -m spinbench.tasks.evaluation.competitive.chess_score_plot \
    --json_folder="saves/o4-mini-2025-04-16/chess_LLM_vs_stockfish" \
    --output_folder="results/o4-mini-2025-04-16"

## Evaluation: compute the game statistics. In the result, win rate is SOLVER's winrate
python -m spinbench.tasks.evaluation.competitive.collect_solver_winrate \
    --directory="saves/o4-mini-2025-04-16/chess_LLM_vs_stockfish" \
    --output_file="results/o4-mini-2025-04-16/chess_LLM_vs_stockfish_winrate.json"


####################################
######### 2-players' Hanabi ########
####################################

# test_model and player_number should be set at the same time

## Run the game given the player models
python -m spinbench.tasks.hanabi.run_game \
    --player_models_json="configs/hanabi_player_models.json" \
    --store_folder="saves/o4-mini-2025-04-16/hanabi" \
    --result_name="2o4-mini-2025-04-16" \
    --test_model="o4-mini-2025-04-16" \
    --player_number=2 \
    --total_rounds=5

## Gather the results
python -m spinbench.tasks.evaluation.hanabi.gather_result \
    --store_folder="saves/o4-mini-2025-04-16/hanabi" \
    --result_name="2o4-mini-2025-04-16" \
    --total_rounds=5 \
    --output_file="results/hanabi_result_2_o4-mini-2025-04-16.json"

####################################
######### 3-players' Hanabi ########
####################################

## Run the game given the player models
python -m spinbench.tasks.hanabi.run_game \
    --player_models_json="configs/hanabi_player_models.json" \
    --store_folder="saves/o4-mini-2025-04-16/hanabi" \
    --result_name="3o4-mini-2025-04-16" \
    --test_model="o4-mini-2025-04-16" \
    --player_number=3 \
    --total_rounds=5
## Gather the results
python -m spinbench.tasks.evaluation.hanabi.gather_result \
    --store_folder="saves/o4-mini-2025-04-16/hanabi" \
    --result_name="3o4-mini-2025-04-16" \
    --total_rounds=5 \
    --output_file="results/hanabi_result_3_o4-mini-2025-04-16.json"


####################################
######### 4-players' Hanabi ########
####################################

## Run the game given the player models
python -m spinbench.tasks.hanabi.run_game \
    --player_models_json="configs/hanabi_player_models.json" \
    --store_folder="saves/o4-mini-2025-04-16/hanabi" \
    --result_name="4o4-mini-2025-04-16" \
    --test_model="o4-mini-2025-04-16" \
    --player_number=4 \
    --total_rounds=5
## Gather the results
python -m spinbench.tasks.evaluation.hanabi.gather_result \
    --store_folder="saves/o4-mini-2025-04-16/hanabi" \
    --result_name="4o4-mini-2025-04-16" \
    --total_rounds=5 \
    --output_file="results/hanabi_result_4_o4-mini-2025-04-16.json"


########################################
######### 5-players' Hanabi ########
####################################


## Run the game given the player models
python -m spinbench.tasks.hanabi.run_game \
    --player_models_json="configs/hanabi_player_models.json" \
    --store_folder="saves/o4-mini-2025-04-16/hanabi" \
    --result_name="5o4-mini-2025-04-16" \
    --test_model="o4-mini-2025-04-16" \
    --player_number=5 \
    --total_rounds=5
## Gather the results
python -m spinbench.tasks.evaluation.hanabi.gather_result \
    --store_folder="saves/o4-mini-2025-04-16/hanabi" \
    --result_name="5o4-mini-2025-04-16" \
    --total_rounds=5 \
    --output_file="results/hanabi_result_5_o4-mini-2025-04-16.json"


####################################
############# Diplomacy ############
####################################

## Basic skill evaluation experiment (one LLM playing against six neural powers)
power_list="AUSTRIA ENGLAND FRANCE GERMANY ITALY RUSSIA TURKEY"

tested_model="o4-mini-2025-04-16_1"
model_list=( "bot" "bot" ${tested_model} "bot" "bot" "bot" "bot" )
winning_centers="18"

model_str=$(IFS=,; echo "${model_list[*]}")

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
  --save_folder=saves/${tested_model}/diplomacy/basic-skill

## Evaluation: gather the metrics
python -m spinbench.tasks.evaluation.diplomacy.eval \
    --game_folder="saves/o4-mini-2025-04-16_1/diplomacy/basic-skill" \
    --output_file="results/o4-mini-2025-04-16_1/diplomacy/basic-skill/eval.json"


## Running 4 agents' Diplomacy setting (as in the main result table)
## Requires setting the OPENAI_API_KEY and ANTHROPIC_API_KEY environment variable

power_list="AUSTRIA ENGLAND FRANCE GERMANY ITALY RUSSIA TURKEY"

# 2 2 2 1
model1="gpt-4-turbo_1"
model2="claude-3-5-haiku-20241022_1"
model3="gpt-4o_1"
model4="o4-mini-2025-04-16_1"
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
--save_folder="saves/o4-mini-2025-04-16/diplomacy/4-players-setting-no-neg"

## Evaluation: gather the metrics
python -m spinbench.tasks.evaluation.diplomacy.eval \
    --game_folder="saves/o4-mini-2025-04-16/diplomacy/4-players-setting-no-neg" \
    --output_file="results/o4-mini-2025-04-16/diplomacy/4-players-setting-no-neg"
