Below is a reference for your **player_list_config.json** format. You’ll supply two arrays—one for each side—each containing one or more “player” objects.  Depending on the kind of agent you’re plugging in, the object can be:

- **LLM‑based**: specify `"model"` and an optional `"prompt_config"` array  
- **Chess Stockfish engine**: specify `"model"` and engine‑specific params (e.g. `"level"` for Stockfish)  
- **Custom solver**: specify `"our_solver"`

> **See also:** full details on each `prompt_config` hook for LLMs are in [doc/prompt_config.md](doc/prompt_config.md).

---

## Top‑Level Structure

```json
{
  "player1_model_list": [ /* one or more player objects */ ],
  "player2_model_list": [ /* one or more player objects */ ]
}
```

Each list represents the “team” of agents controlling White (player1) or Black (player2).  You can include multiple entries per team to run *multiple* agents.

---

## 1. LLM‑Controlled Agent

Use when the agent is driven by a hosted LLM.  You can layer in any number of `prompt_config` hooks to customize chain‑of‑thought, history replay, code gen, etc.

```jsonc
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
```

- `model`  
  The LLM identifier your runner will call (e.g. `"gpt-4o"`, `"our_solver"`, `"gpt-4o-mini"`).  
- `prompt_config`  
  Array of zero or more hook definitions.  See `doc/prompt_config.md` for the full list of hook names and params.

---

## 2. Chess Engine (Stockfish)

If you prefer a classic engine, just supply its model name plus engine‑specific settings:

```jsonc
{
  "model": "stockfish",
  "level": 0
}
```

- `model`  
  Must match the engine your code registers (e.g. `"stockfish"`).  
- `level`  
  Difficulty or depth parameter—whatever your wrapper expects. This can range from 0 (easy) to 20 (very hard).

---

## 3. Custom Solver

Plug in any other algorithm by name—no hooks needed:

```jsonc
{
  "model": "our_solver",
  "prompt_config": []
}
```

Your runner will dispatch to whatever logic lives under `"our_solver"`. Any prompt_config hooks will be ignored here.

---

## Putting It All Together

Here are three complete examples illustrating common patterns:

### Example A: Custom Solver vs. LLM

```json
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
      "prompt_config": []
    }
  ]
}
```

### Example B: Stockfish vs. LLM

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
      "prompt_config": []
    }
  ]
}
```

### Example C: Two LLMs with Forced Reasoning

```json
{
  "player1_model_list": [
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
  ],
  "player2_model_list": [
    {
      "model": "gpt-4o-mini",
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

---

## Further Reading

- **`doc/prompt_config.md`** — deep dive on each `prompt_config` hook (names, params, examples)
- **Runner code** — see `play_service.py` to understand exactly how your config drives the hook pipeline.