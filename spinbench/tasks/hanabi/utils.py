from spinbench.tools.chat_service import get_chat
import regex
import json

json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}', regex.DOTALL)
def parse_game_state(state_str):
    # Split the state string into lines for processing
    lines = state_str.strip().splitlines()
    
    # Initialize variables to store parsed details
    life_tokens = None
    info_tokens = None
    fireworks = {}
    your_hand = []
    other_players_hands = []  # List to hold each other player's hand as a list of cards
    current_other_hand = []   # Temporary list to accumulate cards for the current player's hand
    deck_size = None
    discards = None

    # Parsing state flags
    parsing_your_hand = False
    parsing_other_hands = False

    # Loop over lines to extract information
    for line in lines:
        line = line.strip()
        if line.startswith("Life tokens:"):
            life_tokens = line.split(":")[1].strip()
        elif line.startswith("Info tokens:"):
            info_tokens = line.split(":")[1].strip()
        elif line.startswith("Fireworks:"):
            _, fw_data = line.split("Fireworks:")
            for part in fw_data.split():
                color = part[0]
                number = part[1:]
                fireworks[color] = number
        elif line.startswith("Cur player"):
            parsing_your_hand = True
            parsing_other_hands = False
        elif line.startswith("Hands:"):
            # Skip the header
            continue
        elif line.startswith("Deck size:"):
            deck_size = line.split(":")[1].strip()
        elif line.startswith("Discards:"):
            discards = line.split("Discards:")[1].strip() if ":" in line else ""
        elif line == "-----":
            # Separator found: switching context between hands
            if parsing_your_hand:
                # End of your hand, start parsing other players' hands
                parsing_your_hand = False
                parsing_other_hands = True
            else:
                # End of current player's hand, store it and start a new one
                if current_other_hand:
                    other_players_hands.append(current_other_hand)
                current_other_hand = []
        else:
            # Process line based on current parsing context
            if parsing_your_hand:
                your_hand.append(line)
            elif parsing_other_hands:
                # Lines under other players' hands until next separator
                current_other_hand.append(line)

    # After loop ends, if there's an unfinished other hand, add it
    if current_other_hand:
        other_players_hands.append(current_other_hand)

    description = []

    # Life and info tokens description
    description.append(f"There are {life_tokens} life tokens and {info_tokens} info tokens remaining.")

    # Fireworks progress description
    fireworks_desc = ", ".join([f"{color} stack is at {number}" for color, number in fireworks.items()])
    description.append(f"The fireworks progress: {fireworks_desc}.")

    # Detailed explanation of your hand
    description.append("\nYour hand contains the following cards:")
    for idx, card_line in enumerate(your_hand, start=1):
        try:
            hidden, rest = card_line.split("||")
            known, possibilities = rest.split("|")
        except ValueError:
            continue
        
        hidden = hidden.strip()
        known = known.strip()
        possibilities = possibilities.strip()

        card_desc = f"Card {idx}:\n"
        # Hidden info explanation
        card_desc += f"  - Hidden info: '{hidden}'. This represents what you cannot see about this card. "
        if hidden == "XX":
            card_desc += "It means you have no direct knowledge about the card's identity from your perspective.\n"
        else:
            card_desc += "There are some hints or partial information, but the full identity of this card is not completely known to you.\n"

        # Known info explanation
        card_desc += f"  - Known info: '{known}'. "
        if known == "XX":
            card_desc += "No hints about this card's color or rank have been given yet.\n"
        else:
            details = []
            # Interpret each possible hint character
            colors = {"R": "red", "Y": "yellow", "G": "green", "W": "white", "B": "blue"}
            for char in known:
                if char in colors:
                    details.append(f"{colors[char]} color")
                elif char.isdigit():
                    details.append(f"rank {char}")
            if details:
                card_desc += "Hints suggest that the card might be: " + ", ".join(details) + ".\n"
            else:
                card_desc += "No specific hints have been provided yet.\n"

        # Possible identities explanation
        card_desc += f"  - Possible identities: '{possibilities}'. "
        card_desc += ("This list represents the set of all cards that could possibly be in this position, given "
                      "the hints received and the remaining cards in the deck.\n")
        description.append(card_desc)

    # Explanation for other players' hands from your perspective
    description.append("\nFrom your perspective, you can see the other players' hands clearly. Here's what you observe:")

    for player_idx, hand in enumerate(other_players_hands, start=1):
        description.append(f"\nPlayer +{player_idx}'s hand:")

        for card_line in hand:
            # Each line might represent a card from another player's hand
            try:
                known, rest = card_line.split("||")
                hidden, possibilities = rest.split("|")
            except ValueError:
                continue

            known = known.strip()
            hidden = hidden.strip()
            details = []
            colors = {"R": "red", "Y": "yellow", "G": "green", "W": "white", "B": "blue"}
            for char in hidden:
                if char in colors:
                    details.append(f"{colors[char]} color")
                elif char.isdigit():
                    details.append(f"rank {char}")
            if details:
                hidden = "This player knows the card might be: " + ", ".join(details)
            else:
                hidden = "This player has no specific hints about the card's identity"

            possibilities = "This player knows the card could be one of the following: " + possibilities + "."
            
            possibilities = possibilities.strip()
            description.append(f" - A card: You can see the card: '{known}', {hidden}, {possibilities}")
    


    # Deck and discards description
    description.append(f"\nThere are {deck_size} cards remaining in the deck.")
    if discards:
        description.append(f"Discard pile: {discards}.")
    else:
        description.append("The discard pile is currently empty.")

    return "\n".join(description)

    # # Example usage:
    # state_string = """Game State:
    # Life tokens: 3
    # Info tokens: 7
    # Fireworks: R0 Y0 G0 W0 B0 
    # Hands:
    # Your Hand:
    # XX || RX|R12345
    # XX || RX|R12345
    # XX || XX|YGWB12345
    # XX || R1|R12345
    # XX || X2|YGWB12345
    # -----
    # W1 || XX|RYGWB12345
    # B2 || XX|RYGWB12345
    # W3 || XX|RYGWB12345
    # Y2 || XX|RYGWB12345
    # W4 || XX|RYGWB12345
    # -----
    # W1 || XX|RYGWB12345
    # B2 || XX|RYGWB12345
    # W3 || XX|RYGWB12345
    # Y2 || YX|RYGWB12345
    # W4 || XX|RYGWB12345
    # Deck size: 40
    # Discards:"""

    # print(parse_game_state(state_string))


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
