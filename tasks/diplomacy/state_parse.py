import json
from typing import List, Dict
from datetime import datetime

def generate_phase_history_prompt(history_phases: List[Dict], power_name: str) -> str:
    prompt = f"### Phase History for {power_name}\n\n"
    
    for phase in history_phases:
        phase_name = phase.get("name", "Unknown Phase")
        prompt += f"**Phase:** {phase_name}\n"
        
        # Extract non-empty orders
        orders = phase.get("orders", {})
        non_empty_orders = {power: orders_list for power, orders_list in orders.items() if orders_list}
        
        if non_empty_orders:
            prompt += "**Orders:**\n"
            for power, orders_list in non_empty_orders.items():
                orders_formatted = "; ".join(orders_list)
                prompt += f"- **{power}:** {orders_formatted}\n"
        else:
            prompt += "**Orders:** No orders issued.\n"
        
        # Extract results if not empty
        results = phase.get("results", {})
        non_empty_results = {move: outcome for move, outcome in results.items() if outcome}
        
        if non_empty_results:
            prompt += "**Results:**\n"
            for move, outcome in non_empty_results.items():
                outcome_formatted = ", ".join(outcome)
                prompt += f"- **{move}:** {outcome_formatted}\n"
        else:
            prompt += "**Results:** No results to report.\n"
        
        # Extract and sort relevant messages
        messages = phase.get("messages", [])
        relevant_messages = [
            msg for msg in messages
            if msg.get("sender") == power_name
            or msg.get("recipient") == power_name
            or msg.get("recipient") == "GLOBAL"
        ]
        
        # Sort messages by time_sent
        relevant_messages_sorted = sorted(relevant_messages, key=lambda x: x.get("time_sent", 0))
        
        if relevant_messages_sorted:
            prompt += "**Messages:**\n"
            for msg in relevant_messages_sorted:
                sender = msg.get("sender", "Unknown Sender")
                recipient = msg.get("recipient", "Unknown Recipient")
                # Convert timestamp to readable format if possible
                timestamp = msg.get("time_sent")
                try:
                    # Assuming the timestamp is in microseconds since epoch
                    dt = datetime.fromtimestamp(timestamp / 1e6)
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = str(timestamp)
                message = msg.get("message", "")
                prompt += f"- **From {sender} to {recipient} at {time_str}:** {message}\n"
        else:
            prompt += "**Messages:** No relevant messages.\n"
        
        prompt += "\n"  # Add a newline for separation between phases
    
    return prompt

def parse_diplomacy_state(state: dict) -> str:
    """
    Convert a Game.state (dict) into a human-readable message that lists
    key items like supply centers, units, notes, phases, etc.
    """
    descriptions = []

    note = state.get("note") or "No notes are provided for this state."
    phase_name = state.get("name", "Unknown phase")
    descriptions.append(f"Note: {note}")
    descriptions.append(f"Phase Name: The current game phase is '{phase_name}'.")

    # Units
    descriptions.append("Units: Stores the location of the units currently controlled by each player on the map:")
    for power, units in state.get("units", {}).items():
        unit_list = ", ".join(units)
        descriptions.append(f" {power}: {unit_list if unit_list else 'No units'}")

    # Retreats
    descriptions.append("Retreats: If a unit is defeated but not destroyed and it needs to retreat to a neighboring empty province. The units that need to retreat are as follows:")
    for power, retreats in state['retreats'].items():
        retreat_list = ', '.join([f"{unit} at {location}" for unit, location in retreats.items()]) if retreats else "No retreats needed."
        descriptions.append(f"  {power}: {retreat_list}")

    # Supply Centers
    descriptions.append("Supply Centers: The supply centers controlled by each player are:")
    for power, centers in state['centers'].items():
        center_list = ', '.join(centers)
        descriptions.append(f"  {power}: {center_list}")

    # Home Centers
    descriptions.append("Home Centers: Each player's initial or home supply centers are:")
    for power, homes in state['homes'].items():
        home_list = ', '.join(homes)
        descriptions.append(f"  {power}: {home_list}")

    # Parse influence
    descriptions.append("Influence: The regions influenced or controlled by each player are:")
    for power, influence in state['influence'].items():
        influence_list = ', '.join(influence)
        descriptions.append(f"  {power}: {influence_list}")

    # Parse civil_disorder
    descriptions.append("Civil Disorder: Status of players under civil disorder (1 for yes, 0 for no):")
    for power, disorder in state['civil_disorder'].items():
        descriptions.append(f"  {power}: {'Civil disorder' if disorder == 1 else 'No civil disorder'}")

    # Parse builds
    descriptions.append("Builds: Each player's allowable builds or disbands are:")
    for power, build_info in state['builds'].items():
        build_count = build_info['count']
        build_homes = ', '.join(build_info['homes']) if build_info['homes'] else "No specific build locations"
        descriptions.append(f"  {power}: {build_count} builds allowed. Homes available for builds: {build_homes}")

    # Join all descriptions into a final report
    final_report = "\n".join(descriptions)
    return final_report

def get_message_text(messages: dict, recipient: str, time_start: int, time_end: int) -> str:
    """
    Helper function to extract messages from the game log for a specific player
    or for GLOBAL, within a time range.
    """
    message_text = ""
    for k in sorted(messages.keys()):
        if time_start <= k <= time_end:
            if messages[k].recipient == recipient:
                message_text += f"{messages[k].sender}: {messages[k].message}\n"
            elif messages[k].recipient == "GLOBAL":
                message_text += f"{messages[k].sender} to all players: {messages[k].message}\n"
    return message_text

def get_message_text_bundle(messages: dict, recipients: list, time_start: int, time_end: int) -> str:
    """
    Helper function to extract messages from the game log for a list of recipients
    or for GLOBAL, within a time range.
    """
    message_text = ""
    for k in sorted(messages.keys()):
        if time_start <= k <= time_end:
            if messages[k].recipient in recipients:
                message_text += f"{messages[k].sender} to {messages[k].recipient}: {messages[k].message}\n"
            elif messages[k].recipient == "GLOBAL":
                message_text += f"{messages[k].sender} to all players: {messages[k].message}\n"
    return message_text