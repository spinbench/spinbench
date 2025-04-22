Here’s a guide covering both how to design your own `prompt_config` blocks and how to assemble a full JSON-format config file for the two‐player setup.

---

## Customizing `prompt_config`

Each entry in `prompt_config` defines an augmentation to the basic “give me your next move” flow. Under the hood, our `play()` function will translate each named config into a hook that runs **before** the model is asked to choose its next action.

```json
{
  "prompt_config": [
    {
      "name": "<hook-name>",
      "params": {
        /* hook‑specific parameters */
      }
    }
  ]
}
```

---

### Available Hooks

1. **forced-reasoning**  
   **When to use**: You want the model to pause and produce explicit chain‑of‑thought reasoning before moving.  
   **Params**:
   - `interactive_times` (int) — how many times to invoke the reasoning prompt  
   - `prompt_messages` (array of strings) — each message to feed *in turn* to solicit reasoning  

2. **reasoning-history**  
   **When to use**: You want to remind the model of its last _N_ action/reason pairs so it can build on its recent chain of thought.  
   **Params**:
   - `count` (int) — how many past steps to include  

3. **prompting-code**  
   **When to use**: You want the model to generate or modify code snippets mid‑game.  
   **Params** identical to `forced-reasoning`:  
   - `interactive_times`  
   - `prompt_messages`  

4. **implicit-knowledge-generation**  
   **When to use**: You want the model to surface any unstated domain knowledge (e.g. game heuristics) before choosing.  
   **Params** identical to `forced-reasoning`.

5. **future-based-reasoning**  
   **When to use**: You want the model to speculate about possible future states before acting.  
   **Params** identical to `forced-reasoning`.

6. **in-context-learning-case**  
   **When to use**: You want to feed a single illustrative example (e.g. a sample best move+reason).  
   **Params**:
   - `prompt_messages` (array of exactly one string)

7. **in-context-learning-experience**  
   **When to use**: You want to provide a single tip or tactic the model should adopt.  
   **Params**:
   - `prompt_messages` (array of exactly one string)

---

### How Hooks Are Wired

1. **Name** → the Python hook function in `play_service.py`.  
2. **Params** → unpacked into that function; e.g.:

   ```python
   hook_functions[forced_reasoning] = {
     "interactive_times": params["interactive_times"],
     "prompt_messages": params["prompt_messages"]
   }
   ```

3. All hooks run in the order:  
   1. `reasoning-history` (if any)  
   2. `add_state_description` (always)  
   3. **Other** prompt hooks in the order you list them  
   4. `action_prompt` (always)  

---

## Writing the Full Config File

At the top level, you specify two lists, one per player:

```json
{
  "player1_model_list": [
    {
      "model": "<model-name>",
      "prompt_config": [
        /* zero or more hooks */
      ]
    }
  ],
  "player2_model_list": [
    {
      "model": "<another-model>",
      "prompt_config": [
        /* zero or more hooks */
      ]
    }
  ]
}
```

### Minimal Example

No extra reasoning, just feed state + ask for a move:

```json
{
  "player1_model_list": [
    {
      "model": "gpt-4o-mini",
      "prompt_config": []
    }
  ],
  "player2_model_list": [
    {
      "model": "gpt-4o-mini",
      "prompt_config": []
    }
  ]
}
```

### Advanced Example

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
              "Analyze all previous moves in detail. Then stop—do not play yet."
            ]
          }
        },
        {
          "name": "in-context-learning-case",
          "params": {
            "prompt_messages": [
              "Example:\nMove: E2→E4\nReason: Controls center early."
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
          "name": "reasoning-history",
          "params": {
            "count": 3
          }
        },
        {
          "name": "future-based-reasoning",
          "params": {
            "interactive_times": 2,
            "prompt_messages": [
              "What are three possible responses I might face next turn?",
              "Which of those is most dangerous and why?"
            ]
          }
        }
      ]
    }
  ]
}
```

---

## Tips for Designing Your Prompts

- **Be explicit**: Tell the model *exactly* what form you want its reasoning to take.  
- **Limit verbosity**: If you only need 1 chain‑of‑thought, set `interactive_times: 1`.  
- **Order matters**: Early hooks (like history) prime later ones.  
- **Test iteratively**: Start simple, then layer in more hooks as you see gaps.  
- **Use examples**: In‑context prompts can help “demonstrate” the style you expect.  

With this structure in place, you can mix & match reasoning, history, code generation, or future speculation to tailor the agent’s inner loop exactly to your game or task. This can lead to more strategic, informed, and ultimately more effective decision-making.