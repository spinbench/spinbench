import json
import regex
import llm_engine as lpb
model = lpb.BlackboxLLM("gpt-4o")
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

def parse_model_message(store_messages, phase_list, model):
	message_dict = {}
	store_messages = store_messages[2:] # skip the first two messages

	phase = phase_list[0]
	# print("phase", phase)
	message_dict[phase] = []
	state_descript = "Phase Name: The current game phase is '"+phase+"'."
	for m in store_messages:
		if m["role"] == "user":
			if "Phase Name: The current game phase is" in m["content"]:
				if state_descript not in m["content"]:
					if phase_list.index(phase) == len(phase_list)-1:
						break
					phase = phase_list[phase_list.index(phase)+1]
					message_dict[phase] = []
					state_descript = "Phase Name: The current game phase is '"+phase+"'."
		elif m["role"] == "assistant":
			if m["content"] == "":
				continue
			result, success = parse_json(m["content"])
			if success:
				message_dict[phase].append(result)
			else:
				raise ValueError("parse json failed", m["content"])
	return message_dict