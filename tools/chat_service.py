import os
import json
from collections import OrderedDict
from openai import OpenAI
import regex
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import json
client = OpenAI()
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import llm_engine as lpb

current_dir = os.path.dirname(os.path.abspath(__file__))
# ollama list
# NAME                                                     ID              SIZE      MODIFIED       
# qwen2.5:72b                                              424bad2cc13f    47 GB     49 minutes ago    
# qwen2.5-coder:32b                                        4bd6cbf2d094    19 GB     57 minutes ago    
# qwen2.5:latest                                           845dbda0ea48    4.7 GB    11 hours ago      
# mistral:latest                                           f974a74358d6    4.1 GB    11 hours ago      
# qwen2.5-coder:latest                                     2b0496514337    4.7 GB    11 hours ago      
# llama3.2:latest                                          a80c4f17acd5    2.0 GB    11 hours ago      
# hf.co/bartowski/Llama-3-Groq-70B-Tool-Use-GGUF:Q5_K_S    2a4595cb3862    48 GB     3 weeks ago       
# llama3.1:70b-text-fp16                                   391fbe608631    141 GB    4 weeks ago       
# llama3.1:70b-instruct-fp16                               80d34437631f    141 GB    4 weeks ago       
# llama3.1:70b-instruct-q4_0                               c0df3564cfe8    39 GB     4 weeks ago       
# llama3:70b-instruct                                      786f3184aec0    39 GB     4 weeks ago       
# llama3.1:70b                                             c0df3564cfe8    39 GB     5 weeks ago       
# llama3.1:latest                                          42182419e950    4.7 GB    5 weeks ago

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
		if len(model_dict) >= 2:
			old_model, old_instance = model_dict.popitem(last=False)
			del old_instance
		model_dict[model] = lpb.BlackboxLLM(model, device=device)
	content = model_dict[model](messages)
	return content, 0