NOTE: You have to run the [basic evaluation script](spinbench/tasks/evaluation/diplomacy/eval.py) for Diplomacy first, and then run the negotiation evaluation script.

Here’s a reference for your **Negotiation Annotation** configuration:

---

## Negotiation Annotation Config for Diplomacy

When you want to **post‑process** a saved Diplomacy game’s negotiation phase—e.g. label, summarize or score each message—you point to your game folder, tell the system which model controlled each power, and specify an `eval_model` to do the annotation.

```json
{
  "game_folder": "/path/to/diplomacy_saves/<your‑game>",
  "power2model": {
    "AUSTRIA": "gpt-4o_1",
    "ITALY":   "claude-3-5-haiku-20241022_1",
    "TURKEY":  "claude-3-5-haiku-20241022_1",
    "FRANCE":  "o1-preview_1",
    "RUSSIA":  "gpt-4-turbo_1",
    "GERMANY": "deepseek-reasoner_1",
    "ENGLAND": "o1_1"
  },
  "eval_model":    "claude-3-7-sonnet-20250219",
  "neg_by_phase_output_folder": "neg_result"
}
```

### Field Descriptions

- **`game_folder`**  
  The directory where your game lives.  
  The annotation script will scan all negotiation messages in that folder.

- **`power2model`**  
  A mapping from each Power name → the model string that played it (with `_N` suffix).  
  This lets the annotator know which agent “owns” each message.

- **`eval_model`**  
  The single model used to annotate **all** negotiation messages.  
  It could be a more powerful or specialized model (e.g. `claude-3-7‑sonnet‑20250219`) that:  
  - Labels each message (e.g. “promise”, “threat”)  
  - Scores persuasiveness or detect lies  
  - Summarizes proposals

- **`neg_by_phase_output_folder`**  
  Where the script will write its results

---

## How to Run Negotiation Annotation

With your config saved in `configs/neg_eval_config.json`, invoke:

```bash
python -m spinbench.tasks.evaluation.diplomacy.eval_neg \
    --neg_config_file="/home/jianzhu/spinbench/configs/neg_eval_config.json"
```

This will:

1. **Load** all turn files from `game_folder`.  
2. **Extract** every negotiation message (sender, recipients, timestamp, content).  
3. **Call** `get_chat(eval_model, [system + user prompt])` for each, asking it to annotate.  
4. **Save** the enriched records under `neg_by_phase_output_folder/`.

---

## Tips

- **Reuse** the same `_N` suffix in `power2model` if one agent plays multiple powers.  