import os
import json
from collections import OrderedDict
import regex
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import llm_engine as lpb

current_dir = os.path.dirname(os.path.abspath(__file__))
model_dict = OrderedDict()
fix_model  = lpb.BlackboxLLM("gpt-4o")
def fix_json(line):
	messages = [
		{
			"role": "user",
			"content": line + "\n\nthis is an invalid json string, please fix it to json format. You should generate a json string, the key is \"fixed\" and the value is the fixed json string. For example, {\"fixed\": \"{\"key\": \"value\"}\"}"
		},
	]
	content = fix_model(messages)
	try:
		parsed_json = None
		matches = json_pattern.findall(content)
		for match in matches:
			try:
				parsed_json = json.loads(match)
				print("Valid JSON Found:", parsed_json)
			except Exception as e:
				print("Invalid JSON Found:", match)
		return parsed_json["fixed"]
	except Exception as e:
		print(e)

def get_chat(model, messages, device=None):
	if model in model_dict:
		model_dict.move_to_end(model)
	else:
		if len(model_dict) >= 7:
			old_model, old_instance = model_dict.popitem(last=False)
			del old_instance
		model_dict[model] = lpb.BlackboxLLM(model, device=device)
	# print("messages:", messages)
	before_total_tokens = model_dict[model].engine.total_tokens
	# print("messages", messages)
	content = model_dict[model](messages)
	after_total_tokens = model_dict[model].engine.total_tokens
	return content, after_total_tokens - before_total_tokens