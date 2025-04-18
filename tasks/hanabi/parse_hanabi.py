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
