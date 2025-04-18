import json
from typing import List, Dict
from datetime import datetime

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