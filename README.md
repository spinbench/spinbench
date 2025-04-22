# SPIN‑Bench: How well do large language models plan strategically and reason socially?  

**A Strategic Planning & Interpersonal Negotiation Benchmark**

Jianzhu Yao, Kevin Wang, Ryan Hsieh, Haisu Zhou, Tianqing Zou, Zerui Cheng, Zhangyang Wang, Pramod Viswanath  
[[arXiv 2503.12349]](https://arxiv.org/pdf/2503.12349)  |  [[Project Website]](https://spinbench.github.io/)  |  [[Huggingface Daily Paper]](https://huggingface.co/papers/2503.12349)

---

## 👋 Overview

![](assets/main_figure.png)

SPIN‑Bench is an open‑source benchmark that probes the **strategic planning** and **social‑reasoning** abilities of contemporary language models.  
It unifies a diverse suite of games—from *Tic‑Tac‑Toe* to *Diplomacy*—together with ground‑truth solvers, evaluation harnesses, and reproducible experiments. Researchers can easily:

* **Pit LLMs against optimal solvers** to gauge raw tactical strength.  
* **Stage multi‑agent LLM battles** to study emergent collaboration and deception.  
* **Score reasoning chains** to examine how models plan, reflect, and react.  
* **Compute win‑rates, Elo ratings, and negotiation metrics** with one‑line commands.

---

## 🚀 Features
| Category | Highlights |
| -------- | ---------- |
| **Breadth of Tasks** | Classic perfect‑information games (Tic‑Tac‑Toe, Connect 4, Chess) plus imperfect‑information and negotiation‑heavy games (Hanabi, Diplomacy). |
| **Plug‑and‑Play Solvers** | Optimal solvers (Connect 4, Tic‑Tac‑Toe, Stockfish) for ground‑truth baselines. |
| **Flexible Prompting** | YAML/JSON prompt templates with *forced reasoning*, multi‑step self‑reflection, or any custom protocol. |
| **Rich Analytics** | Fine‑grained move scoring, win‑rate collectors, Elo calculators, detailed game metric, negotiation sentiment analysis. |

---

## 🔧 Installation
### 1. Prerequisites
* Python ≥ 3.9  
* `gcc`, `make`, and a C++17‑capable toolchain (for solvers)  
* Unix‑like OS (Linux/macOS). Windows users are encouraged to leverage WSL2.

### 2. Clone & Install `spinbench`
```shell
git clone --recursive git@github.com:spinbench/spinbench.git
cd spinbench
pip install -e .
```

### 3. Build the **Connect 4** solver
```shell
cd spinbench/tasks/connect4/connect4_solver
make
cp c4solver ..
cd ../../../..    # back to repo root
```

### 4. Build the **Stockfish** chess engine
```shell
wget https://github.com/official-stockfish/Stockfish/archive/refs/tags/sf_17.1.zip
unzip sf_17.1.zip
cd Stockfish-sf_17.1/src
make -j profile-build
cp stockfish ../../
```
The resulting `stockfish` binary must remain in the repository root (or set `--stockfish_path` in later commands).

---

## 🔥 Quick‑Start
Want to see SPIN‑Bench in action? Run ten LLM‑vs‑solver *Tic‑Tac‑Toe* matches and score every move:

```shell
python -m spinbench.tasks.tic_tac_toe.run_game_vs_solver \
    --store_folder="saves/tic_tac_toe_vs_solver" \
    --player_list="configs/solver_list_single.json" \
    --total_rounds=10

python -m spinbench.tasks.evaluation.competitive.tictactoe_score_moves \
    --json_folder="saves/tic_tac_toe_vs_solver"
```

Results appear in `saves/tic_tac_toe_vs_solver`, ready for analysis or Elo aggregation.

---

## 🔩 Configuration Files
SPIN‑Bench decouples *model definitions* from *game logic* through declarative JSON configs:

```jsonc
{
  "player1_model_list": [
    { "model": "our_solver", "prompt_config": [] }
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

*The i‑th entry of `player1_model_list` always faces the i‑th entry of `player2_model_list`; add or reorder entries to orchestrate round‑robins, self‑play, or ablations.*

Detailed prompt‑template documentation lives in **[`docs/prompt_config.md`](docs/prompt_config.md)**.

---

## 🎮 Usage

### Competitive Games
<details>
<summary><strong>Tic‑Tac‑Toe</strong></summary>

**LLM vs Solver**
```shell
python -m spinbench.tasks.tic_tac_toe.run_game_vs_solver \
    --store_folder="saves/tic_tac_toe_vs_solver" \
    --player_list="configs/solver_list_single.json" \
    --total_rounds=10
```

**LLM vs LLM**
```shell
python -m spinbench.tasks.tic_tac_toe.run_game \
    --store_folder="saves/tic_tac_toe_LLMs" \
    --player_list="configs/player_list_single.json" \
    --total_rounds=10
```

**Move Scoring**
```shell
python -m spinbench.tasks.evaluation.competitive.tictactoe_score_moves \
    --json_folder="saves/tic_tac_toe_LLMs"
```
</details>

<details>
<summary><strong>Connect 4</strong></summary>

**Launch solver service (once per machine):**
```shell
cd spinbench/tasks/connect4/
python c4solver.py --port 5000
cd ../../..
```

**Run games: LLM vs Solver**
```shell
python -m spinbench.tasks.connect4.run_game_vs_solver \
    --store_folder="saves/connect4_vs_solver" \
    --player_list="configs/solver_list_single.json" \
    --total_rounds=10
```

**Run games: LLM vs LLM**
```shell
python -m spinbench.tasks.connect4.run_game \
    --store_folder="saves/connect4_LLMs" \
    --player_list="configs/player_list_single.json" \
    --total_rounds=10
```
**Move Scoring**
```shell
python -m spinbench.tasks.evaluation.competitive.connect4_score_moves \
    --json_folder="saves/connect4_vs_solver"
```

</details>

<details>
<summary><strong>Chess</strong></summary>

Create a config such as:
```json
{
  "player1_model_list": [ { "model": "stockfish", "level": 0 } ],
  "player2_model_list": [ { "model": "gpt-4o", "prompt_config": [] } ]
}
```

The level of Stockfish can be set from 0 (weak) to 20 (strongest).

**LLM vs Stockfish**
```shell
python -m spinbench.tasks.chess.chess_stockfish \
    --store_folder="saves/chess_vs_stockfish" \
    --player_list="configs/stockfish-list-supp.json" \
    --stockfish_path="stockfish" \
    --total_rounds=2
```

**LLM vs LLM**
```shell
python -m spinbench.tasks.chess.run_game \
    --store_folder="saves/chess_LLMs" \
    --player_list="configs/player_list_single.json" \
    --total_rounds=2
```

**Move Scoring (Stockfish engine required)**
```shell
python -m spinbench.tasks.evaluation.competitive.chess_score_moves \
    --stockfish_path="stockfish" \
    --json_folder="saves/chess_LLMs"
```
</details>


### Win‑Rate, Win‑Stats, and Elo ratings for competitive games

```shell
python -m spinbench.tasks.evaluation.competitive.collect-solver-winrate \
    --directory="saves/connect4_LLMs" \
    --output="winrate.json"

python -m spinbench.tasks.evaluation.competitive.win_stats \
    --input="saves/connect4_LLMs" \
    --output="saves/connect4_LLMs/win_stats.csv"

python -m spinbench.tasks.evaluation.competitive.compute_elo \
    --input="saves/connect4_LLMs/win_stats.csv"
```

---

### Cooperative Game — Hanabi

To run a game of Hanabi, you need to set up a config file with the player models and their respective prompt configurations. An example config file is provided below:

```jsonc
// configs/hanabi_player_models.json
[
  { "model": "gemini-2.5-pro-preview-03-25", "prompt_config": [] },
  { "model": "gemini-2.5-pro-preview-03-25", "prompt_config": [] }
]
```

With this config, you can run a game of Hanabi with two players using the `gemini-2.5-pro-preview-03-25` model with the following command:

```shell
# run the game given the player models
python -m spinbench.tasks.hanabi.run_game \
    --player_models_json="configs/hanabi_player_models.json" \
    --store_folder="saves/hanabi" \
    --result_name="2gemini-2.5-pro-preview" \
    --total_rounds=5

# gather the results
python -m spinbench.tasks.evaluation.hanabi.gather_result \
    --store_folder="saves/hanabi" \
    --result_name="2gemini-2.5-pro-preview" \
    --total_rounds=5
```

---

### Multi‑Agent Game — Diplomacy

Extensive helper scripts are shown in **[`scripts/run_diplomacy`](scripts/run_diplomacy)**.  
A minimal *basic‑skill* example:

```shell
# power list
power_list="AUSTRIA ENGLAND FRANCE GERMANY ITALY RUSSIA TURKEY"

tested_model="gpt-4o_1"
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
  --save_folder=saves/diplomacy/${tested_model}-basic-skill
```

Generate evaluation metrics:
```shell
python -m spinbench.tasks.evaluation.diplomacy.eval \
    --game_folder="saves/diplomacy/gpt-4o_1-basic-skill" \
    --output_file="saves/diplomacy/gpt-4o_1-basic-skill/eval.json"
```

Negotiation‑specific evaluation requires **[`configs/neg_eval_config.json`](configs/neg_eval_config.json)**:
```shell
python -m spinbench.tasks.evaluation.diplomacy.eval_neg \
    --neg_config_file="configs/neg_eval_config.json"
```

---

## ✍️ Citation
If you build upon SPIN‑Bench, please cite:

```bibtex
@misc{yao2025spinbenchllmsplanstrategically,
  title        = {{SPIN‑Bench}: How Well Do LLMs Plan Strategically and Reason Socially?},
  author       = {Jianzhu Yao and Kevin Wang and Ryan Hsieh and Haisu Zhou and Tianqing Zou and Zerui Cheng and Zhangyang Wang and Pramod Viswanath},
  year         = {2025},
  eprint       = {2503.12349},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2503.12349}
}
```

---

## 💪 Contributing

We would love to hear from you! If you have any suggestions, bug reports, issues, or feature requests, please open an issue on our GitHub repository. If you would like to contribute code, please fork the repository and submit a pull request. We'll be sure to follow up shortly!

Have questions, ideas, or want to integrate a new game?  
Email **Jianzhu Yao** (<jy0246@princeton.edu>) or **Kevin Wang** (<kevinwang.1839@utexas.edu>).

---

## 🪪 License & Contact

SPIN‑Bench is released under the **MIT License**. See [`LICENSE`](LICENSE) for details.


Happy benchmarking!

