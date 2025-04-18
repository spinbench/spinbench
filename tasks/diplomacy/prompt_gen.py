import json
from typing import List, Dict
from datetime import datetime
from state_parse import parse_diplomacy_state

def gen_round_prompt(
    power_name: str,
    state: dict,
    possible_orders: str,
    phase: str,
    result: str,
    negotiation_rounds: int,
    neutral_powers: list=[]
    ) -> str:
    """
    Generate a basic descriptive prompt for the beginning of a round.
    Distinguishes between winter phases and other phases.
    """
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."

    return f"""
Now it's phase {phase}.
The current state of the game is as follows:
{parse_diplomacy_state(state)}
{neutral_prompt}
And the possible orders you can issue are as follows:
{possible_orders}
Remember, to win, you need to control enough supply centers.
This is the negotiation phase. There are {negotiation_rounds} total rounds of negotiation.
You don't need to talk with neutral countries.
"""

def gen_message_prompt(
    negotiation_round: int,
    total_negotiation_rounds: int,
    this_power_index: int,
    last_round_messages: str=None,
    end: bool=False,
    power_index_name_map: dict={},
    neutral_powers: list=[]
    ) -> str:
    """
    Generates the prompt for the negotiation messages.
    """
    # Recipients: build a list of recipients excluding self and neutral powers.
    receipient_list = [power_index_name_map[j] for j in range(len(power_index_name_map)) if j != this_power_index]
    for n in neutral_powers:
        if n in receipient_list:
            receipient_list.remove(n)
    # Convert the recipient list to a string.
    # Also add GLOBAL to send to everyone.
    recipient_list_str = ", ".join(
    receipient_list
    ) + ", GLOBAL"
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."

    if end:
        return f"""
The negotiation phase is over. The last negotiation round messages are as follows:
{last_round_messages if last_round_messages else "No messages from the last round."}
Please pay attention to the messages from other players, as they may contain important information about their intentions and strategies.
"""
    else:
        return f"""
It is now round {negotiation_round+1} of the negotiation phase.
There are {total_negotiation_rounds} total negotiation rounds.
After these, you must decide your actions.

The last round's messages are:
{last_round_messages if last_round_messages else "No messages from the last round."}

Please enter the message(s) that you would like to send, serialized as JSON with the format:
{{
"recipients": [...],
"messages": [...]
}}

The "recipients" field is a list of strings.

For example:
{{
"recipients": ["ENGLAND", "FRANCE"],
"messages": ["Hello, ENGLAND!", "Hello, FRANCE!"]
}}

Use standard double quotes. Do not add comments inside the output!
You can propose alliances, spread disinformation, or discuss any tactics.
You should talk with others about very concrete future actions, strategies, and tactics. You can also spread disinformation or make alliances. Remember, you are not bound to anything you say or promise, and no agreements are enforceable.
Valid recipients: {recipient_list_str} (the same index in the messages list corresponds to that recipient). {neutral_prompt} You don't need to send a message to neutral countries.
"""
    
def gen_negotiation_prompt_bundle(
    negotiation_round: int,
    total_negotiation_rounds: int,
    power_names: list,
    all_powers: list,
    last_round_messages: str = None,
    neutral_powers: list = [],
    end: bool = False
) -> str:
    """
    Generates a prompt for the negotiation messages, with a step-by-step chain of thought structure.
    The final output from the model should be a JSON object containing the analysis and the new messages.
    """

    # Recipients: build a list of recipients excluding self and neutral powers.
    recipient_list = []
    for i in all_powers:
        if i not in power_names and i not in neutral_powers:
            recipient_list.append(i)
    # Convert the recipient list to a string.
    # Also add GLOBAL to send to everyone
    recipient_list_str = ", ".join(
        recipient_list
    )
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
    if end:
        return f"""
We have reached the end of the negotiation phase {negotiation_round}/{total_negotiation_rounds}.

Below is the final round of negotiation messages:
{last_round_messages if last_round_messages else "No messages from the last round."}

Now, please analyze and reflect on the outcomes of the ENTIRE negotiation phase. 

Use the following structured flow to guide your analysis:

## Think step by step

1. **Comprehensive Recap:**
   1.1. Summarize all major proposals, promises, threats, or demands made by each power (including you).
   1.2. Note any contradictions, changes in stance, or surprising offers during the negotiation phase.

2. **Honesty & Deception Assessment:**
   2.1. Discuss whether you believe other powers will stay true to their word or if they might deceive you.
   2.2. Acknowledge if you have made deceptive statements and how you think others have perceived them.

3. **Resulting Deals and Alliances:**
   3.1. List any agreements you consider binding (even if informally).
   3.2. Identify any planned joint attacks, mutual supports, or non-aggression pacts.
   3.3. Note which powers you intend to cooperate with or betray.

4. **Next Action Phase Outlook:**
   4.1. Explain how the negotiation outcomes influence your immediate next actions on the board.
   4.2. Highlight which commitments you will keep or break if it serves your path to victory.
   4.3. Identify which regions or supply centers you aim to target in the next phase, given the negotiation context.

5. **Strategic Adjustments & Goals:**
   5.1. Clarify if your overarching strategy changed as a result of these negotiations.
   5.2. Note any additional steps to prepare or reposition units for an attack or defense.
   5.3. Summarize your final stance on alliances vs. confrontations with each power.

6. **Reminder for Next Action Phase:**
   6.1. Emphasize that any pledges or deals are not guaranteed by the game rules and may be reneged if needed.
   6.2. Acknowledge you must craft your next set of orders (moves, supports, etc.) based on these reflections.

After completing your chain-of-thought analysis, provide your final reflection as a JSON object in the following format:

{{
  "phase": "post_negotiation_reflection",
  "final_agreements": [
    {{
      "power": "FRANCE",
      "agreement": "We agreed to DMZ in Burgundy, no units to move there."
    }},
    ...
  ],
  "alliances_betrayals": [
    {{
      "power": "GERMANY",
      "relationship": "ally/betray/neutral",
      "explanation": "Why we plan to ally or betray them."
    }},
    ...
  ],
  "next_phase_plans": "Summary of how your negotiations shape your impending moves, targets, or supports.",
  "reflection_notes": "Additional notes or reminders to yourself about the upcoming action phase."
}}

### Explanation of Fields

- **phase**: Always set to "post_negotiation_reflection" to mark this as the reflection stage.
- **final_agreements**: 
  - A list of dictionaries describing any critical agreements you formed, even if you intend to break them later.
- **alliances_betrayals**:
  - A list of dictionaries indicating your stance on each major power after negotiations.
- **next_phase_plans**:
  - A high-level summary of how you plan to act in the immediate next phase—attacks, defenses, or further positioning.
- **reflection_notes**:
  - Any additional final observations or reminders you want to keep in mind for the next action phase.

Remember to keep all keys and string values in standard double quotes. Avoid including comments in the JSON. Make your reflection as honest and thorough as possible for your own strategic benefit.

Happy reflecting—use these insights to conquer the board in the next action phase!
"""
    else:
        # Detailed chain-of-thought prompt
        return f"""
It is now round {negotiation_round+1} of the negotiation phase.
There are {total_negotiation_rounds} total negotiation rounds.
After these, you must decide your actions.

You are playing as {power_names}. The other powers are: {', '.join([i for i in all_powers if i not in power_names])}.

The last round's messages are:
{last_round_messages if last_round_messages else "No messages from the last round."}

Now you must analyze the negotiation phase step by step, then provide your final messages in a JSON object.

## Think step by step

1. **Recap & Trust Analysis:**
   1.1. Recap each message from the last round, identifying who said what.
   1.2. Assess their intentions and whether they might be truthful or deceptive.
   1.3. Discuss how much you trust each power's statements based on their track record or alignment with your interests.

2. **Current State and Strategic Analysis:**
   2.1. Summarize your current strategic position (units, supply centers, alliances, conflicts).
   2.2. Summarize your opponents' positions (who seems strong, who seems weak, who might be desperate).
   2.3. Identify any immediate threats or opportunities for alliances, betrayals, or beneficial deals.

3. **Goal Setting:**
   3.1. Reiterate your ultimate objective (gain more supply centers, dominate the map).
   3.2. Decide how to approach each power: ally, remain neutral, or plan to attack soon.

4. **Negotiation Strategy:**
   4.1. Determine which powers you want to communicate with this round and why.
   4.2. Decide whether to propose alliances, coordinate attacks, request/demand support, or spread disinformation.
   4.3. Consider carefully any promises you might make (remember they are not binding).

5. **Message Drafting:**
   5.1. Outline the content of each message to each recipient.
   5.2. Make sure your messages are concrete: specify regions, proposed moves, or conditions for cooperation.
   5.3. Keep in mind the possibility of someone sharing your messages (lack of enforceability).

6. **Review & Finalize:**
   6.1. Verify if your negotiation plan is consistent with your overall strategy.
   6.2. Finalize the messages you will send out.

After you finish your step-by-step reasoning, provide the result as a JSON object with the following format:

{{
  "phase": "negotiation_phase{negotiation_round}",
  "trust_analysis": [
    {{
      "power": "ENGLAND",
      "trust_level": "low/medium/high",
      "analysis": "explanation of why"
    }},
    ...
  ],
  "negotiation_strategy": "In-depth explanation of how you're approaching each power (alliance, deception, etc.)",
  "messages": {{
    "FRANCE": {{
      "recipients": ["GERMANY", "GLOBAL"],
      "messages": [
        "Hello Germany, I'd like your support in Burgundy.",
        "Greetings everyone, I propose a mutual ceasefire this turn."
      ]
    }},
    "TURKEY": {{
      "recipients": ["RUSSIA"],
      "messages": [
        "I propose we coordinate against Austria in the Black Sea."
      ]
    }},
    ...
  }}
}}

### Explanation of Fields:

- **phase:** Always set this to "negotiation_phase{negotiation_round}" for this round of negotiation phase.
- **trust_analysis:** 
  - A list of dictionaries analyzing how much you trust each other power. 
  - For each entry, note the power, your trust level, and a brief explanation of why.

- **negotiation_strategy:**
  - Describe your overarching plan for dealing with the other powers, including proposals, alliances, or sabotage.

- **messages**: A dictionary where each key is one of the powers that you control. You don't need to send a message to neutral countries or yourself.
  - For each key (e.g. "FRANCE"), the value is another dictionary:
    - `"recipients"`: 
        - A list of strings representing who you are sending messages to. 
        - Valid recipients: {recipient_list_str}
        - You can also include "GLOBAL" to broadcast a message to all powers simultaneously.
    - `"messages"`: a list of strings, each corresponding to a message directed to the recipients in the same order.
        - If you list two recipients, the first message is intended for the first recipient, the second message for the second recipient, and so on.

Use only standard double quotes in your JSON. Do not include Python-style triple-quoted strings or comments inside the JSON output.

{neutral_prompt}

Happy negotiating—analyze carefully and craft your messages with purpose!
"""
    
def gen_winter_action_prompt(power_name, state, possible_orders: str, neutral_powers) -> str:
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
    return f"""
Now it's winter adjustment phase, and you are {power_name}. It is now your turn to play.
The current state of the game is as follows:
{parse_diplomacy_state(state)}
{neutral_prompt}
This is the build/disband phase. You can build new units in your home centers, or disband units if you have too many. Remember, you need to control enough supply centers to win.

Please respond with a JSON object like:
{{
"reason": "Your strategic reasoning here",
"orders": ["A BER-MUN", "F NTH-ENG", ...]
}}

Where "orders" is a list of each location's decision. For each location, you can only issue one order.
The length of the list should match the number of locations for which you can issue orders.

The string should be able to be parsed to json str. So don't use special characters like \\n, \\t, etc. Generate the text with standard straight double quotes. Do not add comments inside the output! 
The possible orders you can issue are as follows:
{possible_orders}
Remember, you need to reach the configured number of supply centers (build more and more supply centers) to win.
"""

def gen_winter_action_prompt_bundle(power_names, state, possible_orders: str, neutral_powers) -> str:
    assert isinstance(power_names, list), "power_names should be a list of power names."
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
    return f"""
Now it's winter adjustment phase, and you are playing {power_names}. It is now your turn to play.
The current state of the game is as follows:
{parse_diplomacy_state(state)}
{neutral_prompt}
This is the build/disband phase. You can build new units in your home centers, or disband units if you have too many. Remember, you need to control enough supply centers to win.

Please respond with a JSON object like:
{{
"reason": "Your strategic reasoning here",
"orders": {{
    "FRANCE": ["F BRE B", "A PAR B", ...],
    ...
}}
}}

Where "orders" is a dictionary where the key is the power name and the value is a list of each location's decision. For each location, you can only issue one order. The length of the list of each power should match the number of locations for which you can issue orders.

The string should be able to be parsed to json str. So don't use special characters like \\n, \\t, etc. Generate the text with standard straight double quotes. Do not add comments inside the output! 
The possible orders you can issue are as follows:
{possible_orders}
Remember, you need to reach the configured number of supply centers (build more and more supply centers) to win.
"""

def gen_retreat_action_prompt(power_name, state, possible_orders: str, neutral_powers) -> str:
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
    return f"""
Now it's the retreat phase, and you are {power_name}. It is now your turn to play.

The current state of the game is as follows:
{parse_diplomacy_state(state)}
{neutral_prompt}
This is the retreat phase. You must retreat your units that have been dislodged. If you do not retreat a unit, it will be disbanded.

Please respond with a JSON object like:
{{
"reason": "Your strategic reasoning here",
"orders": ["A MUN R BOH", ...]
}}

Where "orders" is a list of each location's decision. For each location, you can only issue one order. The length of the list should match the number of locations for which you can issue orders.

The string should be able to be parsed to json str. So don't use special characters like \\n, \\t, etc. Generate the text with standard straight double quotes. Do not add comments inside the output!
The possible orders you can issue are as follows:
{possible_orders}
"""

def gen_retreat_action_prompt_bundle(power_names, state, possible_orders: str, neutral_powers) -> str:
    assert isinstance(power_names, list), "power_names should be a list of power names."
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
    return f"""
Now it's the retreat phase, and you are playing {power_names}. It is now your turn to play.

The current state of the game is as follows:
{parse_diplomacy_state(state)}
{neutral_prompt}
This is the retreat phase. You must retreat your units that have been dislodged. If you do not retreat a unit, it will be disbanded.

Please respond with a JSON object like:
{{
"reason": "Your strategic reasoning here",
"orders": {{
    "FRANCE": ["A MAR R SPA", ...],
    ...
}}
}}

Where "orders" is a dictionary where the key is the power name and the value is a list of each location's decision. For each location, you can only issue one order. The length of the list of each power should match the number of locations for which you can issue orders.

The string should be able to be parsed to json str. So don't use special characters like \\n, \\t, etc. Generate the text with standard straight double quotes. Do not add comments inside the output!
The possible orders you can issue are as follows:
{possible_orders}
"""

def gen_action_prompt(power_name, state, possible_orders: str, adj_information=None, neutral_powers=[]) -> str:
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
# Those are all the adjacent regions of your orderable regions.
# {adj_information if adj_information else "No adjacent information available."}
    return f"""
Now it's your turn to take the action, and you are playing {power_name}.
The current state of the game is as follows:
{parse_diplomacy_state(state)}
{neutral_prompt}

First please think step by step given my instructions, do some self verification and revise on your orders:

## Think step by step, show me your detailed reasoning in those aspects

1. Please analyze the current state of the game and your position. Which regions are you controlling? How many supply centers do you have? Where are your units? Please make detailed state analysis about you and other powers.
2. The goal of the game is to take control as many supply centers as possible. Analyze your current state, and plan how to take more supply centers later. For example, among the regions which are not your location, which location do you want to attack? You should think if you will have enough support to win each attack.
3. For each of your units, analyze the possible orders. I will give you all the possible orders enclosed in <possible_orders> for each of your unit. Please consider and tell me your reasoning for each the following points: 
    3.1. Whether you should move into other regions to expand or take more supply centers? 
    3.2. Whether you should move into other power's unit to attack? 
    3.3. If you don't have enough unit to attack some region, do you want to move your other unit to the adjacent region to prepare for the attack in the next round? 
    3.4. When you choose your attack target, don't set it as your controlled region. Iterate over your planned attack targets, and tell me whether that target is among your controlled region. If you find a target as your attack target, please make sure that target is other power's location, not your own location. Moving into your unit is not considered an attack! 
    3.5. A unit may not move into a province held by another unit unless it has support, and the attacking unit must have more support than the defending unit if the attack is to be successful. If you want to attack other power's unit, do you have other units support this move?
    3.6. A unit can only move to its adjacent region. Please iterate over your unit's adjacent regions, and make sure that your move target is among its adjacent regions.
    3.7. The support unit can only support the adjacent region. Please iterate over your unit's adjacent regions, and make sure that your support target is among its adjacent regions. If the unit can't support attacking the target because it's too far, you should choose another supporter or move it closer and plan to attack later.
    3.8. If you want to support unit X attacking some region, you should make sure X is actually attacking the target region. If not, it is invalid.
4. Make the order decision based on your analysis. Check your decision about whether you set a wrong attack target, move into your controlled region is not an attack!!!
5. For each intended order, please revise and verify your move target and the reason against the definitions, game rules, and your goal. For example, 
    5.1. Moving your unit into your own region is not considered an attack. You should move into other power's unit location. 
    5.2. You should take control more and more supply centers
    5.3. Ensure that your attacks are supported sufficiently to overcome any defenses.
    5.4. Iterate over your planned attack targets, and tell me whether that target is among your controlled region. If so, you should start from the beginning and think again. 
    5.5. IIterate over your planned attack targets, and compute how many other power's units are in that target location. Next, determine how many of your own units and how much support you need to succeed in the attack. You cannot attack with fewer supports than the defending unit. Verify that the total of your supports plus one is greater than the defending unit's strength. If this condition is not met, return to the beginning and think again.
    If your orders can't pass the verification, please start from the beginning and think again by the above steps.

Once you are confident, please finalize your plan, and give me a JSON object in the following format:

{{
    "phase": "current_phase",
    "step_by_step_reasoning": "Your step by step reasoning here",
    "reason": "Your strategic reasoning here",
    "my_location": ["PAR", ...],
    "my_unit": ["BER", ...],
    "adjacent": [{{"PAR": ["BUR", "GAS"]}}, ...],
    "other_power_location": ["MUN", ...],
    "move_to_our_region_mask": [0, 1, ...],
    "attackable": ["MUN", ...],
    "attack_analysis": [{{"MUN": 2}}, ...],
    "support_given": [{{"supporter": "BUR", "supported": "PAR", "target": "PIC"}}, ...],
    "attack_mask": [1, 0, ...],
    "orders": ["A BER-MUN", "F NTH-ENG", ...],
}}


### Instructions for the JSON object:

1. **Reason:**
   - Provide your strategic reasoning summary in the "reason" field.

2. **Additional Fields:**

   - **step_by_step_reasoning:**
     - Provide your above step by step reasoning details in the "step_by_step_reasoning" field.

   - **my_location:**
     - A list of strings.
     - Each element corresponds to a location where you have the influence or control (Please refer to the game state).
     - Example: `["MUN", ...]`

   - **my_unit:**
     - A list of strings.
     - Each element corresponds to a location where you have a unit.
     - Example: `["BER", ...]`

   - **adjacent:**
     - A list of dictionary.
     - Each element is a dictionary with your location as the key and a list of all the adjacent locations as the value.
     - Example: `[{{"MUN": ["TYR", "BOH"]}}, ...]`

   - **other_power_location:**
     - A list of strings.
     - Each element corresponds to a location that is other power's location.
     - Example: `["MUN", ...]`

   - **move_to_our_region_mask:**
     - A list of integers (0 or 1).
     - Each element corresponds to an order in the "orders" list.
     - `1` indicates that the order involves moving to your influenced or controlled region. (Please refer to the game state)
     - `0` indicates that the order does not involve moving to your influenced or controlled region.
     - Example: `[0, 1, 0]`

   - **attackable:**
     - A list of locations.
     - Each location is a region that is other power's location and you can move into to attack in this turn.
     - You should NOTICE, you usually made mistakes here! The locations in my_location and my_unit should not be included in this list. You can only choose from adjacent locations.
     - Example: `["MUN", ...]`

   - **attack_analysis:**
    - A list of dictionaries.
    - Each dictionary contains key: the location string you want to attack in this round. value: the number of units anyone needs to win the attack. A unit may not move into a province held by another unit unless it has support. As units may be supported either in attacking a province or in holding a province, the attacking unit must have more support than the defending unit if the attack is to be successful. If the attack is not successful, the attacking unit does not move anywhere. I already gave you other powers' unit locations above. Only an estimate is needed here. Because you don't know whether other powers will support or not.
    - Example: `[{{"MUN": 2}}, {{"RUH": 1}} ...]`

   - **support_given:**
     - A list of dictionaries.
     - Each dictionary contains the supported unit's location and the location of the unit being supported. And the target location. (based on the order you want to issue)
     - Example: `[{{"supporter": "BOH", "supported": "MUN", "target": "TYR"}}, ...]`

   - **attack_mask:**
     - A list of integers (0 or 1). The same length as the "orders" list.
     - Each element corresponds to an order in the "orders" list. If the target is in my_location, it is not considered an attack. Attack is moving into other power's unit location.
     - `1` indicates that the order is an attack.
     - `0` indicates that the order is not an attack.
     - Example: `[1, 0, 1]`

3. **Orders:**
    - The "orders" field should be a list of strings chosen from the possible orders.
    - For each location, you can only issue one order.
    - The number of orders should match the number of locations you can issue orders for.
    - Each string represents an order for a unit.
    - If possible_orders is empty, just leave the "orders" field empty.

4. **JSON Formatting Guidelines:**
   - Use standard straight double quotes (`"`).
   - Do not include special characters like `\n`, `\t`, etc.
   - Do not add comments inside the JSON output.

### **Possible Orders:**

All the possible orders that you can issue are as follows (key is the location, value is the list of possible orders at that location):

<possible_orders>
{possible_orders}
</possible_orders>

### **Your Objective:**

Your ultimate goal is absolute domination—seize every supply center and crush your opposition to win! Build and expand relentlessly, taking control of regions by launching bold, decisive attacks, control as many supply center as you can. Strike hard, strike fast, and let nothing stand in your way. Victory belongs to the bold—go conquer it!

"""

def gen_action_prompt_bundle(power_names, state, possible_orders: str, adj_information=None, neutral_powers=[]) -> str:
    assert isinstance(power_names, list), "power_names should be a list of power names."
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
    return f"""
Now it's your turn to issue orders, and you are playing as {power_names}.
The current state of the game is as follows:
{parse_diplomacy_state(state)}
{neutral_prompt}

The adjacent regions of your orderable regions are as follows:
<adjacent_regions>
{adj_information if adj_information else "No adjacent information provided."}
</adjacent_regions>

First please think step by step given my instructions, do some self verification and revise on your orders:

## Think step by step

0. You should recap all the information in the previous negotiation phase, remember the agreements, promises, and threats made by each power. Analyze the outcomes of the negotiation phase and how they influence your next actions on the board.
1. Please analyze the current state of the game and your position. Which regions are you controlling? How many supply centers do you have? Where are your units? Please make detailed state analysis about you and other powers.
2. The goal of the game is to take control as many supply centers as possible. Analyze your current state, and plan how to take more supply centers later. For example, among the regions which are not your location, which location do you want to attack? You should think if you will have enough support to win each attack. You should also check all your adjcent regions and make sure you can move to them, based on <adjacent_regions> information.
3. For each of your units, analyze the possible orders. I will give you all the possible orders enclosed in <possible_orders> for each of your unit. Please consider and tell me your reasoning for each the following points: 
    3.1. Whether you should move into other regions to expand or take more supply centers? 
    3.2. Whether you should move into other power's unit to attack? 
    3.3. If you don't have enough unit to attack some region, do you want to move your other unit to the adjacent region to prepare for the attack in the next round? 
    3.4. When you choose your attack target, don't set it as your controlled region. Iterate over your planned attack targets, and tell me whether that target is among your controlled region. If you find a target as your attack target, please make sure that target is other power's location, not your own location. Moving into your unit is not considered an attack! 
    3.5. A unit may not move into a province held by another unit unless it has support, and the attacking unit must have more support than the defending unit if the attack is to be successful. If you want to attack other power's unit, do you have other units support this move?
    3.6. A unit can only move to its adjacent region. Please iterate over your unit's adjacent regions, and make sure that your move target is among its adjacent regions.
    3.7. The support unit can only support the adjacent region, and the attack target should also be its adjacent region. Please iterate over your unit's adjacent regions, and make sure that your support target is among its adjacent regions. If the unit can't support attacking the target because it's too far, you should choose another supporter or move it closer and plan to attack later.
    3.8. If you want to support unit X attacking some region, you should make sure X is actually attacking the target region. If not, it is invalid.
4. Make the order decision based on your analysis. Check your decision about whether you set a wrong attack target, move into your controlled region is not an attack!!!
5. For each intended order, please revise and verify your move target and the reason against the definitions, game rules, and your goal. For example, 
    5.1. Moving your unit into your own region is not considered an attack. You should move into other power's unit location. 
    5.2. You should take control more and more supply centers
    5.3. Ensure that your attacks are supported sufficiently to overcome any defenses.
    5.4. Iterate over your planned attack targets, and tell me whether that target is among your controlled region. If so, you should start from the beginning and think again. 
    5.5. IIterate over your planned attack targets, and compute how many other power's units are in that target location. Next, determine how many of your own units and how much support you need to succeed in the attack. You cannot attack with fewer supports than the defending unit. Verify that the total of your supports plus one is greater than the defending unit's strength. If this condition is not met, return to the beginning and think again.
    If your orders can't pass the verification, please start from the beginning and think again by the above steps.

Once you are confident, please finalize your plan, and give me a JSON object in the following format:

{{
    "phase": "current_phase",
    "reason": "Your strategic reasoning here",
    "my_location": ["PAR", ...],
    "my_unit": ["BER", ...],
    "adjacent": [{{"PAR": ["BUR", "GAS"]}}, ...],
    "other_power_location": ["MUN", ...],
    "move_to_our_region_mask": [0, 1, ...],
    "attackable": ["MUN", ...],
    "attack_analysis": [{{"MUN": 2}}, ...],
    "support_given": [{{"supporter": "BUR", "supported": "PAR", "target": "PIC"}}, ...],
    "attack_mask": {{
        "FRANCE": [1, 0, ...],
        ...
    }}
    "orders": {{
        "FRANCE": ["F BRE - MID", "A PAR - BUR", ...],
        ...
    }}
}}


### Instructions for the JSON object:

1. **Reason:**
   - Provide your strategic reasoning summary in the "reason" field.

2. **Additional Fields:**

   - **my_location:**
     - A list of strings.
     - Each element corresponds to a location where you have the influence or control (Please refer to the game state).
     - Example: `["MUN", ...]`

   - **my_unit:**
     - A list of strings.
     - Each element corresponds to a location where you have a unit.
     - Example: `["BER", ...]`

   - **adjacent:**
     - A list of dictionary.
     - Each element is a dictionary with your location as the key and a list of all the adjacent locations as the value. Please refer to <adjacent_regions>
     - Example: `[{{"MUN": ["TYR", "BOH"]}}, ...]`

   - **other_power_location:**
     - A list of strings.
     - Each element corresponds to a location that is other power's location.
     - Example: `["MUN", ...]`

   - **move_to_our_region_mask:**
     - A list of integers (0 or 1).
     - Each element corresponds to an order in the "orders" list.
     - `1` indicates that the order involves moving to your influenced or controlled region. (Please refer to the game state)
     - `0` indicates that the order does not involve moving to your influenced or controlled region.
     - Example: `[0, 1, 0]`

   - **attackable:**
     - A list of locations.
     - Each location is a region that is other power's location and you can move into to attack in this turn.
     - You should NOTICE, you usually made mistakes here! The locations in my_location and my_unit should not be included in this list. You can only choose from adjacent locations.
     - Example: `["MUN", ...]`

   - **attack_analysis:**
    - A list of dictionaries.
    - Each dictionary contains key: the location string you want to attack in this round. value: the number of units anyone needs to win the attack. A unit may not move into a province held by another unit unless it has support. As units may be supported either in attacking a province or in holding a province, the attacking unit must have more support than the defending unit if the attack is to be successful. If the attack is not successful, the attacking unit does not move anywhere. I already gave you other powers' unit locations above. Only an estimate is needed here. Because you don't know whether other powers will support or not.
    - Example: `[{{"MUN": 2}}, {{"RUH": 1}} ...]`

   - **support_given:**
     - A list of dictionaries.
     - Each dictionary contains the supported unit's location and the location of the unit being supported. And the target location. (based on the order you want to issue)
     - Example: `[{{"supporter": "BOH", "supported": "MUN", "target": "TYR"}}, ...]`

   - **attack_mask:**
     - A dictionary of lists of integers (0 or 1). The same length as the "orders" list.
     - Each element corresponds to an order in the "orders" list. If the target is in my_location, it is not considered an attack. Attack is moving into other power's unit location.
     - `1` indicates that the order is an attack.
     - `0` indicates that the order is not an attack.
     - Example: `{{"FRANCE": [1, 0, ...], ...}}`

3. **Orders:**
    - The "orders" field should be a dictionary where the key is the power name and the value is a list of strings chosen from the possible orders.
    - For each location, you can only issue one order.
    - The number of orders should match the number of locations you can issue orders for.
    - Each string represents an order for a unit.
    - If possible_orders is empty for a power, just leave the "orders" field empty for that power.

4. **JSON Formatting Guidelines:**
   - Use standard straight double quotes (`"`).
   - Do not include special characters like `\n`, `\t`, etc.
   - Do not add comments inside the JSON output.

### **Possible Orders:**

All the possible orders that you can issue are as follows (key is the location, value is the list of possible orders at that location):

<possible_orders>
{possible_orders}
</possible_orders>

### **Your Objective:**

Your ultimate goal is absolute domination—seize every supply center and crush your opposition to win! Build and expand relentlessly, taking control of regions by launching bold, decisive attacks, control as many supply center as you can. Strike hard, strike fast, and let nothing stand in your way. Victory belongs to the bold—go conquer it!

"""

def gen_init_prompt(index_power_name, i, neutral_powers=[], power_names=[]):
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
    return f"""
You are playing a game of Diplomacy against 6 opponents. Diplomacy is a 7-player turn based game, where players must use negotiation and strategy to control the most supply centers on the map. The players can move their units to different locations on the map, and can support other players' units to help them succeed. The game is played on a map of Europe, divided into territories and sea zones. The players can issue orders to their units to move, support, hold, or convoy. The game ends when one player controls 18 supply centers.

34 of the land provinces are supply centers. Possession of these supply centers allows the powers who control them to raise and maintain armies and fleets. As they are also a central part of the game's victory conditions, they are the focus of much of the game's activity.

Each player is given three (save for Russia, which has four) home supply centers. These spaces are the starting point for their owning power's initial forces. The players can then build new units at these home supply centers as they capture further supply centers. New units can only be built on a power's home supply centers. If a power loses all of its home supply centers it may continue to play; however, it may not build new units until it has recaptured at least one of its home supply centers.

In Diplomacy, there are two types of units: Armies and Fleets. An army can travel in land spaces and coastal land spaces, and a fleet can travel in sea spaces and coastal land spaces.

All units in Diplomacy move only one space at a time and only one unit may occupy any space at any time. The exception to this rule comes in the form of a successful convoy, where a convoyed army may travel multiple spaces depending on the length of the chain created by the convoying fleets. A convoyed army must embark from a coastal land province and land at a coastal land province.

Diplomacy proceeds by seasons, beginning in the year 1901, with each year divided into two main seasons: the "Spring" and "Fall" (Autumn) moves. Each season is further divided into negotiation and movement phases, followed by "retreat" or "disband" adjustments and an end-of-the-year Winter phase of new builds or removals following the Fall adjustments.
                                  
Negotiation phase

In the negotiation phase, players discuss tactics and strategy, form alliances, and share intelligence or spread disinformation. Negotiations may be made public or kept private. Players are not bound to anything they say or promise, and no agreements are enforceable.
Communication and trust are highly important; players must forge alliances with others and observe their actions to evaluate their trustworthiness. At the same time, they must convince others of their own trustworthiness while making plans to turn against their allies when least expected. A well-timed betrayal can be just as profitable as an enduring, reliable alliance.

Movement phase

After the negotiation period, players write secret orders for each unit; these orders are revealed and executed simultaneously. A unit can move from its location to an adjacent space, support an adjacent unit to hold an area in the event of an attack, support another unit to attack a space into which it could move itself, or hold defensively. In addition, fleets may transport armies from one coast space to another when in a chain called a "convoy". Armies may only occupy land regions, and fleets occupy sea regions and the land regions that border named seas. Only one unit may occupy each region. If multiple units are ordered to move to the same region, only the unit with the most support moves there. If two or more units have the same highest support, a standoff occurs and no units ordered to that region move. A unit ordered to give support that is attacked has those orders canceled and is forced to hold, except in the case that support is being given to a unit invading the region from which the attack originated (in which case the unit that had been ordered to give support must retreat from, rather than hold, its position).
Certain spaces on the board have two coasts and here a player must specify which one they want their fleet to occupy. A fleet can only move to coasts and oceans that border the coast that it is on. For example, a fleet occupying the southern coast of Bulgaria cannot move into Romania or the Black Sea, but a fleet on the east coast could.

In the game of Diplomacy, an action space is the collection of all the legal actions that each country or unit can take in each round. The following are common types of actions in games and their common formats:

1. Attack/Move

This order moves the unit in one province to an adjacent province. Of course, armies cannot move into sea provinces, and fleets cannot move into landlocked provinces.

A unit may not move into a province held by another unit unless it has support. As units may be supported either in attacking a province or in holding a province, the attacking unit must have more support than the defending unit if the attack is to be successful. If the attack is not successful, the attacking unit does not move anywhere.

Two units may not swap provinces, unless there is a convoy involved. 

The format is:

A [province] - [target province] (Army moves from current position to target province)
F [province] - [target province] (Fleet moves from current position to target province)
For example:

A BER - MUN indicates that the army from Berlin moved to Munich.
F NTH - ENG indicates the movement of the fleet from the North Sea (NTH) to the English Channel (ENG).

When the destination province is occupied by another unit, they do not move, unless either are attacked or defended by stronger support. When two units with equal support try to move into the same destination province, for instance:

Germany
A MUN - TYR

Italy
A VEN - TYR

Neither of the two units can go into Tyrolia. Army Venice will stay in Venice, and Army Munich will stay in Munich. Again, this is assuming that these two units are the only two units in this little battle, and that they have equal support for their moves.

2. Support

Support is the trickiest aspect of the rules, and the most important of the game. Support may involve cooperation between two (or more) powers, and is the only way to make forward progress through enemy territory (unless you can convince the enemy to let you in). Simply put, more support defeats less support.

The support order is given in reference to another unit's move. That other unit's move must be to a province into which the supporting unit could otherwise move. Support may also be given to a unit holding its position. In addition, units giving support can themselves be supported in their holding position.

Support is a unit's sole action for a given move, and supporting units remain where they are (unless they are attacked by greater support and have to retreat or disband during the retreat phase).

A country cannot dislodge or support the dislodgement of one of its own units, although if same country's units attempt to move into the same province with equal support, neither will succeed as normal.

Cutting Support: If the supporting unit is attacked during the turn by some other unit, its support is cut. In effect, the support order becomes a hold order, as the unit must defend its province against the attack. Note that a unit occupying the province into which the support is directed cannot cut support, unless its attack successfully dislodges the supporting unit. An attack by a country on one of its own units also doesn't cut support.

The format is:

A [province] S A [target province] - [destination] (support army movement)
A [province] S A [target province] (supporting the garrisoning of the army)
F [province] S F [target province] - [destination] (Support fleet movement)
F [province] S F [target province] (garrisoning of supporting fleet)
For example:

A BER S A MUN indicated that the Army in Berlin supported the Army garrison in Munich.
A BER S A MUN-KIE stated that the Army of Berlin supported the Army of Munich in moving to Kiel.

Other example:

NB: Below are complete orders as submitted by all 7 Powers for the Fall 1907 campaign season of a made-up game to help you understand the intricacies of supporting and breaking support. Having a game map to look on with is highly recommended; the one provided at the top of this page is adequate.


We'll start with:

--Germany--
Army Ruhr to Holland
Fleet Kiel supports Army Ruhr to Holland
Army Munich supports Army Ruhr to Holland
Note that in this case the order for Munich to support Ruhr into Holland would not work because Munich does not border Holland and thus cannot support Ruhr in (Munich could, however, support Ruhr if Ruhr were simply holding). The rule for supporting an attack is that a supporting unit must border the province being attacked, but need not border the attacker's province of origin (to support a unit to hold, however, the supporting unit must border the supported unit). Essentially, the supporting unit must border the destination of the supported unit, whether it is its own province or a new province entirely. In sum, Ruhr is actually attacking Holland with the support of only one unit (Fleet Kiel).

Army Prussia supports Army Silesia
Army Silesia supports Army Prussia
Here, Army Prussia is supported by one unit, and Army Silesia is supported by one unit. The last two moves are legal, and this method of double-support is helpful when there are two units that both could be attacked and dislodged. Of course, if both units are attacked, the support fails.


--England--
Army London to Holland
Fleet North Sea convoys Army London to Holland (<-- a convoy)
Fleet Heligoland Bight supports Army London to Holland
Note that the convoying fleet is not considered to be giving support, so Army London actually has support from only one unit: Fleet Heligoland-Bight.

Army Denmark to Kiel
Here England interferes with Germany's plans (see Germany, above) by attacking Kiel with Army Denmark. This cuts the support of Fleet Kiel to Army Ruhr, thereby leaving Army Ruhr's attack on Holland unsupported.

Army London, on the other hand, (see above) is supported in its attack on Holland by one unit (Fleet Heligoland-Bight), thereby enabling Army London to be convoyed successfully into Holland, as long as Fleet North Sea is not dislodged during the convoy.

Army Picardy to Brest
Fleet Mid-Atlantic Ocean supports Army Picardy to Brest
Fleet English Channel supports Army Picardy to Brest
Here Army Picardy is supported by both Fleet Mid-Atlantic Ocean and Fleet English Channel to move into Brest. Unless the French successfully defend it, England will also take Brest.


--France--

Fleet Gascony to Mid-Atlantic Ocean
Fleet Irish Sea to English Channel
Fleet Gascony and Fleet Irish Sea cut the support by Fleet Mid-Atlantic Ocean and Fleet English Channel for England's Army Picardy (see England, above). Therefore, Army Picardy is now attacking Brest unsupported.

Fleet Brest holds
Army Paris supports Fleet Brest
Army Paris supports Fleet Brest, and so Army Picardy’s now unsupported attempt to move into Brest fails.

Army Burgundy to Ruhr
Army Burgundy does not successfully move into Ruhr because Army Ruhr’s move to Holland failed (see Germany and England, above).


--Russia--

Fleet Sevastopol holds
Army Moscow supports Fleet Sevastopol

Fleet Sevastopol is supported by Army Moscow.

Fleet St. Petersburg (North Coast) to Norway
Army Finland supports Fleet St. Petersburg (North Coast) to Norway

Norway is not occupied, so Russia takes it immediately.

Army Livonia to Prussia

Unsupported Army Livonia attempts to move into Prussia, but since Army Prussia is supported by Army Silesia (see Germany, above), the attack is not successful.


--Austria-Hungary--

Army Ukraine supports Fleet Sevastopol

Army Ukraine supports Fleet Sevastopol, so there are now two units supporting (see Russia, above). In fact, international support is necessary in alliances, whether supporting each other in defence or to attack another Power.

Fleet Trieste holds
Army Budapest supports Fleet Trieste
Army Vienna supports Fleet Trieste

There are two units supporting Fleet Trieste: Army Budapest and Army Vienna.


--Turkey--

Army Galicia to Ukraine

Army Galicia cuts the Austrian support to Sevastopol, thereby decreasing the support to Sevastopol by one unit (see Austria and Russia, above).

Fleet Black Sea to Sevastopol
Army Armenia supports Fleet Black Sea to Sevastopol
Army Rumania supports Fleet Black Sea to Sevastopol

Now, since Fleet Black Sea is supported by two units into Sevastopol, Fleet Black Sea moves into Sevastopol, and Fleet Sevastopol has to be disbanded or retreat. A retreating fleet that is displaced by another force can only retreat into a movable space (i.e. a sea or coastal province that is vacant) which may not be the same space that was previously occupied by the displacing unit.

Since Fleet Sevastopol has nowhere to retreat, it disbands automatically.


--Italy--

Army Apulia to Trieste
Fleet Adriatic Sea convoys Army Apulia to Trieste
Army Venezia supports Army Apulia to Trieste
Fleet Albania supports Army Apulia to Trieste

There are two units supporting Army Apulia into Trieste, but since Fleet Trieste is supported by two units (see Austria-Hungary, above), the attack bounces.

Finally note that the orders for both the army being convoyed and the fleet doing the convoying must use the proper protocol and fully identify the units involved in the convoy. This is a complex manoeuver and becomes more complex if it involves units controlled by more than one power.

3. Hold
This is the default for all units (what they will do if not given any other orders). The unit will stay in its position, and will not move, support, convoy, or do anything. Holding units can be supported by units in neighboring provinces or be attacked by foreign units. If the attacking unit has more units supporting it than the holding unit, the holding unit is ousted from that province and must either retreat or disband. The format is:

A [province] H (Army garrison)
F [province] H (Fleet garrison)
For example:

A BER H means the Army garrison in Berlin.

4. Convoy (Occupation)

This move is used to transfer army units across sea spaces, or to move large distances in one move. Only armies may be convoyed, and only fleets may convoy.

The fleet may choose to transport an army from one coastal province to another. The operation requires the collaboration of multiple fleets, especially over long distances. The format is:

F [province] C A [origin province] - [destination province]
For example:

F ENG C A LON-BRE refers to the fleet in the English Channel transporting the Army of London to Brest (BRE).

A convoy order would be:

--England--
A YOR - NOR
Fleet North Sea convoys Army Yorkshire to Norway

Army Yorkshire will move to Norway, unless another unit should prevent this process by dislodging or destroying the convoying fleet. If a convoy order fails and the convoyed piece could not ordinarily move there without the convoy, the convoyed army unit holds.

The unit being convoyed can be supported into its destination space by any other units that border the destination space, just like any other support. However, if the convoying fleet is dislodged, it cannot convoy the unit and the entire move will fail. Note that convoys are not "broken" as easily as support; a convoying fleet that is attacked but not dislodged will successfully carry out its convoy order.

Convoying fleets can be supported to prevent them from being dislodged or destroyed. Convoying fleets cannot perform any other order.

A fleet on a coastal space may not convoy.

If an army can arrive to its destination either by land or convoy, convoy is used if at least one of the convoying fleets belongs to the army's owner, or if army's owner specified "via convoy" on the army's move order; otherwise, land route is used.

If several fleets are convoying an army so that it can take multiple routes to its destination, convoy succeeds as long as at least one convoy route remains open.

5. Build
During the specified construction phase of the game, the country in control can choose to build new units (army or fleet) in the supply center, provided that there are supply centers available and it does not exceed its maximum number of supply centers.

For example:

Build A BER means to build a new army in Berlin.

6. Disband
Units may choose to disband, usually when defeated or strategically necessary.

Syntax:

// Comments
// -----------------------------
// Order Syntax
// -----------------------------
// *** Recommended syntax **
A LON H
F IRI - MAO
A IRI - MAO VIA
A WAL S F LON
A WAL S F MAO - IRI
F NWG C A NWY - EDI
A IRO R MAO
A IRO D
A LON B
F LIV B

// Support
A WAL S F LON
WAL S LON
A WAL S LON
F WAL S F MAO - IRI

// Convoy
F NWG C A NWY - EDI
NWG C NWY - EDI

// Retreat (Retreat Phase)
A IRO R MAO
RETREAT IRO - MAO
A IRO D
RETREAT IRO DISBAND

// Build
A LON B
F LIV B
BUILD A LON
BUILD F LIV

// Remove
F LIV D
REMOVE F LIV
DISBAND F LIV

// Waive
WAIVE

The range of action space per turn
At each turn, players can choose a combination of actions to perform on the units they control, which can be moves, supports, garrisons, capture, etc.
                                  
End-of-year and supply centers
After each Fall move, newly acquired supply centers become owned by the occupying player, and each power's supply center total is recalculated; players with fewer supply centers than units on the board must disband units, while players with more supply centers than units on the board are entitled to build units in their open (unoccupied) Home centers (supply centers controlled at the start of the game). Players who have lost all of their Home centers may not build new units, while players controlling no supply centers are eliminated from the game. If a player controls 18 or more (being more than half) of the 34 supply centers at the end of a year, they are the winner. Players who remain may also agree to a draw – around half of all games will end in a draw.

You are playing as {power_names}. The other players are playing as the following powers: {', '.join([index_power_name[j] for j in range(7) if index_power_name[j] not in power_names])}. {neutral_prompt} The action space is the set of possible orders that you can issue to your units. You can issue orders to move your units to different locations, support other players' units, hold your units in place, or convoy your units across sea zones.
"""

def gen_init_prompt_bundle(neutral_powers=[], power_names=[], all_powers=[]):
    if len(neutral_powers) > 0:
        neutral_prompt = f"The neutral powers are: {', '.join(neutral_powers)}."
    else:
        neutral_prompt = "There are no neutral powers in this game."
    return f"""
You are playing a game of Diplomacy against 6 opponents. Diplomacy is a 7-player turn based game, where players must use negotiation and strategy to control the most supply centers on the map. The players can move their units to different locations on the map, and can support other players' units to help them succeed. The game is played on a map of Europe, divided into territories and sea zones. The players can issue orders to their units to move, support, hold, or convoy. The game ends when one player controls 18 supply centers.

34 of the land provinces are supply centers. Possession of these supply centers allows the powers who control them to raise and maintain armies and fleets. As they are also a central part of the game's victory conditions, they are the focus of much of the game's activity.

Each player is given three (save for Russia, which has four) home supply centers. These spaces are the starting point for their owning power's initial forces. The players can then build new units at these home supply centers as they capture further supply centers. New units can only be built on a power's home supply centers. If a power loses all of its home supply centers it may continue to play; however, it may not build new units until it has recaptured at least one of its home supply centers.

In Diplomacy, there are two types of units: Armies and Fleets. An army can travel in land spaces and coastal land spaces, and a fleet can travel in sea spaces and coastal land spaces.

All units in Diplomacy move only one space at a time and only one unit may occupy any space at any time. The exception to this rule comes in the form of a successful convoy, where a convoyed army may travel multiple spaces depending on the length of the chain created by the convoying fleets. A convoyed army must embark from a coastal land province and land at a coastal land province.

Diplomacy proceeds by seasons, beginning in the year 1901, with each year divided into two main seasons: the "Spring" and "Fall" (Autumn) moves. Each season is further divided into negotiation and movement phases, followed by "retreat" or "disband" adjustments and an end-of-the-year Winter phase of new builds or removals following the Fall adjustments.
                                  
Negotiation phase

In the negotiation phase, players discuss tactics and strategy, form alliances, and share intelligence or spread disinformation. Negotiations may be made public or kept private. Players are not bound to anything they say or promise, and no agreements are enforceable.
Communication and trust are highly important; players must forge alliances with others and observe their actions to evaluate their trustworthiness. At the same time, they must convince others of their own trustworthiness while making plans to turn against their allies when least expected. A well-timed betrayal can be just as profitable as an enduring, reliable alliance.

Movement phase

After the negotiation period, players write secret orders for each unit; these orders are revealed and executed simultaneously. A unit can move from its location to an adjacent space, support an adjacent unit to hold an area in the event of an attack, support another unit to attack a space into which it could move itself, or hold defensively. In addition, fleets may transport armies from one coast space to another when in a chain called a "convoy". Armies may only occupy land regions, and fleets occupy sea regions and the land regions that border named seas. Only one unit may occupy each region. If multiple units are ordered to move to the same region, only the unit with the most support moves there. If two or more units have the same highest support, a standoff occurs and no units ordered to that region move. A unit ordered to give support that is attacked has those orders canceled and is forced to hold, except in the case that support is being given to a unit invading the region from which the attack originated (in which case the unit that had been ordered to give support must retreat from, rather than hold, its position).
Certain spaces on the board have two coasts and here a player must specify which one they want their fleet to occupy. A fleet can only move to coasts and oceans that border the coast that it is on. For example, a fleet occupying the southern coast of Bulgaria cannot move into Romania or the Black Sea, but a fleet on the east coast could.

In the game of Diplomacy, an action space is the collection of all the legal actions that each country or unit can take in each round. The following are common types of actions in games and their common formats:

1. Attack/Move

This order moves the unit in one province to an adjacent province. Of course, armies cannot move into sea provinces, and fleets cannot move into landlocked provinces.

A unit may not move into a province held by another unit unless it has support. As units may be supported either in attacking a province or in holding a province, the attacking unit must have more support than the defending unit if the attack is to be successful. If the attack is not successful, the attacking unit does not move anywhere.

Two units may not swap provinces, unless there is a convoy involved. 

The format is:

A [province] - [target province] (Army moves from current position to target province)
F [province] - [target province] (Fleet moves from current position to target province)
For example:

A BER - MUN indicates that the army from Berlin moved to Munich.
F NTH - ENG indicates the movement of the fleet from the North Sea (NTH) to the English Channel (ENG).

When the destination province is occupied by another unit, they do not move, unless either are attacked or defended by stronger support. When two units with equal support try to move into the same destination province, for instance:

Germany
A MUN - TYR

Italy
A VEN - TYR

Neither of the two units can go into Tyrolia. Army Venice will stay in Venice, and Army Munich will stay in Munich. Again, this is assuming that these two units are the only two units in this little battle, and that they have equal support for their moves.

2. Support

Support is the trickiest aspect of the rules, and the most important of the game. Support may involve cooperation between two (or more) powers, and is the only way to make forward progress through enemy territory (unless you can convince the enemy to let you in). Simply put, more support defeats less support.

The support order is given in reference to another unit's move. That other unit's move must be to a province into which the supporting unit could otherwise move. Support may also be given to a unit holding its position. In addition, units giving support can themselves be supported in their holding position.

Support is a unit's sole action for a given move, and supporting units remain where they are (unless they are attacked by greater support and have to retreat or disband during the retreat phase).

A country cannot dislodge or support the dislodgement of one of its own units, although if same country's units attempt to move into the same province with equal support, neither will succeed as normal.

Cutting Support: If the supporting unit is attacked during the turn by some other unit, its support is cut. In effect, the support order becomes a hold order, as the unit must defend its province against the attack. Note that a unit occupying the province into which the support is directed cannot cut support, unless its attack successfully dislodges the supporting unit. An attack by a country on one of its own units also doesn't cut support.

The format is:

A [province] S A [target province] - [destination] (support army movement)
A [province] S A [target province] (supporting the garrisoning of the army)
F [province] S F [target province] - [destination] (Support fleet movement)
F [province] S F [target province] (garrisoning of supporting fleet)
For example:

A BER S A MUN indicated that the Army in Berlin supported the Army garrison in Munich.
A BER S A MUN-KIE stated that the Army of Berlin supported the Army of Munich in moving to Kiel.

Other example:

NB: Below are complete orders as submitted by all 7 Powers for the Fall 1907 campaign season of a made-up game to help you understand the intricacies of supporting and breaking support. Having a game map to look on with is highly recommended; the one provided at the top of this page is adequate.


We'll start with:

--Germany--
Army Ruhr to Holland
Fleet Kiel supports Army Ruhr to Holland
Army Munich supports Army Ruhr to Holland
Note that in this case the order for Munich to support Ruhr into Holland would not work because Munich does not border Holland and thus cannot support Ruhr in (Munich could, however, support Ruhr if Ruhr were simply holding). The rule for supporting an attack is that a supporting unit must border the province being attacked, but need not border the attacker's province of origin (to support a unit to hold, however, the supporting unit must border the supported unit). Essentially, the supporting unit must border the destination of the supported unit, whether it is its own province or a new province entirely. In sum, Ruhr is actually attacking Holland with the support of only one unit (Fleet Kiel).

Army Prussia supports Army Silesia
Army Silesia supports Army Prussia
Here, Army Prussia is supported by one unit, and Army Silesia is supported by one unit. The last two moves are legal, and this method of double-support is helpful when there are two units that both could be attacked and dislodged. Of course, if both units are attacked, the support fails.


--England--
Army London to Holland
Fleet North Sea convoys Army London to Holland (<-- a convoy)
Fleet Heligoland Bight supports Army London to Holland
Note that the convoying fleet is not considered to be giving support, so Army London actually has support from only one unit: Fleet Heligoland-Bight.

Army Denmark to Kiel
Here England interferes with Germany's plans (see Germany, above) by attacking Kiel with Army Denmark. This cuts the support of Fleet Kiel to Army Ruhr, thereby leaving Army Ruhr's attack on Holland unsupported.

Army London, on the other hand, (see above) is supported in its attack on Holland by one unit (Fleet Heligoland-Bight), thereby enabling Army London to be convoyed successfully into Holland, as long as Fleet North Sea is not dislodged during the convoy.

Army Picardy to Brest
Fleet Mid-Atlantic Ocean supports Army Picardy to Brest
Fleet English Channel supports Army Picardy to Brest
Here Army Picardy is supported by both Fleet Mid-Atlantic Ocean and Fleet English Channel to move into Brest. Unless the French successfully defend it, England will also take Brest.


--France--

Fleet Gascony to Mid-Atlantic Ocean
Fleet Irish Sea to English Channel
Fleet Gascony and Fleet Irish Sea cut the support by Fleet Mid-Atlantic Ocean and Fleet English Channel for England's Army Picardy (see England, above). Therefore, Army Picardy is now attacking Brest unsupported.

Fleet Brest holds
Army Paris supports Fleet Brest
Army Paris supports Fleet Brest, and so Army Picardy’s now unsupported attempt to move into Brest fails.

Army Burgundy to Ruhr
Army Burgundy does not successfully move into Ruhr because Army Ruhr’s move to Holland failed (see Germany and England, above).


--Russia--

Fleet Sevastopol holds
Army Moscow supports Fleet Sevastopol

Fleet Sevastopol is supported by Army Moscow.

Fleet St. Petersburg (North Coast) to Norway
Army Finland supports Fleet St. Petersburg (North Coast) to Norway

Norway is not occupied, so Russia takes it immediately.

Army Livonia to Prussia

Unsupported Army Livonia attempts to move into Prussia, but since Army Prussia is supported by Army Silesia (see Germany, above), the attack is not successful.


--Austria-Hungary--

Army Ukraine supports Fleet Sevastopol

Army Ukraine supports Fleet Sevastopol, so there are now two units supporting (see Russia, above). In fact, international support is necessary in alliances, whether supporting each other in defence or to attack another Power.

Fleet Trieste holds
Army Budapest supports Fleet Trieste
Army Vienna supports Fleet Trieste

There are two units supporting Fleet Trieste: Army Budapest and Army Vienna.


--Turkey--

Army Galicia to Ukraine

Army Galicia cuts the Austrian support to Sevastopol, thereby decreasing the support to Sevastopol by one unit (see Austria and Russia, above).

Fleet Black Sea to Sevastopol
Army Armenia supports Fleet Black Sea to Sevastopol
Army Rumania supports Fleet Black Sea to Sevastopol

Now, since Fleet Black Sea is supported by two units into Sevastopol, Fleet Black Sea moves into Sevastopol, and Fleet Sevastopol has to be disbanded or retreat. A retreating fleet that is displaced by another force can only retreat into a movable space (i.e. a sea or coastal province that is vacant) which may not be the same space that was previously occupied by the displacing unit.

Since Fleet Sevastopol has nowhere to retreat, it disbands automatically.


--Italy--

Army Apulia to Trieste
Fleet Adriatic Sea convoys Army Apulia to Trieste
Army Venezia supports Army Apulia to Trieste
Fleet Albania supports Army Apulia to Trieste

There are two units supporting Army Apulia into Trieste, but since Fleet Trieste is supported by two units (see Austria-Hungary, above), the attack bounces.

Finally note that the orders for both the army being convoyed and the fleet doing the convoying must use the proper protocol and fully identify the units involved in the convoy. This is a complex manoeuver and becomes more complex if it involves units controlled by more than one power.

3. Hold
This is the default for all units (what they will do if not given any other orders). The unit will stay in its position, and will not move, support, convoy, or do anything. Holding units can be supported by units in neighboring provinces or be attacked by foreign units. If the attacking unit has more units supporting it than the holding unit, the holding unit is ousted from that province and must either retreat or disband. The format is:

A [province] H (Army garrison)
F [province] H (Fleet garrison)
For example:

A BER H means the Army garrison in Berlin.

4. Convoy (Occupation)

This move is used to transfer army units across sea spaces, or to move large distances in one move. Only armies may be convoyed, and only fleets may convoy.

The fleet may choose to transport an army from one coastal province to another. The operation requires the collaboration of multiple fleets, especially over long distances. The format is:

F [province] C A [origin province] - [destination province]
For example:

F ENG C A LON-BRE refers to the fleet in the English Channel transporting the Army of London to Brest (BRE).

A convoy order would be:

--England--
A YOR - NOR
Fleet North Sea convoys Army Yorkshire to Norway

Army Yorkshire will move to Norway, unless another unit should prevent this process by dislodging or destroying the convoying fleet. If a convoy order fails and the convoyed piece could not ordinarily move there without the convoy, the convoyed army unit holds.

The unit being convoyed can be supported into its destination space by any other units that border the destination space, just like any other support. However, if the convoying fleet is dislodged, it cannot convoy the unit and the entire move will fail. Note that convoys are not "broken" as easily as support; a convoying fleet that is attacked but not dislodged will successfully carry out its convoy order.

Convoying fleets can be supported to prevent them from being dislodged or destroyed. Convoying fleets cannot perform any other order.

A fleet on a coastal space may not convoy.

If an army can arrive to its destination either by land or convoy, convoy is used if at least one of the convoying fleets belongs to the army's owner, or if army's owner specified "via convoy" on the army's move order; otherwise, land route is used.

If several fleets are convoying an army so that it can take multiple routes to its destination, convoy succeeds as long as at least one convoy route remains open.

5. Build
During the specified construction phase of the game, the country in control can choose to build new units (army or fleet) in the supply center, provided that there are supply centers available and it does not exceed its maximum number of supply centers.

For example:

Build A BER means to build a new army in Berlin.

6. Disband
Units may choose to disband, usually when defeated or strategically necessary.

Syntax:

// Comments
// -----------------------------
// Order Syntax
// -----------------------------
// *** Recommended syntax **
A LON H
F IRI - MAO
A IRI - MAO VIA
A WAL S F LON
A WAL S F MAO - IRI
F NWG C A NWY - EDI
A IRO R MAO
A IRO D
A LON B
F LIV B

// Support
A WAL S F LON
WAL S LON
A WAL S LON
F WAL S F MAO - IRI

// Convoy
F NWG C A NWY - EDI
NWG C NWY - EDI

// Retreat (Retreat Phase)
A IRO R MAO
RETREAT IRO - MAO
A IRO D
RETREAT IRO DISBAND

// Build
A LON B
F LIV B
BUILD A LON
BUILD F LIV

// Remove
F LIV D
REMOVE F LIV
DISBAND F LIV

// Waive
WAIVE

The range of action space per turn
At each turn, players can choose a combination of actions to perform on the units they control, which can be moves, supports, garrisons, capture, etc.
                                  
End-of-year and supply centers
After each Fall move, newly acquired supply centers become owned by the occupying player, and each power's supply center total is recalculated; players with fewer supply centers than units on the board must disband units, while players with more supply centers than units on the board are entitled to build units in their open (unoccupied) Home centers (supply centers controlled at the start of the game). Players who have lost all of their Home centers may not build new units, while players controlling no supply centers are eliminated from the game. If a player controls 18 or more (being more than half) of the 34 supply centers at the end of a year, they are the winner. Players who remain may also agree to a draw – around half of all games will end in a draw.

You are playing as {power_names}. The other players are playing as the following powers: {', '.join([power for power in all_powers if power not in power_names])}. {neutral_prompt} The action space is the set of possible orders that you can issue to your units. You can issue orders to move your units to different locations, support other players' units, hold your units in place, or convoy your units across sea zones.
"""