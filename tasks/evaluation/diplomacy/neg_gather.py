import json
import glob
import os
import sys

folder = "/home/jianzhu/LLm-pddl-benchmark/game/diplomacy/evaluation/neg_eval_211111_1by1"
files = glob.glob(folder + "/*.json")
eval_result = {
    "reasoning_and_negotiation_alignment": {
        "gpt-4o_1": 0,
        "claude-3-5-haiku-20241022_1": 0,
        "o1-preview_1": 0,
        "gpt-4-turbo_1": 0,
        "deepseek-reasoner_1": 0,
        "o1_1": 0,
    },
    "proposals": {
        "gpt-4o_1": {
            "mutual_benefit": 0,
            "one_sided": 0,
            "accepted": 0,
            "total": 0,
        },
        "claude-3-5-haiku-20241022_1": {
            "mutual_benefit": 0,
            "one_sided": 0,
            "accepted": 0,
            "total": 0,
        },
        "o1-preview_1": {
            "mutual_benefit": 0,
            "one_sided": 0,
            "accepted": 0,
            "total": 0,
        },
        "gpt-4-turbo_1": {
            "mutual_benefit": 0,
            "one_sided": 0,
            "accepted": 0,
            "total": 0,
        },
        "deepseek-reasoner_1": {
            "mutual_benefit": 0,
            "one_sided": 0,
            "accepted": 0,
            "total": 0,
        },
        "o1_1": {
            "mutual_benefit": 0,
            "one_sided": 0,
            "accepted": 0,
            "total": 0,
        },
    },
    "other_features": {
        "gpt-4o_1": {
            "peace": 0,
            "conflict": 0,
            "perspective_taking": 0,
            "conditional_thinking": 0,
        },
        "claude-3-5-haiku-20241022_1": {
            "peace": 0,
            "conflict": 0,
            "perspective_taking": 0,
            "conditional_thinking": 0,
        },
        "o1-preview_1": {
            "peace": 0,
            "conflict": 0,
            "perspective_taking": 0,
            "conditional_thinking": 0,
        },
        "gpt-4-turbo_1": {
            "peace": 0,
            "conflict": 0,
            "perspective_taking": 0,
            "conditional_thinking": 0,
        },
        "deepseek-reasoner_1": {
            "peace": 0,
            "conflict": 0,
            "perspective_taking": 0,
            "conditional_thinking": 0,
        },
        "o1_1": {
            "peace": 0,
            "conflict": 0,
            "perspective_taking": 0,
            "conditional_thinking": 0,
        },
    },
    "total_messages": {
        "gpt-4o_1": 0,
        "claude-3-5-haiku-20241022_1": 0,
        "o1-preview_1": 0,
        "gpt-4-turbo_1": 0,
        "deepseek-reasoner_1": 0,
        "o1_1": 0,
    },
}

for json_file in files:
    with open(json_file) as f:
        data = json.load(f)
        for category in eval_result:
            for model in eval_result[category]:
                if isinstance(eval_result[category][model], dict):
                    for sub_key in eval_result[category][model]:
                        eval_result[category][model][sub_key] += data["eval_result"][category][model][sub_key]
                else:
                    eval_result[category][model] += data["eval_result"][category][model]
for model in eval_result["proposals"]:
    eval_result["proposals"][model]["accepted_rate"] = eval_result["proposals"][model]["accepted"] / eval_result["proposals"][model]["total"] if eval_result["proposals"][model]["total"] > 0 else 0
    eval_result["proposals"][model]["mut/one"] = eval_result["proposals"][model]["mutual_benefit"] / eval_result["proposals"][model]["one_sided"] if eval_result["proposals"][model]["one_sided"] > 0 else 0
eval_result["align_ratio"] = {}
for model in eval_result["reasoning_and_negotiation_alignment"]:
    eval_result["align_ratio"][model] = eval_result["reasoning_and_negotiation_alignment"][model] / eval_result["total_messages"][model] if eval_result["total_messages"][model] > 0 else 0
for model in eval_result["other_features"]:
    eval_result["other_features"][model]["peace/conflict"] = eval_result["other_features"][model]["peace"] / eval_result["other_features"][model]["conflict"] if eval_result["other_features"][model]["conflict"] > 0 else 0
    eval_result["other_features"][model]["perspective_rate"] = eval_result["other_features"][model]["perspective_taking"] / eval_result["total_messages"][model] if eval_result["total_messages"][model] > 0 else 0
    eval_result["other_features"][model]["conditional_rate"] = eval_result["other_features"][model]["conditional_thinking"] / eval_result["total_messages"][model] if eval_result["total_messages"][model] > 0 else 0
output_file = os.path.join(folder, "aggregated_results.json")
with open(output_file, "w") as f:
    json.dump(eval_result, f, indent=4)

print(f"Aggregated results saved to {output_file}")


