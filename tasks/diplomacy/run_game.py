"""
Refactored Diplomacy Code with Configurable Settings

This script initializes a Diplomacy game, sets up a specified number of agents
and language models, and runs a game loop that includes negotiation phases and
action phases. It can store state into a single JSON file, allowing you to resume
the game gracefully.

Command-line arguments:
--num_agents: The number of players (agents). Defaults to 7.
--winning_centers: The minimum number of supply centers needed to win the game. Defaults to 18.
--max_tokens: The maximum cumulative tokens to allow before ending the game. Defaults to 100000.
--model_names: Comma-separated model names for each agent, e.g. "gpt-4,gpt-3.5,gpt-3.5,..."
--temperature: OpenAI temperature hyperparameter. Defaults to 1.0.
--top_p: OpenAI top_p hyperparameter. Defaults to 1.0.
--state_file: JSON file to store and resume game states. Defaults to "diplomacy_game_state.json".
--enable_negotiation: Whether to enable negotiation rounds. Defaults to 1 (enabled).
--negotiation_rounds: Number of negotiation rounds per move phase. Defaults to 3.
--store_folder: Folder to store game state and messages.


Example usage:
python diplomacy_refactored.py
--num_agents 7
--winning_centers 18
--max_tokens 500000
--model_names "gpt-4,gpt-4,gpt-3.5,gpt-3.5,gpt-4,gpt-3.5,gpt-4"
--temperature 0.7
--top_p 0.9
--state_file "my_saved_game.json"
--enable_negotiation 1
--negotiation_rounds 3
--store_folder "my_game_store"
"""
import time
import copy
import anthropic
import traceback
import os
import requests
import re
import sys
import json
import argparse
from collections import defaultdict
from diplomacy import Game, Message
from diplomacy.utils import common
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk
from diplomacy.utils.sorted_dict import SortedDict
from openai import OpenAI
from diplomacy_utils import (
    parse_diplomacy_state,
    get_message_text_bundle,
    gen_round_prompt,
    gen_message_prompt,
    gen_action_prompt,
    get_message_text,
    gen_init_prompt,
    gen_winter_action_prompt,
    generate_phase_history_prompt,
    append_user_message,
    append_assistant_message,
    gen_retreat_action_prompt,
    gen_winter_action_prompt_bundle,
    gen_action_prompt_bundle,
    gen_retreat_action_prompt_bundle,
    gen_init_prompt_bundle,
    gen_negotiation_prompt_bundle,
)
JSON_PATTERN = re.compile(r"({(.|\n)*})")
anthropic_client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
)
headers = {
  'Authorization': "Bearer "+os.environ.get("OPENROUTER_API_KEY"),
  'Content-Type': "application/json",
}
# response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json={
#     'model': 'mistralai/mixtral-8x7b-instruct',
#     'messages': [
#       {
#         'role': 'user',
#         'content': 'Hello'
#       }
#     ],
#     'provider': {
#       'order': [
#         'OpenAI',
#         'Together'
#       ],
#       'allow_fallbacks': False
#     }
# })


def format_adj_information(adj_info):
    """
    Takes a list of dictionaries representing adjacencies and returns a human-readable string.
    """
    lines = []
    for entry in adj_info:
        # Each dictionary has one key with a list of adjacent items.
        for region, neighbors in entry.items():
            # Format neighbors as a comma-separated string.
            neighbor_str = ", ".join(neighbors)
            line = f"{region} is adjacent to: {neighbor_str}."
            lines.append(line)
    # Join all lines into a single formatted string.
    return "\n".join(lines)

def end_game_check(game, winning_centers, max_tokens, max_years, total_tokens):
    # Check game outcome dynamically: If any power has >= winning_centers, end.
    # The diplomacy library automatically updates game.is_game_done if
    # a player hits 18 centers in standard. But if your victory condition is custom,
    # you can add your own check here.
    for p_name, p_obj in game.powers.items():
        if len(p_obj.centers) >= winning_centers:
            print(f"{p_name} has reached {winning_centers} supply centers and wins!")
            return True

    # If we've used too many tokens, exit gracefully
    if total_tokens >= max_tokens:
        print(f"Max token usage {max_tokens} exceeded, ending game.")
        # decide the winner based on the number of centers
        max_centers = 0
        winner = None
        for power_name, power in game.powers.items():
            if len(power.centers) > max_centers:
                max_centers = len(power.centers)
                winner = power_name
        print(f"Winner: {winner}")
        return True

    # If we've reached the max number of years, end the game
    if int(game.phase.split(" ")[1]) >= max_years:
        print(f"Max years {max_years} reached, ending game.")
        max_centers = 0
        winner = None
        for power_name, power in game.powers.items():
            if len(power.centers) > max_centers:
                max_centers = len(power.centers)
                winner = power_name
        print(f"Winner: {winner}")
        return True
    return False

def play_diplomacy_game(
    num_agents: int=7,
    winning_centers: int=18,
    max_tokens: int=1000000,
    max_years: int=1916,
    model_names: list=None,
    temperature: float=0.8,
    top_p: float=1.0,
    state_file: str="diplomacy_game_state.json",
    message_file: str="diplomacy_game_message.json",
    enable_negotiation: int=1,
    negotiation_rounds: int=3,
    store_folder: str=None,
    ):
    """
    Main function to run a Diplomacy game with the given settings.

    Args:
    num_agents: Number of players in the game.
    winning_centers: Number of centers needed to claim victory.
    max_tokens: If the total token usage exceeds this, end the game.
    model_names: A list of strings denoting which model each agent uses.
    temperature: OpenAI temperature.
    top_p: OpenAI top_p.
    state_file: Path to the JSON file to store and resume game states.
    negotiation_rounds: Number of negotiation rounds per move phase.
    """
    # Basic validation
    if model_names is None:
        # Default every agent to the same model if not provided
        model_names = ["bot"] * num_agents
    elif len(model_names) < num_agents:
        raise ValueError("Not enough model names provided for each agent.")
    
    index_model = {i: model_names[i] for i in range(num_agents)}
    model_index = {name: i for i, name in index_model.items()}

    # For simplicity, let's assume the default power names are 7:
    power_list = [
        "AUSTRIA",
        "ENGLAND",
        "FRANCE",
        "GERMANY",
        "ITALY",
        "RUSSIA",
        "TURKEY"
    ]
    neutral_powers = []
    for i in range(len(model_names)):
        if model_names[i] == "bot":
            neutral_powers.append(power_list[i])

    # Map indices to powers and vice versa
    index_power_name = {i: power_list[i] for i in range(num_agents)}
    power_name_index = {name: i for i, name in index_power_name.items()}
    # generate model_power_dict
    model_name_set = set(model_names)
    model_power_dict = {
        model_name: {
            "model": model_name.split("_")[0], # gpt-4o_1 -> gpt-4o
            "power_names": [],
            "power_name_to_location_orders": {},
            "messages": [],
            "store_messages": [],
        } for model_name in model_name_set if model_name != "bot"
    }
    # init messages
    for model_name in model_power_dict.keys():
        model_power_dict[model_name]["messages"].append({
            "role": "user",
            "content": gen_init_prompt_bundle(neutral_powers, model_power_dict[model_name]["power_names"], power_list)
        })
        model_power_dict[model_name]["store_messages"].append({
            "role": "user",
            "content": gen_init_prompt_bundle(neutral_powers, model_power_dict[model_name]["power_names"], power_list)
        })
        model_power_dict[model_name]["messages"].append({
            "role": "assistant",
            "content": "Sure, let's start."
        })
        model_power_dict[model_name]["store_messages"].append({
            "role": "assistant",
            "content": "Sure, let's start."
        })
    # Initialize or load from state_file
    if os.path.exists(store_folder + "/" + state_file):
        state = json.load(open(store_folder + "/" + state_file, "r"))
        game = load_saved_games_from_disk(state["game_path"])[-1]
        past_model_power_dict = state["model_power_dict"]
        total_tokens = state["total_tokens"]
        try:
            input_tokens = state["input_tokens"]
            output_tokens = state["output_tokens"]
            cached_tokens = state["cached_tokens"]
        except KeyError:
            input_tokens = 0
            output_tokens = 0
            cached_tokens = 0
        for model_name in model_power_dict.keys():
            model_power_dict[model_name]["store_messages"] = past_model_power_dict[model_name]["store_messages"]
        print("Resuming from existing game:", game.get_current_phase())
    else:
        game = Game()
        total_tokens = 0
        input_tokens = 0
        output_tokens = 0
        cached_tokens = 0

    # init power
    for power_name, power in game.powers.items():
        if model_names[power_name_index[power_name]] == "bot":
            continue
        model_power_dict[model_names[power_name_index[power_name]]]["power_names"].append(power_name)
    
    

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
    )

    # Helper function to call the chat model
    def call_chat_model(role_messages, model):
        nonlocal total_tokens, input_tokens, output_tokens, cached_tokens
        try:
            # You can also pass temperature, top_p here if needed
            if "o1" not in model and "gpt" in model:
                chat_completion = client.chat.completions.create(
                    messages=role_messages,
                    model=model,
                    temperature=temperature,
                    top_p=top_p
                )
                total_tokens += chat_completion.usage.to_dict().get("total_tokens", 0)
                print("total tokens used in this call: ", chat_completion.usage.to_dict().get("total_tokens", 0))
                input_tokens += chat_completion.usage.to_dict().get("prompt_tokens", 0)
                print("input tokens used in this call: ", chat_completion.usage.to_dict().get("prompt_tokens", 0))
                output_tokens += chat_completion.usage.to_dict().get("completion_tokens", 0)
                print("output tokens used in this call: ", chat_completion.usage.to_dict().get("completion_tokens", 0))
                cached_tokens += chat_completion.usage.to_dict().get("completion_tokens_details", {}).get("cached_tokens", 0)
                content = chat_completion.choices[0].message.content
            elif "o1" in model:
                chat_completion = client.chat.completions.create(
                    messages=role_messages,
                    model=model,
                )
                total_tokens += chat_completion.usage.to_dict().get("total_tokens", 0)
                print("total tokens used in this call: ", chat_completion.usage.to_dict().get("total_tokens", 0))
                input_tokens += chat_completion.usage.to_dict().get("prompt_tokens", 0)
                print("input tokens used in this call: ", chat_completion.usage.to_dict().get("prompt_tokens", 0))
                output_tokens += chat_completion.usage.to_dict().get("completion_tokens", 0)
                print("output tokens used in this call: ", chat_completion.usage.to_dict().get("completion_tokens", 0))
                cached_tokens += chat_completion.usage.to_dict().get("completion_tokens_details", {}).get("cached_tokens", 0)
                content = chat_completion.choices[0].message.content
            elif "o3" in model:
                chat_completion = client.chat.completions.create(
                    messages=role_messages,
                    model=model,
                )
                total_tokens += chat_completion.usage.to_dict().get("total_tokens", 0)
                input_tokens += chat_completion.usage.to_dict().get("prompt_tokens", 0)
                output_tokens += chat_completion.usage.to_dict().get("completion_tokens", 0)
                cached_tokens += chat_completion.usage.to_dict().get("completion_tokens_details", {}).get("cached_tokens", 0)
                content = chat_completion.choices[0].message.content
            elif "claude" in model:
                message = anthropic_client.messages.create(
                    messages=role_messages,
                    model=model,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=8000,
                )
                total_tokens += message.usage.input_tokens + message.usage.output_tokens
                print("total tokens used in this call: ", message.usage.input_tokens + message.usage.output_tokens)
                input_tokens += message.usage.input_tokens
                print("input tokens used in this call: ", message.usage.input_tokens)
                output_tokens += message.usage.output_tokens
                print("output tokens used in this call: ", message.usage.output_tokens)
                content = message.content[0].text
            elif "deepseek" in model:
                response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json={
                    'model': 'deepseek/deepseek-r1',
                    'messages': role_messages,
                    'provider': {
                        'order': [
                            'Minimax'
                        ],
                        'allow_fallbacks': False
                        }
                }).json()
                total_tokens += response["usage"].get("total_tokens", 0)
                print("total tokens used in this call: ", response["usage"].get("total_tokens", 0))
                input_tokens += response["usage"].get("prompt_tokens", 0)
                print("input tokens used in this call: ", response["usage"].get("prompt_tokens", 0))
                output_tokens += response["usage"].get("completion_tokens", 0)
                print("output tokens used in this call: ", response["usage"].get("completion_tokens", 0))
                cached_tokens += response["usage"].get("completion_tokens_details", {}).get("cached_tokens", 0)
                content = response["choices"][0]["message"]["content"]
                print("deepseek content: ", content)
            return content
        except Exception as e:
            print("Error calling chat model:", e)
            return ""

    # Prepare dictionary to store messages and orders as well
    store_messages = {}
    store_orders = {}

    # The main game loop
    while not game.is_game_done:
        current_phase = game.get_current_phase()
        current_state = game.get_state()

        # Check if the game should end
        if end_game_check(game, winning_centers, max_tokens, max_years, total_tokens):
            break

        # update the model_power_dict
        possible_orders_dict = game.get_all_possible_orders()
        for power_name, power in game.powers.items():
            if model_names[power_name_index[power_name]] == "bot":
                continue
            orderable_locations = game.get_orderable_locations(power_name)
            location_orders = {loc: possible_orders_dict[loc] for loc in orderable_locations if loc in possible_orders_dict}
            model_power_dict[model_names[power_name_index[power_name]]]["power_name_to_location_orders"][power_name] = location_orders

        # truncate
        for model_name in model_power_dict.keys():
            model_power_dict[model_name]["messages"] = model_power_dict[model_name]["messages"][:2]

        # add the phase history
        # phase_history = game.get_phase_history()
        # for idx in range(len(phase_history)):
        #     phase_history[idx] = phase_history[idx].to_dict()
        # for power_name, power in game.powers.items():
        #     append_user_message(index_messages[power_name_index[power_name]], index_store_messages[power_name_index[power_name]], generate_phase_history_prompt(phase_history, power_name))

        # Prepare possible orders
        possible_orders_dict = game.get_all_possible_orders()
        print("total tokens: ", total_tokens)
        print("input tokens: ", input_tokens)
        print("output tokens: ", output_tokens)
        print("cached tokens: ", cached_tokens)
        print("*"*50)
        print("current state: ", game.get_state())
        print("now phase: ", game.get_current_phase())
        phase_type = game.phase_type

        if phase_type == "A":
            print("adjustment phase")
            # Winter phase
            # iterate through each model
            for model_name in model_power_dict.keys():
                print("model_name: ", model_name)
                print("controlling powers: ", model_power_dict[model_name]["power_names"])
                prompt = gen_winter_action_prompt_bundle(model_power_dict[model_name]["power_names"], current_state, str(model_power_dict[model_name]["power_name_to_location_orders"]), neutral_powers)
                append_user_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], prompt)
                print("prompt: ", prompt)
                while True:
                    try:
                        content_reply = call_chat_model(model_power_dict[model_name]["messages"], model_power_dict[model_name]["model"])
                        append_assistant_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], content_reply)
                        print(content_reply)
                        response_re_match = re.search(JSON_PATTERN, content_reply)
                        respond_obj = json.loads(response_re_match.group())
                        power_orders = respond_obj["orders"]
                        for k in power_orders.keys():
                            game.set_orders(k, power_orders[k])
                        break
                    except Exception as e:
                        print(f"Error parsing JSON from {model_name}'s order response: {e}")
                        if model_power_dict[model_name]["messages"][-1]["role"] == "assistant":
                            model_power_dict[model_name]["messages"].pop()
                            model_power_dict[model_name]["store_messages"].pop()
                        continue
                print("power_orders: ", power_orders)
                # Store
                store_orders[f"{current_phase}-{model_name}"] = power_orders
            # iterate through all the bot
            for power_name, power in game.powers.items():
                if model_names[power_name_index[power_name]] == "bot":
                    # bot
                    print("bot: ", power_name)
                    orderable_locations = game.get_orderable_locations(power_name)
                    location_orders = {loc: possible_orders_dict[loc] for loc in orderable_locations if loc in possible_orders_dict}
                    if not location_orders:
                        print("No adjustment order available for", power_name)
                        continue
                    current_centers = len(power.centers)
                    required_centers = current_centers  # They maintain their current number of units
                    current_units = len(power.units)
                    if current_units > required_centers:
                        print("need to disband for neutral bot")
                    power_orders = [location_orders[loc][0] for loc in location_orders]
                    print("power_orders: ", power_orders)
                    store_orders[f"{current_phase}-{power_name}"] = power_orders
                    game.set_orders(power_name, power_orders)
                else:
                    continue
        elif phase_type == "R":
            print("retreat phase")
            # iterate through each model
            for model_name in model_power_dict.keys():
                print("model_name: ", model_name)
                print("controlling powers: ", model_power_dict[model_name]["power_names"])
                prompt = gen_retreat_action_prompt_bundle(model_power_dict[model_name]["power_names"], current_state, str(model_power_dict[model_name]["power_name_to_location_orders"]), neutral_powers)
                append_user_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], prompt)
                print("prompt: ", prompt)
                while True:
                    try:
                        content_reply = call_chat_model(model_power_dict[model_name]["messages"], model_power_dict[model_name]["model"])
                        append_assistant_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], content_reply)
                        print(content_reply)
                        response_re_match = re.search(JSON_PATTERN, content_reply)
                        respond_obj = json.loads(response_re_match.group())
                        power_orders = respond_obj["orders"]
                        for k in power_orders.keys():
                            game.set_orders(k, power_orders[k])
                        break
                    except Exception as e:
                        print(f"Error parsing JSON from {model_name}'s order response: {e}")
                        if model_power_dict[model_name]["messages"][-1]["role"] == "assistant":
                            model_power_dict[model_name]["messages"].pop()
                            model_power_dict[model_name]["store_messages"].pop()
                        continue
                print("power_orders: ", power_orders)
                # Store
                store_orders[f"{current_phase}-{model_name}"] = power_orders

            # iterate through all the bot
            for power_name, power in game.powers.items():
                if model_names[power_name_index[power_name]] == "bot":
                    # bot
                    print("bot: ", power_name)
                    orderable_locations = game.get_orderable_locations(power_name)
                    location_orders = {loc: possible_orders_dict[loc] for loc in orderable_locations if loc in possible_orders_dict}
                    if not location_orders:
                        print("No retreat order available for", power_name)
                        continue
                    power_orders = [location_orders[loc][0] for loc in location_orders]
                    print("power_orders: ", power_orders)
                    store_orders[f"{current_phase}-{power_name}"] = power_orders
                    game.set_orders(power_name, power_orders)
                else:
                    continue
        elif phase_type == "M":
            print("move phase")
            if enable_negotiation == 1:
                last_negotiation_round_time = None
                for round_i in range(negotiation_rounds):
                    print("#"*50)
                    print("negotiation round: ", round_i)
                    negotiation_round_start_time = common.timestamp_microseconds()
                    # iterate through each model
                    for model_name in model_power_dict.keys():
                        print("model_name: ", model_name)
                        print("controlling powers: ", model_power_dict[model_name]["power_names"])
                        if round_i == 0:
                            prompt = gen_round_prompt(
                                power_name=model_power_dict[model_name]["power_names"][0], # deprecated
                                state=current_state,
                                possible_orders=str(model_power_dict[model_name]["power_name_to_location_orders"]),
                                phase=current_phase,
                                result=str(game.result),
                                negotiation_rounds=negotiation_rounds,
                                neutral_powers=neutral_powers,
                            )
                            prompt += gen_negotiation_prompt_bundle(round_i, negotiation_rounds, model_power_dict[model_name]["power_names"], power_list, None, neutral_powers, False)
                        else:
                            # Summarize last round's messages
                            last_msgs = get_message_text_bundle(
                                game.messages,
                                recipients=model_power_dict[model_name]["power_names"],
                                time_start=last_negotiation_round_time or 0,
                                time_end=negotiation_round_start_time
                            )
                            prompt = gen_negotiation_prompt_bundle(round_i, negotiation_rounds, model_power_dict[model_name]["power_names"], power_list, last_msgs, neutral_powers, False)
                        prompt += f"""\nEnsure that in your JSON output, the value assigned to the "messages" key must strictly be options listed in {model_power_dict[model_name]['power_names']}.\n"""
                        append_user_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], prompt)
                        print("prompt: ", prompt)
                        while True:
                            try:
                                content_reply = call_chat_model(model_power_dict[model_name]["messages"], model_power_dict[model_name]["model"])
                                respond_obj = json.loads(re.search(JSON_PATTERN, content_reply).group())
                                messages = respond_obj["messages"]
                                append_assistant_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], content_reply)
                                print(content_reply)
                                for k in messages.keys():
                                    if k not in model_power_dict[model_name]["power_names"]:
                                        print("sending message with wrong power name")
                                        raise Exception("sending message with wrong power name")
                                break
                            except Exception as e:
                                print(f"Error parsing JSON from {model_name}'s negotiation message: {e}")
                                if model_power_dict[model_name]["messages"][-1]["role"] == "assistant":
                                    model_power_dict[model_name]["messages"].pop()
                                    model_power_dict[model_name]["store_messages"].pop()
                                continue
                        store_messages[f"{current_phase}-{model_name}-R{round_i}"] = {
                            "messages": messages
                        }
                        for power_name in messages.keys():
                            recipients = messages[power_name]["recipients"]
                            messages_list = messages[power_name]["messages"]
                            for rcpt, msg in zip(recipients, messages_list):
                                game.add_message(Message(sender=power_name, recipient=rcpt, message=msg, phase=current_phase))
                    last_negotiation_round_time = negotiation_round_start_time
                # "End" negotiation message
                current_time = common.timestamp_microseconds()
                for model_name in model_power_dict.keys():
                    print("model_name: ", model_name)
                    print("controlling powers: ", model_power_dict[model_name]["power_names"])
                    last_msgs = get_message_text_bundle(
                        game.messages,
                        recipients=model_power_dict[model_name]["power_names"],
                        time_start=last_negotiation_round_time or 0,
                        time_end=current_time
                    )
                    prompt = gen_negotiation_prompt_bundle(negotiation_rounds, negotiation_rounds, model_power_dict[model_name]["power_names"], power_list, last_msgs, neutral_powers, True)
                    append_user_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], prompt)
                    print("prompt: ", prompt)
                    while True:
                        try:
                            content_reply = call_chat_model(model_power_dict[model_name]["messages"], model_power_dict[model_name]["model"])
                            append_assistant_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], content_reply)
                            print(content_reply)
                            break
                        except Exception as e:
                            print(f"Error parsing JSON from {model_name}'s negotiation message: {e}")
                            if model_power_dict[model_name]["messages"][-1]["role"] == "assistant":
                                model_power_dict[model_name]["messages"].pop()
                                model_power_dict[model_name]["store_messages"].pop()
                            continue
                    store_messages[f"{current_phase}-{model_name}-R{negotiation_rounds}-end"] = content_reply
            print("#"*50)
            print("negotiation phase done")
            print("start action phase")
            # iterate through each model
            for model_name in model_power_dict.keys():
                print("model_name: ", model_name)
                print("controlling powers: ", model_power_dict[model_name]["power_names"])
                adj_list = []
                loc_list = []
                for k in model_power_dict[model_name]["power_name_to_location_orders"].keys():
                    loc_list.extend(list(model_power_dict[model_name]["power_name_to_location_orders"][k].keys()))
                for loc in loc_list:
                    try:
                        adj_list.append({loc: game.map.loc_abut[loc]})
                    except Exception as e:
                        print(f"Error getting adjacencies: {e}")
                if len(adj_list) == 0:
                    adj_information = None
                else:
                    adj_information = str(adj_list)
                # adj_information = None
                prompt = gen_action_prompt_bundle(
                    power_names=model_power_dict[model_name]["power_names"], state=current_state, 
                    possible_orders=str(model_power_dict[model_name]["power_name_to_location_orders"]), 
                    adj_information=adj_information, 
                    neutral_powers=neutral_powers)
                prompt += f"""Ensure that in your JSON output, the value assigned to the "orders" is a dictionary, and that dictionary's keys must strictly be options listed in {model_power_dict[model_name]['power_names']}."""
                append_user_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], prompt)
                print("prompt: ", prompt)
                while True:
                    try:
                        content_reply = call_chat_model(model_power_dict[model_name]["messages"], model_power_dict[model_name]["model"])
                        append_assistant_message(model_power_dict[model_name]["messages"], model_power_dict[model_name]["store_messages"], content_reply)
                        print(content_reply)
                        response_re_match = re.search(JSON_PATTERN, content_reply)
                        respond_obj = json.loads(response_re_match.group())
                        power_orders = respond_obj["orders"]
                        for k in power_orders.keys():
                            if k not in model_power_dict[model_name]["power_names"]:
                                print("sending order with wrong power name")
                                raise Exception("sending order with wrong power name")
                        for k in power_orders.keys():
                            game.set_orders(k, power_orders[k])
                        break
                    except Exception as e:
                        print(f"Error parsing JSON from {model_name}'s order response: {e}")
                        if model_power_dict[model_name]["messages"][-1]["role"] == "assistant":
                            model_power_dict[model_name]["messages"].pop()
                            model_power_dict[model_name]["store_messages"].pop()
                        continue
                print("power_orders: ", power_orders)
                # Store
                store_orders[f"{current_phase}-{model_name}"] = power_orders
            
        # Process
        print("Processing orders...")
        game.process()

        # compute model supply center
        for model_name in model_power_dict.keys():
            model_power_dict[model_name]["supply_center_count"] = 0
            for power_name in model_power_dict[model_name]["power_names"]:
                model_power_dict[model_name]["supply_center_count"] += len(game.powers[power_name].centers)
        print("supply center count: ", {model_name: model_power_dict[model_name]["supply_center_count"] for model_name in model_power_dict.keys()})

        # Save the game state
        print("Saving game state...")
        game.render(True, True, output_format="svg", output_path=f"{store_folder}/maps/{game.get_current_phase()}.svg")
        outcome = None
        game_save_path = f"{store_folder}/diplomacy_game_save.json"
        to_saved_game_format(game, output_path=game_save_path)
        data_to_save = {
            "game_path": game_save_path, # Save the path to the game state
            "total_tokens": total_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cached_tokens": cached_tokens,
            "outcome": outcome,
            "model_power_dict": {
                model_name: {
                    "model": model_power_dict[model_name]["model"],
                    "power_names": model_power_dict[model_name]["power_names"],
                    "supply_center_count": model_power_dict[model_name]["supply_center_count"],
                    "store_messages": model_power_dict[model_name]["store_messages"],
                } for model_name in model_power_dict.keys()
            },
            "index_model": index_model,
            "index_power_name": index_power_name,
            "store_messages": store_messages,
            "store_orders": store_orders
        }
        with open(store_folder + "/" + state_file, "w") as f:
            json.dump(data_to_save, f, indent=2)
        if any([model_power_dict[model_name]["supply_center_count"] >= winning_centers for model_name in model_power_dict.keys()]):
            break

    # End of game
    outcome = game.outcome
    print("Game finished. Outcome:", outcome)
    print("Total tokens used:", total_tokens)
    if outcome is None:
        print("No outcome was set, possibly ended early or by max_tokens.")
    else:
        print("Winner(s):", outcome)
    
def main():
    parser = argparse.ArgumentParser(description="Run a configurable Diplomacy game with LLM-based agents.")
    parser.add_argument("--num_agents", type=int, default=7, help="Number of players in the game.")
    parser.add_argument("--winning_centers", type=int, default=18, help="Number of supply centers required to win.")
    parser.add_argument("--max_tokens", type=int, default=10000000, help="Max total token usage before ending.")
    parser.add_argument("--max_years", type=int, default=1916, help="Max number of years to run the game.")
    parser.add_argument("--model_names", type=str, default="",
    help="Comma-separated model names, e.g. 'gpt-4,gpt-4,gpt-4'")
    parser.add_argument("--temperature", type=float, default=1.0, help="OpenAI temperature parameter.")
    parser.add_argument("--top_p", type=float, default=1.0, help="OpenAI top_p parameter.")
    parser.add_argument("--state_file", type=str, default="diplomacy_game_state.json",
    help="File to store and resume game state.")
    parser.add_argument("--enable_negotiation", type=int, default=1, help="Enable negotiation phase.")
    parser.add_argument("--negotiation_rounds", type=int, default=3,
    help="Number of negotiation rounds per move phase.")
    parser.add_argument("--store_folder", type=str, default=None, help="Folder to store game state.")
    args = parser.parse_args()
    print(args)
    

    # If user supplied model names
    models = []
    if args.model_names:
        models = [m.strip() for m in args.model_names.split(",")]

    if args.store_folder is None:
        store_folder = time.strftime("%Y%m%d-%H%M%S")
        save_folder = f"diplomacy_saves/" + store_folder
        os.makedirs(save_folder, exist_ok=True)
        os.makedirs(f"{save_folder}/maps", exist_ok=True)
        # save args as config
        with open(f"{save_folder}/config.json", "w") as f:
            json.dump(vars(args), f, indent=2)
        output_file = open(save_folder+"/output.log", "w")
        print("output log: ", output_file)
        sys.stdout = output_file
        print(f"Using save folder: {save_folder}", flush=True)
    else:
        save_folder = f"diplomacy_saves/" + args.store_folder
        os.makedirs(save_folder, exist_ok=True)
        os.makedirs(f"{save_folder}/maps", exist_ok=True)
        # save args as config
        with open(f"{save_folder}/config.json", "w") as f:
            json.dump(vars(args), f, indent=2)
        output_file = open(save_folder+"/output.log", "a")
        print("output log: ", output_file)
        sys.stdout = output_file
        print("Resuming from existing save folder.")
        print(f"Using save folder: {save_folder}", flush=True)

    try:
        play_diplomacy_game(
            num_agents=args.num_agents,
            winning_centers=args.winning_centers,
            max_tokens=args.max_tokens,
            max_years=args.max_years,
            model_names=models if models else None,
            temperature=args.temperature,
            top_p=args.top_p,
            state_file=args.state_file,
            enable_negotiation=args.enable_negotiation,
            negotiation_rounds=args.negotiation_rounds,
            store_folder=save_folder
        )
        output_file.close()
    except Exception as e:
        print("Error during game:", e)
        traceback.print_exc()
    finally:
        output_file.close()
    

if __name__ == "__main__":
    main()