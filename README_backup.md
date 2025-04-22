# SPIN-Bench

This is the repository for SPIN-Bench, a benchmark for evaluating the strategic planning and social reasoning capabilities of large language models (LLMs). It includes implementations of various games and tasks, as well as the code to run the benchmark.

Title: SPIN-Bench: How Well Do LLMs Plan Strategically and Reason Socially?
Authors: Jianzhu Yao, Kevin Wang, Ryan Hsieh, Haisu Zhou, Tianqing Zou, Zerui Cheng, Zhangyang Wang, Pramod Viswanath
Affiliation: University of Texas at Austin, Princeton University
Paper: https://arxiv.org/pdf/2503.12349
Website: https://spinbench.github.io/
Huggingface Daily Paper: https://huggingface.co/papers/2503.12349

## Installation

### spinbench package

To install this repository, you can run the following command in the root directory of the repository:

```shell
git clone --recursive git@github.com:spinbench/spinbench.git
cd spinbench
pip install -e .
```

### Build the connect4 solver

In our benchmark, we used [connect4 solver](https://github.com/PascalPons/connect4) developed by Pascal Pons. You can install it by running the following command in the root directory of the repository:

```shell
cd spinbench/tasks/connect4/connect4_solver 
make
cp c4solver ..
cd ../../../.. # go back to the root directory
```

### Build the Stockfish engine

We also used Stockfish as the chess engine, to install the Stockfish engine, you can run the following command:

```shell
wget https://github.com/official-stockfish/Stockfish/archive/refs/tags/sf_17.1.zip
unzip sf_17.1.zip
cd Stockfish-sf_17.1/src
make -j profile-build
cp stockfish ../../
```

Then the Stockfish engine will be in the root directory of the repository. You will use it in the chess game.

## Usage

### PDDL

Coming soon.

### Competitive Games

You can define your own config files for three competitive games in our benchmark, an example is shown as below:

```json
// configs/solver_list_single.json
{
    "player1_model_list": [
        {
            "model": "our_solver",
            "prompt_config": [
            ]
        }
    ],
    "player2_model_list": [
        {
            "model": "gpt-4o",
            "prompt_config": [
                {
                    "name": "forced-reasoning",
                    "params": {
                        "interactive_times": 1,
                        "prompt_messages": [
                            "Please reason about the current state. You should analyze all the opponent's moves and your moves, try to reason opponent's thought in detail. Only need to plan and reason now, no need to make move at this stage."
                        ]
                    }
                }
            ]
        }
    ]
}
```

<!-- Some notes how to define the config files -->

If you want to run multiple pairs of models, you can add more models in the player1/2_model_list. The benchmark will run all the pairs of models in the list. Notice, the same index in player1_model_list and player2_model_list will play against each other.

If you want to run games between different LLM models, you can refer to the config file at [configs/player_list_single.json](configs/player_list_single.json). 

For advanced `prompt_config` design, please refer to the doc at [docs/prompt_config.md](docs/prompt_config.md).

#### Run Tic Tac Toe

To run Tic Tac Toe between LLM and the solver, you can run the following command:

```shell
python -m spinbench.tasks.tic_tac_toe.run_game_vs_solver \
    --store_folder="saves/tic_tac_toe_vs_solver" \
    --player_list="configs/solver_list_single.json" \
    --total_rounds=10 
```

To run Tic Tac Toe ONLY among LLMs, you can run the following command:

```shell
python -m spinbench.tasks.tic_tac_toe.run_game \
    --store_folder="saves/tic_tac_toe_LLMs" \
    --player_list="configs/player_list_single.json" \
    --total_rounds=10
```

After getting the results, you can score each step of LLMs' moves by running the following command:

```shell
python -m spinbench.tasks.evaluation.competitive.tictactoe_score_moves \
    --json_folder="saves/tic_tac_toe_LLMs"

python -m spinbench.tasks.evaluation.competitive.tictactoe_score_moves \
    --json_folder="saves/tic_tac_toe_vs_solver"
```

#### Run Connect 4

You should run the connect 4 solver web service first:

```shell
cd spinbench/tasks/connect4/
python c4solver.py --port 5000
cd ../../..
```

Likewise, to run Connect 4 between LLM and the solver, you can run the following command:

```shell
python -m spinbench.tasks.connect4.run_game_vs_solver \
    --store_folder="saves/connect4_vs_solver" \
    --player_list="configs/solver_list_single.json" \
    --total_rounds=10 
```

To run Connect 4 ONLY among LLMs, you can run the following command:

```shell
python -m spinbench.tasks.connect4.run_game \
    --store_folder="saves/connect4_LLMs" \
    --player_list="configs/player_list_single.json" \
    --total_rounds=10
```

After getting the results, you can score each step of LLMs' moves by running the following command:

```shell
python -m spinbench.tasks.evaluation.competitive.connect4_score_moves \
    --json_folder="saves/connect4_LLMs"

python -m spinbench.tasks.evaluation.competitive.connect4_score_moves \
    --json_folder="saves/connect4_vs_solver"
```

### Chess

To run chess between LLM and the stockfish engine, you should first write a similar config file:

```json
{
    "player1_model_list": [
        {
            "model": "stockfish",
            "level": 0
        }
    ],
    "player2_model_list": [
        {
            "model": "gpt-4o",
            "prompt_config": [
            ]
        }
    ]
}
```

In the level field, you can set the level of the stockfish engine. The higher the level, the stronger the engine. The level ranges from 0 to 20. You can also add more models in the player1/2_model_list to run more pairs of models. 

Then you can write the command to run the chess game between LLM and the stockfish engine:

```shell
# input your stockfish binary path in the --stockfish_path argument
python -m spinbench.tasks.chess.chess_stockfish \
    --store_folder="saves/chess_vs_stockfish" \
    --player_list="configs/stockfish-list-supp.json" \
    --stockfish_path="stockfish" \
    --total_rounds=2
```

To run chess ONLY among LLMs, you can run the following command:

```shell
python -m spinbench.tasks.chess.run_game \
    --store_folder="saves/chess_LLMs" \
    --player_list="configs/player_list_single.json" \
    --total_rounds=2
```

After getting the results, you can score each step of LLMs' moves by running the following command:

```shell
# input your stockfish binary path in the --stockfish_path argument
python -m spinbench.tasks.evaluation.competitive.chess_score_moves \
    --stockfish_path="stockfish \
    --json_folder="saves/chess_LLMs"

# or
python -m spinbench.tasks.evaluation.competitive.chess_score_moves \
    --stockfish_path="stockfish \
    --json_folder="saves/chess_vs_stockfish"
```

### Win rate

To compute the win rate of each model/solver for the competitive games (the above three games), you can run the following command:

```shell
python -m spinbench.tasks.evaluation.competitive.collect-solver-winrate \
    --directory="saves/connect4_LLMs" \
    --output="winrate.json" 
```

To compute the win stats into the csv file, you can run the following command:

```shell
python -m spinbench.tasks.evaluation.competitive.win_stats \
    --input="saves/connect4_LLMs \
    --output="saves/connect4_LLMs/win_stats.csv"
```

With the win_stats, you can also compute the elo rating of those models:

```shell
python -m spinbench.tasks.evaluation.competitive.compute_elo \
    --input="saves/connect4_LLMs/win_stats.csv" \
```

### Hanabi

Hanabi is 2-5 players cooperative card game. An example config file is shown as below:

```json
// configs/hanabi_player_models.json
[
    {
        "model": "gemini-2.5-pro-preview-03-25",
        "prompt_config": [
        ]
    },
    {
        "model": "gemini-2.5-pro-preview-03-25",
        "prompt_config": [
        ]
    }
]
```

This means we will run 2 players, both using the same model. You can add more models in the list to run more players.

To run the Hanabi game with the above config, you can run the following command in the root directory of the repository:

```shell
python -m spinbench.tasks.hanabi.run_game \
    --player_models_json="configs/hanabi_player_models.json" \
    --store_folder="saves/hanabi" \
    --result_name="2gemini-2.5-pro-preview" \
    --total_rounds=5
```

To gather all the results, you can run the following command:

```shell
python -m spinbench.tasks.evaluation.hanabi.gather_result \
    --store_folder="saves/hanabi" \
    --result_name="2gemini-2.5-pro-preview" \
    --total_rounds=5
```

### Diplomacy

We provide several example scripts running Diplomacy among LLMs in [scripts/run_diplomacy](scripts/run_diplomacy). You can refer to [scripts/run_diplomacy/README.md](scripts/run_diplomacy/README.md) for more details about how to setup different configurations for running Diplomacy.

For example, to run the basic skill test, you can run the following command:

```shell
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
```

To run the Diplomacy among multiple LLMs, you can refer to [scripts/run_diplomacy/run_5_players.sh](scripts/run_diplomacy/run_5_players.sh) for more details.

For the evaluation of Diplomacy game, you can run the following command to generate general evaluation metrics:

```shell
python -m spinbench.tasks.evaluation.diplomacy.eval \
    --game_folder="saves/diplomacy/gpt-4o_1-basic-skill" \
    --output_file="saves/diplomacy/gpt-4o_1-basic-skill/eval.json"
```

To generate the negotiation evaluation metrics, you should setup the `neg_eval_config.json` file first, an example is shown at [configs/neg_eval_config.json](configs/neg_eval_config.json). You can refer to README file in configs folder for more configuration details.

Then you can run the following command to generate the negotiation evaluation metrics:

```shell
python -m spinbench.tasks.evaluation.diplomacy.eval_neg \
    --neg_config_file="configs/neg_eval_config.json"
```

## Contributions

We would love to hear from you! If you have any suggestions, bug reports, issues, or feature requests, please open an issue on our GitHub repository. If you would like to contribute code, please fork the repository and submit a pull request. We'll be sure to follow up shortly!

Contact person: Jianzhu Yao and Kevin Wang (Email: jy0246@princeton.edu, kevinwang.1839@utexas.edu)

## Citation

If you use SPIN-Bench in your research, please cite our paper:

```bibtex
@misc{yao2025spinbenchllmsplanstrategically,
    title={SPIN-Bench: How Well Do LLMs Plan Strategically and Reason Socially?},
    author={Jianzhu Yao and Kevin Wang and Ryan Hsieh and Haisu Zhou and Tianqing Zou and Zerui Cheng and Zhangyang Wang and
    Pramod Viswanath},
    year={2025},
    eprint={2503.12349},
    archivePrefix={arXiv},
    primaryClass={cs.AI},
    url={https://arxiv.org/abs/2503.12349},
}
```

## License

MIT. See [LICENSE](LICENSE) for details.
