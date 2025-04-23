import json
import glob
import argparse
import regex
import traceback
import os
from openai import OpenAI
client = OpenAI()
import re
import anthropic
import sys
anthropic_client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
)
from spinbench.tools.chat_service import get_chat
import spinbench.llm_engine as lpb
model = lpb.BlackboxLLM("gpt-4o") # model for fixing the json data
from diplomacy.utils.export import load_saved_games_from_disk
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
def parse_json(content):
	try:
		matches = json_pattern.findall(content)
		for match in matches:
			try:
				return json.loads(match), True
			except Exception as e:
				print(e)
				print("use model to fix the JSON data")
				new_data = model(f"\n{match}\n\nPlease convert the above incorrect JSON data to correct JSON data.")
				print("new_data", new_data)
				if new_data:
					try:
						matches = json_pattern.findall(new_data)
						for match in matches:
							return json.loads(match), True
					except:
						print("Failed to fix the JSON data")
				pass
	except:
		pass
	return None, False

def get_message(power1, power2, phase, model_power_dict,power2model):
	model1 = power2model[power1]
	model2 = power2model[power2]
	inter_message_list = [[], [], []]
	for i in range(3):
		if power1 in model_power_dict[model1]["sta"]["message_dict"][phase][i]["messages"]:
			message1 = model_power_dict[model1]["sta"]["message_dict"][phase][i]["messages"][power1]
		else:
			message1 = None
		if power2 in model_power_dict[model2]["sta"]["message_dict"][phase][i]["messages"]:
			message2 = model_power_dict[model2]["sta"]["message_dict"][phase][i]["messages"][power2]
		else:
			message2 = None
		if not message1 and not message2:
			continue
		# check whether power2 is in power1's recipient list
		if message1:
			if power2 in message1["recipients"]:
				inter_message_list[i].append(f"{power1} to {power2}: {message1['messages'][message1['recipients'].index(power2)]}")
		if message2:
			if power1 in message2["recipients"]:
				inter_message_list[i].append(f"{power2} to {power1}: {message2['messages'][message2['recipients'].index(power1)]}")
	return inter_message_list

def generate_eval_result_dict(config):
    """
    Generate an evaluation result dictionary based on the provided config.
    
    Args:
        config (dict): Configuration dictionary containing game_folder, 
                      power2model mappings, eval_model, and neg_by_phase_output_folder.
    
    Returns:
        dict: Structured evaluation result dictionary with all metrics initialized to 0.
    """
    # Extract unique model names from the power2model mapping
    unique_models = list(set(config["power2model"].values()))
    
    # Initialize the evaluation result dictionary
    eval_result = {
        "reasoning_and_negotiation_alignment": {model: 0 for model in unique_models},
        "proposals": {
            model: {
                "mutual_benefit": 0,
                "one_sided": 0,
                "accepted": 0,
                "total": 0,
            } for model in unique_models
        },
        "other_features": {
            model: {
                "peace": 0,
                "conflict": 0,
                "perspective_taking": 0,
                "conditional_thinking": 0,
            } for model in unique_models
        },
        "total_messages": {model: 0 for model in unique_models}
    }
    
    return eval_result

def generate_neg_metric_by_phase(neg_config_file):
	neg_config = json.load(open(neg_config_file, "r"))
	game_folder = neg_config["game_folder"]
	power2model = neg_config["power2model"]
	eval_model = neg_config["eval_model"]
	output_folder = neg_config["neg_by_phase_output_folder"]
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	game_state = json.load(open(os.path.join(game_folder, "diplomacy_game_state.json"),"r"))
	store_orders = game_state["store_orders"]
	model_power_dict = game_state["model_power_dict"]
	games = load_saved_games_from_disk(os.path.join(game_folder, "diplomacy_game_save.json"))
	game = games[-1]

	total_tokens = 0

	initial_prompt = "You are an expert in the game of Diplomacy. You are asked to evaluate the negotiation messages and the orders issued by the players in the game. "
	phase_list = ["S1901M"]
	for game in games:
		phase = game.get_current_phase()
		phase_list.append(phase)
	phase_list.pop(-1)
	total_messages = 0
	for phase in phase_list:
		eval_result = generate_eval_result_dict(neg_config)
		eval_meta_data = []
		prompt = ""
		if "W" in phase or "R" in phase:
			continue
		print("Phase: ", phase)
		for model in model_power_dict.keys():
			print("Model: ", model)
			messages = model_power_dict[model]["sta"]["message_dict"][phase]
			for i in range(3):
				try:
					message_dict = messages[i]
					for k in message_dict["messages"].keys():
						if k == "GLOBAL":
							continue
						for r in message_dict["messages"][k]["recipients"]:
							if r == "GLOBAL":
								continue
							# Create a unique ask_query for each message-recipient pair
							current_ask_query = {
								"negotiation_strategy": message_dict["negotiation_strategy"],
								"recipient": r,
								"message": message_dict["messages"][k]["messages"][message_dict["messages"][k]["recipients"].index(r)]
							}
							prompt = f"""
	{initial_prompt}This is the message you have to annotate. Please provide your evaluation of the message. You have to tell me 1. whether the message aligns with the negotiation strategy provided. 2. Are there any proposals in this message? If there is, are those proposals for mutual_benefit or only for one_sided? 3. Is this message promoting peace or provoking conflict? 4. Whether this message explicitly acknowledges or summarizes another power's viewpoint/needs? (perspective taking) 5. Whether this message uses conditional thinking/planning (for example, it's using if-then format)?

	In your response, please provide a json object with the following keys:
	- "alignment": 0 or 1 // 0 for not aligned, 1 for aligned
	- "proposals": [
			{{
				"proposal_text": "proposal_text", // the content of the proposal	
				"label": "mutual_benefit" or "one_sided" // "mutual_benefit" for mutual benefit, "one_sided" for one-sided benefit
			}},
		]
	- "peace_or_conflict": "peace" or "conflict" // "peace" for promoting peace, "conflict" for provoking conflict
	- "perspective_taking": 0 or 1 // 0 for not acknowledging or summarizing another power's viewpoint/needs, 1 for acknowledging or summarizing another power's viewpoint/needs
	- "conditional_thinking": 0 or 1 // 0 for not using conditional thinking/planning, 1 for using conditional thinking/planning

	Now please evaluate the following data:
	{current_ask_query}
	"""
							print(prompt)
							d, this_tokens = get_chat(eval_model, [{"role": "user", "content": prompt}])
							total_tokens += this_tokens
							d,s = parse_json(d)
							print(d)
							print("******************")
							if d:
								eval_result["reasoning_and_negotiation_alignment"][model] += d["alignment"]
								eval_result["proposals"][model]["mutual_benefit"] += sum([1 for p in d["proposals"] if p["label"] == "mutual_benefit"])
								eval_result["proposals"][model]["one_sided"] += sum([1 for p in d["proposals"] if p["label"] == "one_sided"])
								eval_result["proposals"][model]["total"] += len(d["proposals"])
								eval_result["other_features"][model]["peace"] += d["peace_or_conflict"].count("peace")
								eval_result["other_features"][model]["conflict"] += d["peace_or_conflict"].count("conflict")
								eval_result["other_features"][model]["perspective_taking"] += d["perspective_taking"]
								eval_result["other_features"][model]["conditional_thinking"] += d["conditional_thinking"]
								eval_meta_data.append({
									"ask_query": current_ask_query.copy(),  # Create a copy to prevent reference issues
									"response": d,
									"total_tokens": total_tokens,
								})
							else:
								print("Failed to parse the response")
							eval_result["total_messages"][model] += 1
							total_messages += 1

							# Store the current proposals for the second evaluation
							current_proposals = d["proposals"] if d else []
							
							inter_message_list = get_message(k, r, phase, model_power_dict, power2model)
							prompt = f"""
	{initial_prompt}

	The interaction between {k} and {r} in {phase} negotiation round 0:
	{inter_message_list[0]}
	The interaction between {k} and {r} in {phase} negotiation round 1:
	{inter_message_list[1]}
	The interaction between {k} and {r} in {phase} negotiation round 2:
	{inter_message_list[2]}

	The orders issued by {k} after the negotiation:
	{store_orders[phase+"-"+model][k] if k in store_orders[phase+"-"+model] else "No orders issued"}
	The orders issued by {r} after the negotiation:
	{store_orders[phase+"-"+power2model[r]][r] if r in store_orders[phase+"-"+power2model[r]] else "No orders issued"}

	Now please tell me for each proposal, whether it is accepted by the recipient or not. Please also provide the reason.

	Your response should be in json format with the following key:
	- "answer": [
			{{
				"proposal_text": "proposal_text", // the content of the proposal
				"accepted": 0 or 1, // 0 for not accepted, 1 for accepted
				"reason": "reason" // the reason why the proposal is accepted or not
			}},
		] // the order of the proposals should be the same as the order of the proposals in the previous response

	Those are the proposals {k} is sending to {r} in {phase} negotiation round {i}:
	{[p["proposal_text"] for p in current_proposals]}
	Your answer must be of the same length as the number of proposals.
	"""
							print(prompt)
							d, this_tokens = get_chat(eval_model, [{"role": "user", "content": prompt}])
							total_tokens += this_tokens
							print(d)
							if d:
								eval_result["proposals"][model]["accepted"] += sum([1 for p in d["answer"] if p["accepted"] == 1])
								eval_meta_data.append({
									"ask_query": current_ask_query.copy(),  # Use the same ask_query as the first evaluation
									"inter_message_list": inter_message_list,
									"model1_orders": store_orders[phase+"-"+model][k] if k in store_orders[phase+"-"+model] else "No orders issued",
									"model2_orders": store_orders[phase+"-"+power2model[r]][r] if r in store_orders[phase+"-"+power2model[r]] else "No orders issued",
									"response": d,
									"total_tokens": total_tokens,
								})
							else:
								print("Failed to parse the response")
				except Exception as e:
					print(e)
					traceback.print_exc()
					print("Failed to evaluate the message")
					pass			
		json.dump({
			"eval_result": eval_result,
			"eval_meta_data": eval_meta_data,
		}, open(f"{output_folder}/neg_eval_{phase}_{eval_model}.json", "w"), indent=2, ensure_ascii=False)

def gather_neg_result(neg_config_file, output_folder):
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	neg_config = json.load(open(neg_config_file, "r"))
	folder = neg_config["neg_by_phase_output_folder"]
	files = glob.glob(folder + "/*.json")
	eval_result = generate_eval_result_dict(neg_config)
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
	output_file = os.path.join(output_folder, "aggregated_results.json")
	with open(output_file, "w") as f:
		json.dump(eval_result, f, indent=2)
	print(f"Aggregated results saved to {output_file}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate negotiation metrics by phase")
	parser.add_argument("--neg_config_file", type=str, required=True, help="Path to the negotiation config file")
	parser.add_argument("--output_folder", type=str, required=True, help="Path to the output folder")
	args = parser.parse_args()
	generate_neg_metric_by_phase(args.neg_config_file)
	gather_neg_result(args.neg_config_file, args.output_folder)