import json
import regex
import time
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
import llm_engine as lpb
model = lpb.BlackboxLLM("gpt-4o") # model for fixing the json data
claudemodel = lpb.BlackboxLLM("claude-3-7-sonnet-20250219")
from diplomacy import Game, Message
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk
from diplomacy.utils.game_phase_data import GamePhaseData, MESSAGES_TYPE
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

def chat(prompt, model):
	# chat_completion = client.chat.completions.create(
	# 	messages=[{"role": "user", "content": prompt}],
	# 	model=model,
	# )
	chat_completion = anthropic_client.messages.create(
		messages=[{"role": "user", "content": prompt}],
		model=model,
		max_tokens=2000,
	)
	total_tokens = chat_completion.usage.to_dict().get("total_tokens", 0)
	input_tokens = chat_completion.usage.to_dict().get("prompt_tokens", 0)
	output_tokens = chat_completion.usage.to_dict().get("completion_tokens", 0)
	# response = chat_completion.choices[0].message.content
	response = chat_completion.content[0].text
	d,s = parse_json(response)
	if not s:
		print("Failed to parse the response")
		print(response)
		return None, total_tokens, input_tokens, output_tokens
	return d, total_tokens, input_tokens, output_tokens

prompt_template = open("prompt.md", "r").read()
game_folder = "/home/jianzhu/LLm-pddl-benchmark/game/diplomacy/diplomacy_saves/multi-211111-talk-fix"
config = json.load(open(os.path.join(game_folder, "config.json"),"r"))
game_state = json.load(open(os.path.join(game_folder, "diplomacy_game_state.json"),"r"))
store_orders = game_state["store_orders"]
model_power_dict = game_state["model_power_dict"]
models = list(model_power_dict.keys())
model2power = {
	"gpt-4o_1": ["AUSTRIA",],
	"claude-3-5-haiku-20241022_1": ["ITALY", "TURKEY"],
	"o1-preview_1": ["FRANCE", ],
	"gpt-4-turbo_1": ["RUSSIA"],
	"deepseek-reasoner_1": ["GERMANY"],
	"o1_1": ["ENGLAND"],
}
power2model = {
	"AUSTRIA": "gpt-4o_1",
	"ITALY": "claude-3-5-haiku-20241022_1",
	"TURKEY": "claude-3-5-haiku-20241022_1",
	"FRANCE": "o1-preview_1",
	"RUSSIA": "gpt-4-turbo_1",
	"GERMANY": "deepseek-reasoner_1",
	"ENGLAND": "o1_1",
}
def get_message(power1, power2, phase, model_power_dict):
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

games = load_saved_games_from_disk(os.path.join(game_folder, "diplomacy_game_save.json"))
eval_model = "claude-3-7-sonnet-20250219"
total_tokens = 0
input_tokens = 0
output_tokens = 0
game = games[-1]

initial_prompt = "You are an expert in the game of Diplomacy. You are asked to evaluate the negotiation messages and the orders issued by the players in the game. "

phase_list = ["S1901M"]
for game in games:
	phase = game.get_current_phase()
	phase_list.append(phase)
phase_list.pop(-1)
total_messages = 0
for phase in phase_list:
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
	eval_meta_data = []
	prompt = ""
	if "W" in phase or "R" in phase:
		continue
	print("Phase: ", phase)
	if phase == "F1902M":
		exit(0)
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
						d, total_tokens, input_tokens, output_tokens = chat(prompt, eval_model)
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
								"input_tokens": input_tokens,
								"output_tokens": output_tokens,
							})
						else:
							print("Failed to parse the response")
						eval_result["total_messages"][model] += 1
						total_messages += 1

						# Store the current proposals for the second evaluation
						current_proposals = d["proposals"] if d else []
						
						inter_message_list = get_message(k, r, phase, model_power_dict)
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
						d, total_tokens, input_tokens, output_tokens = chat(prompt, eval_model)
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
								"input_tokens": input_tokens,
								"output_tokens": output_tokens,
							})
						else:
							print("Failed to parse the response")
						exit(0)
			except Exception as e:
				print(e)
				traceback.print_exc()
				print("Failed to evaluate the message")
				pass			
	json.dump({
		"eval_result": eval_result,
		"eval_meta_data": eval_meta_data,
	}, open(f"neg_eval_211111_1by1_new/neg_eval_{phase}_{eval_model}.json", "w"), indent=2, ensure_ascii=False)