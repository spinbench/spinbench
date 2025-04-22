Below is a self‐contained reference for wiring up and running a Diplomacy match via the `spinbench.tasks.diplomacy.run_game` entrypoint, using a Bash wrapper to map powers to agent models. We take [scripts/run_diplomacy/run_3_players.sh](scripts/run_diplomacy/run_3_players.sh) as an example here:

---

## 1. Your Powers (Don't change this)

We list out the seven Powers in one space‑separated string for your reference. The order here is fixed and will determine the index when you assign models.

```bash
# 7 Powers in order (indexes 0–6)
power_list="AUSTRIA ENGLAND FRANCE GERMANY ITALY RUSSIA TURKEY"
```

> **Tip:** Whatever number you pass to `--num_powers` must match the count in `power_list`.

---

## 2. Declare Your Agent Models

Each agent gets a name plus a suffix `_N` to indicate which “instance” it is.  Reusing the same suffix means multiple powers are controlled by the *same* agent.

```bash
# Agent definitions (you can add more with _2, _3, etc.)
model1="gpt-4-turbo_1"
model2="o1_1"
model3="gpt-4o_1"
```

- The string before the underscore is the model name.  
- The number after the underscore groups powers under the same agent.

---

## 3. Map Powers → Models

Create a Bash array whose entries line up **one‑to‑one** with `power_list`.  Index 0 (`AUSTRIA`) gets `model_list[0]`, index 1 (`ENGLAND`) gets `model_list[1]`, and so on.

```bash
model_list=(
  ${model3}  # AUSTRIA
  ${model3}  # ENGLAND
  ${model3}  # FRANCE
  ${model1}  # GERMANY
  ${model1}  # ITALY
  ${model2}  # RUSSIA
  ${model2}  # TURKEY
)
```

This example gives the first three powers to `gpt-4o_1`, the next two to `gpt-4-turbo_1`, and the last two to `o1_1`.

---

## 4. Build the Comma‑Separated Model String

`run_game` expects a single comma‑delimited list in the same order as your powers:

```bash
model_str=$(IFS=,; echo "${model_list[*]}")
# => "gpt-4o_1,gpt-4o_1,gpt-4o_1,gpt-4-turbo_1,gpt-4-turbo_1,o1_1,o1_1"
```

---

## 5. Invoke the Runner

Below is a typical call with all the most common flags:

```bash
python -m spinbench.tasks.diplomacy.run_game \
  --num_powers=7 \
  --winning_centers=20 \
  --max_tokens=10000000 \
  --max_years=1920 \
  --model_names="${model_str}" \
  --temperature=0.9 \
  --top_p=1.0 \
  --state_file=diplomacy_game_state.json \
  --enable_negotiation=0 \
  --negotiation_rounds=3 \
  --save_folder="223-no-neg"
```

| Flag                    | Description                                                   |
|-------------------------|---------------------------------------------------------------|
| `--num_powers`          | How many powers in play, should be 7 (must match `power_list`)|
| `--winning_centers`     | # of supply centers required for victory                     |
| `--max_tokens`          | Total token budget across all moves                          |
| `--max_years`           | Simulation end year (e.g. 1920)                              |
| `--model_names`         | Comma‑separated model strings, one per power                 |
| `--temperature`         | Sampling temperature                                         |
| `--top_p`               | Nucleus sampling parameter                                   |
| `--state_file`          | Name of the file to load/save intermediate game state        |
| `--enable_negotiation`  | `0` to disable or `1` to enable diplomatic negotiation phase |
| `--negotiation_rounds`  | How many negotiation rounds per year                         |
| `--save_folder`         | Directory where logs and states will be dumped,used for resuming the game|

---

## 6. Putting It All Together

```bash
#!/usr/bin/env bash

# 1. Powers
power_list="AUSTRIA ENGLAND FRANCE GERMANY ITALY RUSSIA TURKEY"

# 2. Agents
model1="gpt-4-turbo_1"
model2="o1_1"
model3="gpt-4o_1"

# 3. Map powers → agents
model_list=(
  ${model3}  # AUSTRIA
  ${model3}  # ENGLAND
  ${model3}  # FRANCE
  ${model1}  # GERMANY
  ${model1}  # ITALY
  ${model2}  # RUSSIA
  ${model2}  # TURKEY
)

# 4. Make comma‑string
model_str=$(IFS=,; echo "${model_list[*]}")

# 5. Run the game
python -m spinbench.tasks.diplomacy.run_game \
  --num_powers=7 \
  --winning_centers=20 \
  --max_tokens=10000000 \
  --max_years=1920 \
  --model_names="${model_str}" \
  --temperature=0.9 \
  --top_p=1.0 \
  --state_file=diplomacy_game_state.json \
  --enable_negotiation=0 \
  --negotiation_rounds=3 \
  --save_folder="223-no-neg"
```

With this pattern you can flexibly assign any number of models (and let one model control multiple powers) by tweaking the `_N` suffix and the order of `model_list`. Happy gaming!