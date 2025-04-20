from tools.chat_service import get_chat
import copy

# player1_model_list = [
# 	{
# 		"model": "gpt-4o-mini",
# 		"prompt_config": [],
# 	},
# 	{
# 		"model": "gpt-4o-mini",
# 		"prompt_config": [
# 			{
# 				"name": "forced-reasoning",
# 				"params": {
# 					"interactive_times": 1,
# 					"prompt_messages": ["Please reason about the current state. You should analyze all the opponent's moves and your moves, try to reason opponent's thought in detail."]
# 				}
# 			}
# 		]
# 	},
# 	{
# 		"model": "gpt-4o-mini",
# 		"prompt_config": [
# 			{
# 				"name": "reasoning-history",
# 				"params": {
# 					"count": 3,
# 				}
# 			}
# 		]
# 	}
# ]

def play(player_messages, player_store_message, player_model, player_reasoning_action_steps, state_description, legal_move_description, legal_moves, gen_move=None, illegal_tolerance=10,print_content=True, hook_functions=None,player_index=None, **kwargs):
    # in hook_functions, key is the function, and the value is the additional arguments
    win = None
    game_state = None
    added_tokens = 0
    if "legal_move_list" in kwargs.keys():
        legal_move_list = kwargs["legal_move_list"]
    else:
        legal_move_list = copy.deepcopy(legal_moves)
    for i in range(len(legal_move_list)):
        legal_move_list[i] = str(legal_move_list[i])
    for k in hook_functions:
        k(player_messages, player_store_message, player_model, **hook_functions[k])
    move, content, used_token, action, reason = gen_move(player_messages, player_model, **kwargs)
    print(move, legal_moves)
    added_tokens += used_token
    while illegal_tolerance > 0 and (move not in legal_moves or move == None):
        print(content)
        print("Illegal move for player", player_model, "try again")
        illegal_tolerance -= 1
        player_messages.extend([
            {"role": "assistant", "content": content},
            # {"role": "user", "content": "Illegal move, try again, your legal moves are: " + " ".join(legal_move_list)}
            {"role": "user", "content": "Illegal move, try again"}
        ])
        player_store_message.extend([
            {"role": "assistant", "content": content},
            # {"role": "user", "content": "Illegal move, try again, your legal moves are: " + " ".join(legal_move_list)}
            {"role": "user", "content": "Illegal move, try again"}
        ])
        move, content, used_token, action, reason = gen_move(player_messages, player_model)
        added_tokens += used_token
    if print_content:
        print(content)
    player_store_message.append({
        "role": "assistant",
        "content": content
    })
    if move not in legal_moves or move == None:
        print("Player", player_model, "exceeded illegal move tolerance")
        if player_index == 0:
            win = 3
        elif player_index == 1:
            win = 4
        game_state = "Player " + player_model + " illegal move!"
    else:
        player_reasoning_action_steps.append({
            "action": action,
            "reason": reason
        })
    return move, action, win, game_state, added_tokens

def forced_reasoning(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None):
    # user prompting the assistant to reason about the current state2
    assert len(prompt_messages) == interactive_times, "Prompt messages should be the same as the interactive times"
    for i in range(interactive_times):
        append_user_message(player_messages, player_store_message, prompt_messages[i])
        content, used_token = get_chat(player_model, player_messages)
        append_assistant_message(player_messages, player_store_message, content)

def prompting_code(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None):
    # user prompting the assistant to generate code
    assert len(prompt_messages) == interactive_times, "Prompt messages should be the same as the interactive times"
    for i in range(interactive_times):
        append_user_message(player_messages, player_store_message, prompt_messages[i])
        content, used_token = get_chat(player_model, player_messages)
        print(content)
        append_assistant_message(player_messages, player_store_message, content)

def implicit_knowledge_generation(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None):
    # user asking the assistant to generate implicit knowledge
    assert len(prompt_messages) == interactive_times, "Prompt messages should be the same as the interactive times"
    for i in range(interactive_times):
        append_user_message(player_messages, player_store_message, prompt_messages[i])
        content, used_token = get_chat(player_model, player_messages)
        append_assistant_message(player_messages, player_store_message, content)

def future_based_reasoning(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None):
    # user prompting the assistant to reason about the future
    assert len(prompt_messages) == interactive_times, "Prompt messages should be the same as the interactive times"
    for i in range(interactive_times):
        append_user_message(player_messages, player_store_message, prompt_messages[i])
        content, used_token = get_chat(player_model, player_messages)
        append_assistant_message(player_messages, player_store_message, content)

def in_context_learning_case(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None):
    # user providing some examples
    assert len(prompt_messages) == 1, "Only one prompt message is allowed"
    append_user_message(player_messages, player_store_message, prompt_messages[0])

def in_context_learning_experience(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None):
    # user providing some game tricks or strategies
    assert len(prompt_messages) == 1, "Only one prompt message is allowed"
    append_user_message(player_messages, player_store_message, prompt_messages[0])

def reasoning_history(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None, player_reasoning_action_steps=None,count=3):
    # generate reasoning prompt
    append_user_message(player_messages, player_store_message, generate_reasoning_prompt(player_reasoning_action_steps,count))

def add_state_description(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None, state_description=None):
    # state_description
    append_user_message(player_messages, player_store_message, state_description)

def action_prompt(player_messages=None, player_store_message=None, player_model=None, interactive_times=None, prompt_messages=None, action_prompt=None):
    assert action_prompt is not None
    append_user_message(player_messages, player_store_message, action_prompt)


def generate_reasoning_prompt(player_reasoning_action_steps,count):
	li = [f"Move: {step['action']}\nReason: {step['reason']}" for step in player_reasoning_action_steps[-count:]]
	steps = "\n---------------------------\n".join(li)
	return f"""
Your previous moves and thinking are below  (in the last {count} moves in the order of the oldest to the newest):
<previous_moves>
{steps}
</previous_moves>
"""

def append_user_message(player_messages, player_store_message, user_message):
    # check the role of the last message
    if len(player_messages) == 0 or player_messages[-1]["role"] == "assistant":
        player_messages.append({
            "role": "user",
            "content": user_message
        })
        player_store_message.append({
            "role": "user",
            "content": user_message
        })
    elif player_messages[-1]["role"] == "user":
        player_messages[-1]["content"] += "\n" + user_message
        player_store_message[-1]["content"] += "\n" + user_message

def append_assistant_message(player_messages, player_store_message, assistant_message):
    player_messages.append({
        "role": "assistant",
        "content": assistant_message
    })
    player_store_message.append({
        "role": "assistant",
        "content": assistant_message
    })

def append_message_pair(player_messages, player_store_message, message_list):
    assert len(message_list) == 2, "Message list should have two messages"
    assert player_messages[-1]["role"] == "assistant", "The last message should be assistant"
    player_messages.extend(message_list)
    player_store_message.extend(message_list)

def create_hook_functions(model, player_reasoning_action_steps, state_description, action_prompt_text):
    prompt_dict = {}
    for prompt in model["prompt_config"]:
        prompt_dict[prompt["name"]] = prompt["params"]

    hook_functions = {}
    if "reasoning-history" in prompt_dict.keys():
        hook_functions[reasoning_history] = { "count": prompt_dict["reasoning-history"]["count"], "player_reasoning_action_steps": player_reasoning_action_steps }

    # necessary
    hook_functions[add_state_description] = { "state_description": state_description }

    if "forced-reasoning" in prompt_dict.keys():
        hook_functions[forced_reasoning] = { "interactive_times": prompt_dict["forced-reasoning"]["interactive_times"], "prompt_messages": prompt_dict["forced-reasoning"]["prompt_messages"] }

    if "prompting-code" in prompt_dict.keys():
        hook_functions[prompting_code] = { "interactive_times": prompt_dict["prompting-code"]["interactive_times"], "prompt_messages": prompt_dict["prompting-code"]["prompt_messages"] }

    # necessary
    hook_functions[action_prompt] = { "action_prompt": action_prompt_text }

    return hook_functions
