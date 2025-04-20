import json
import sys
import copy
import pyspiel
import os
import json
import regex
from tools.chat_service import get_chat
from utils.play_service import (
	play,
	create_hook_functions,
)
# Regex pattern for recursive matching
json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
import numpy as np
from tasks.hanabi.parse_hanabi import parse_game_state


def gen_initial_prompt():
	return """
You are a master of hanabi game. You are playing a game of Hanabi. Hanabi is a cooperative card game where players work together to create a series of fireworks by playing cards in ascending numerical order starting from 1. Each player holds their cards facing outward so that all players can see everyone else's cards but not their own. The objective is to play cards in sequence (1 through 5) for each color without making mistakes. There are 5 different colors and each color has cards numbered 1 to 5.

Key Rules:

On your turn, you have three types of possible actions:

Give a Hint(Reveal): Provide a hint to another player about their cards, specifying either a color or a number present in their hand. Hints must be accurate and can only reveal positions of cards matching the hint.
Discard a Card: Discard one of your own cards to potentially gain an Info token.
Play a Card: Attempt to play a card from your hand. If played correctly in sequence, it adds to the fireworks; if not, it reduces one life token.

Tokens:
Life Tokens: Deducted when a wrong card is played.
Info Tokens: Used to give clues.
Illegal Moves: Playing a card that cannot be placed properly costs a life token. If life tokens reach zero, the game ends in failure.
Game End: The game ends when all fireworks are completed (perfect score of 25), or when the deck is exhausted and each player has taken one final turn, or when the players run out of life tokens.

State Representation: The game state is represented with the following details:

Life tokens: Number of remaining life tokens.
Info tokens: Number of available information tokens.
Fireworks: Current progress on each firework color (e.g., R1, Y0, G1, W0, B0).
Discards: Cards that have been discarded.

Your Role:

You are one of the players, cooperating with others to maximize the total score of the fireworks (the number of cards correctly played in sequence).
Although you cannot see your own cards, you can see the cards in the hands of your teammates.
Use hints, discards, and plays strategically to guide the team towards successful sequences.

Remember, communication is limited to hints about colors or numbers only, and sharing illegal or extraneous information is not allowed. Work together, follow the rules, and aim for the highest cooperative score possible!
"""

def generate_state_description(observation):
	player_number = len(observation.split("-----"))
	observation = parse_game_state(observation)
	return f"""
Below is the current detailed state information. There are {player_number} players in the game.

Game State:
{observation}

"""

def generate_action_prompt(legal_moves_dict):
	return f"""

Please think step by step based on the current state
	
# Think step by step

## Evaluate Playable Cards in Hand

Look at each card in your hand.
Cross-reference with the current game state to see if any card can be immediately played to complete or extend a firework stack.
Consider hints you have received about each card (color/rank information) to determine if it might be safe to play.
If a card can be played without risk, prioritize playing it to score a point.

## Consider Teammates' Hands and Hint Opportunities

Analyze the visible cards in your teammates' hands.
Identify if any of their cards can now be played based on the current firework stacks or previous hints.
If you notice a teammate holds a card that can be played but they may not realize it, think about what hints you could give them.
Use hints to communicate critical information, such as color or rank, to help them make the right play.
Choose the hint that maximizes the chance for a correct play while considering the limited hint tokens.

## Assess Discard Options to Gain Info Tokens

Look for cards in your hand that are least likely to be playable or helpful in the near future.
Consider the remaining deck composition and cards already played/discarded to predict the value of each card.
Discard a card that you believe to be least useful to gain an Info token, especially if no immediate playable or hint options are available.
Ensure that discarding this card won't permanently remove a critical card needed to complete any firework stack.

Now it's your turn. You can choose from the following legal actions:

The legal actions are provided in a mapping of action identifiers to their descriptions:
{legal_moves_dict}

(Reveal player +N color C): Give a hint about color C to the player who is N positions ahead of you.
(Reveal player +N rank R): Give a hint about rank R to the player who is N positions ahead.
(Play X): Play the card in position X from your hand.
(Discard X): Discard the card in position X from your hand.

Based on the annotated state and the list of legal actions, decide on the most appropriate move to make. Consider factors like current tokens, firework progress, and information available in hands. Then, output one of the legal action descriptions as your chosen action.

Your output should be in this format: 
{{"reason": string, "action": int}} And the action should be one of the legal actions provided above.
You can only use json valid characters. When you write json, all the elements (including all the keys and values) should be enclosed in double quotes!!!

To win, you need to play the cards in the correct sequence and maximize the total score of the fireworks. Good luck!
"""

def gen_move(player_messages, player_model):
	content, used_token = get_chat(player_model, player_messages)
	try:
		parsed_json = None
		matches = json_pattern.findall(content)
		for match in matches:
			try:
				parsed_json = json.loads(match)
				print("Valid JSON Found:", parsed_json)
			except Exception as e:
				print("Invalid JSON Found:", match)
				parsed_json = json.loads(match)
		action = int(parsed_json["action"])
		reason = parsed_json["reason"]
		move = action
	except Exception as e:
		print(e)
		move = None
		action = None
		reason = None
	return move, content, used_token, action, reason

def parse_legal_actions(state, legal_actions):
	legal_moves_dict = {}
	for action in legal_actions:
		legal_moves_dict[action] = state.action_to_string(action)
	return legal_moves_dict

config = json.load(open("../../config/hanabi-config.json","r")) # list

for idx in range(5):
	filename = config["filename"]+str(idx)+".json"
	if os.path.exists(filename):
		print("File exists, skipping", filename)
		continue

	log_file = config["log_file"]+str(idx)+".log"
	# output stream to log_file
	if log_file:
		sys.stdout = open(log_file, "w")
	hand_size = config["hand_size"]
	player_models = config["player_models"]
	player_num = len(player_models)
	print(player_num, "players")

	index_model = {
		i: player_models[i] for i in range(player_num)
	}
	index_messages = {
		i: [
			{
				"role": "user",
				"content": gen_initial_prompt()
			}
		] for i in range(player_num)
	}

	for i in range(len(player_models)):
		if player_models[i]["model"] == "human":
			continue
		content, used_token = get_chat(player_models[i]["model"], index_messages[i])
		index_messages[i].append({
			"role": "assistant",
			"content": content,
		})

	index_store_messages = copy.deepcopy(index_messages)

	game_log = []
	game = pyspiel.load_game("hanabi", {"players": len(player_models),"hand_size": hand_size})
	state = game.new_initial_state()
	cnt = 0
	print(state)
	while not state.is_terminal():
		cnt += 1
		print("*"*30)
		print("cnt: ", cnt)
		print("current returns: ", state.returns())
		legal_actions = state.legal_actions()
		if state.is_chance_node():
			# Sample a chance event outcome.
			print("Chance Node")
			outcomes_with_probs = state.chance_outcomes()
			action_list, prob_list = zip(*outcomes_with_probs)
			action = np.random.choice(action_list, p=prob_list)
			# game_log.append((int(action), state.returns()))
			state.apply_action(action)
		else:
			player_index = state.current_player()
			print("State: ", state)
			print("Current Player: ", player_index)
			player_observation = state.observation_string(player_index)
			print(parse_game_state(player_observation))
			print(parse_legal_actions(state, legal_actions))


			# action = int(input("Enter action: "))
			index_messages[player_index] = index_messages[player_index][:2]
			hook_functions = create_hook_functions(player_models[player_index], None, generate_state_description(player_observation), generate_action_prompt(parse_legal_actions(state, legal_actions)))
			move, action, win, game_state, added_tokens = play(index_messages[player_index], index_store_messages[player_index], player_models[player_index]["model"], [], None, None, legal_actions, gen_move, 5, True, hook_functions, player_index)
			game_log.append((int(action), state.returns()))
			state.apply_action(action)

	returns = state.returns()
	print("Returns: ", returns)
	json.dump({
		"config": config,
		"cnt": cnt,
		"returns": returns,
		"game_log": game_log,
		"index_store_messages": index_store_messages,
	}, open(filename, "w"), indent=2, ensure_ascii=False)

	if log_file:
		sys.stdout.close()
		sys.stdout = sys.__stdout__