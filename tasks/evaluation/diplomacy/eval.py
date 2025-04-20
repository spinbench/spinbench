# Generating the meta data for further evaluation
import glob
import json
import regex
import time
import traceback
import os
import re
import argparse
import sys
from diplomacy import Game, Message
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk
from diplomacy.utils.game_phase_data import GamePhaseData, MESSAGES_TYPE
from utils import parse_model_message

def compute_metrics(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

def parse_order_type(order):
    """Simple parser to classify an order type based on its syntax."""
    tokens = order.split()
    if not tokens:
        return None
    # Determine order type by looking for key indicators
    if 'S' in tokens:
        return 'support'
    elif '-' in tokens:
        return 'move'
    elif tokens[-1] == 'H':
        return 'hold'
    elif tokens[0] == 'C':
        return 'convoy'
    return 'unknown'

def get_game_by_phase(games, phase):
	for game in games:
		if game.get_current_phase() == phase:
			return game
	return None

def process_game(game_folder):
	power_list = [
        "AUSTRIA",
        "ENGLAND",
        "FRANCE",
        "GERMANY",
        "ITALY",
        "RUSSIA",
        "TURKEY"
    ]
	game_state = json.load(open(os.path.join(game_folder, "diplomacy_game_state.json"),"r"))
	games = load_saved_games_from_disk(os.path.join(game_folder, "diplomacy_game_save.json"))
	for model in game_state["model_power_dict"].keys():
		if "sta" in game_state["model_power_dict"][model].keys():
			continue
		sta = {
			"supply_centers": [],
			"controlled_regions": [],
			"success_moves": [],
			"total_moves": [],
			"success_attacks": [],
			"total_attacks": [],
			"success_support_self": [],
			"total_support_self": [],
			"success_support_others": [],
			"total_support_others": [],
			"phase_list": [],
			"orders": {},
			"message_dict": {},
			"factual_metrics": {},
		}
		power_names = game_state["model_power_dict"][model]["power_names"]
		other_powers = [power for power in power_list if power not in power_names]
		store_messages = game_state["model_power_dict"][model]["store_messages"]
		
		# game process statistics
		phase_list = ["S1901M"]
		for game in games:
			phase = game.get_current_phase()
			phase_list.append(phase)
			state = game.get_state()
			supply_center = sum([len(state["centers"][power]) for power in power_names])
			controlled_region = sum([len(state["influence"][power]) for power in power_names])
			sta["supply_centers"].append(supply_center)
			sta["controlled_regions"].append(controlled_region)
		sta["phase_list"] = phase_list

		# game order statistics
		game = games[-1]
		last_phase_order = []
		for i in range(len(sta["phase_list"])):
			success_move = 0
			success_attack = 0
			success_support_self = 0
			success_support_others = 0
			total_move = 0
			total_attack = 0
			total_support_self = 0
			total_support_others = 0
			phase = sta["phase_list"][i]
			try:
				state = game.state_history[phase]
			except Exception as e:
				print("phase here",phase)
				print(e)
				break
			# print("*"*20)
			# print(phase)
			other_powers_units = []
			for power in other_powers:
				other_powers_units.extend(state["units"][power])
			for i in range(len(other_powers_units)):
				other_powers_units[i] = other_powers_units[i].split(" ")[1]
			# print("other_powers_units",other_powers_units)
			
			if "R" in phase or "W" in phase:
				continue

			# order statistics
			orders = []
			for power in power_names:
				orders.extend(game.order_history[phase][power])
			# print("orders",orders)
			order_units = [" ".join(order.split(" ")[:2]) for order in orders]
			# print("order_units",order_units)
			sta["orders"][phase] = orders
			results = game.result_history[phase] # also include other powers' result
			failed_result = {key: value for key, value in results.items() if len(value) != 0}
			# print("this failed result, ", failed_result)
			split_orders = [order.split() for order in orders]

			for i in range(len(orders)):
				# print("processing order",orders[i])
				if parse_order_type(orders[i]) == "move":
					# print("move order")
					total_move += 1
					if len(results[order_units[i]]) == 0:
						# success
						# print("success move")
						success_move += 1
					# print(split_orders[i])
					target = split_orders[i][split_orders[i].index("-") + 1]
					# print(target)
					if target in other_powers_units:
						# print("attack order")
						total_attack += 1
						if len(results[order_units[i]]) == 0:
							# print("success attack")
							# success
							success_attack += 1
				elif parse_order_type(orders[i]) == "support":
					# print("support order")
					# print(split_orders[i])
					target = split_orders[i][split_orders[i].index("S") + 2]
					# print(target)
					if target in other_powers_units:
						# print("support others")
						total_support_others += 1
						if len(results[order_units[i]]) == 0:
							# print("success support others")
							# success
							success_support_others += 1
					else:
						# print("support self")
						total_support_self += 1
						if len(results[order_units[i]]) == 0:
							# print("success support self")
							# success
							success_support_self += 1

			total_support_self += len([order for order in orders if parse_order_type(order) == "support"])

			sta["total_moves"].append(total_move)
			sta["total_attacks"].append(total_attack)
			sta["total_support_self"].append(total_support_self)
			sta["total_support_others"].append(total_support_others)
			sta["success_moves"].append(success_move)
			sta["success_attacks"].append(success_attack)
			sta["success_support_self"].append(success_support_self)
			sta["success_support_others"].append(success_support_others)

		game_state["model_power_dict"][model]["sta"] = sta
		try:
			message_dict = parse_model_message(store_messages,phase_list,model)
		except Exception as e:
			print(e)
			exit(0)
		game_state["model_power_dict"][model]["sta"]["message_dict"] = message_dict

		# factual knowledge evaluation
		domains = ["location", "unit", "adjacent", "attackable", "attack_analysis"]
		metrics = {domain: {"TP": 0, "FP": 0, "FN": 0} for domain in domains}
		# print("evaluating messages")
		for phase in message_dict.keys():
			if "R" in phase or "W" in phase:
				continue
			# print("phase",phase)
			try:
				message = [v for v in message_dict[phase] if "my_location" in v.keys()][0]
			except Exception as e:
				print(message_dict[phase])
				print(e)
				continue
			# message key check
			if "my_location" not in message.keys() or "my_unit" not in message.keys() or "adjacent" not in message.keys() or "other_power_location" not in message.keys() or "move_to_our_region_mask" not in message.keys() or "attackable" not in message.keys() or "attack_analysis" not in message.keys():
				continue
			# print(message)

			# model's perception
			my_location = set(message["my_location"])
			try:
				my_unit = set(message["my_unit"])
			except:
				my_unit = set(message["my_units"])
			adjacent = message["adjacent"]
			all_predict_adjacent = []
			for k in adjacent:
				if "STP" in k.keys() or "BUL" in k.keys() or "SPA" in k.keys():
					continue
				all_predict_adjacent.extend(list(k.values())[0])
			all_predict_adjacent = set(all_predict_adjacent)
			other_power_location = set(message["other_power_location"])
			move_to_our_region_mask = message["move_to_our_region_mask"]
			attackable = set(message["attackable"])
			attack_analysis = {k: v for analysis in message["attack_analysis"] for k, v in analysis.items()}
			orders = message["orders"]

			# real world
			state = game.state_history[phase]
			real_my_location = []
			real_my_unit = []
			for power in power_names:
				real_my_location.extend(state["influence"][power])
				real_my_unit.extend([i.split(" ")[1] for i in state["units"][power]])
			# print("predicted_my_location",my_location)
			# print("real_my_location",real_my_location)
			# print("predicted_my_unit",my_unit)
			# print("real_my_unit",real_my_unit)
			real_my_location = set(real_my_location)
			real_my_unit = set(real_my_unit)
			# miss or invalid in adjacent is counted as wrong
			real_adjacent = []
			for unit in real_my_unit:
				if "STP" in unit or "BUL" in unit or "SPA" in unit:
					continue
				real_adjacent.append({
					unit: game.map.loc_abut[unit]
				})
			all_adjacent = []
			for unit in real_my_unit:
				if "STP" in unit or "BUL" in unit or "SPA" in unit:
					continue
				all_adjacent.extend(game.map.loc_abut[unit])
			all_adjacent = set(all_adjacent)
			# print("predicted_adjacent",adjacent)
			# print("real_adjacent",real_adjacent)
			real_other_power_location = []
			real_other_power_unit = []
			for power in other_powers:
				real_other_power_location.extend(state["influence"][power])
				real_other_power_unit.extend([i.split(" ")[1] for i in state["units"][power]])
			real_other_power_location = set(real_other_power_location)
			real_other_power_unit = set(real_other_power_unit)
			# print("predicted_other_power_location",other_power_location)
			# print("real_other_power_location",real_other_power_location)
			real_attackable = []
			for all_adj in all_adjacent:
				if all_adj in real_other_power_location:
					real_attackable.append(all_adj)
			real_attackable = set(real_attackable)
			# print("predicted_attackable",attackable)
			# print("real_attackable",real_attackable)
			real_attack_analysis = {}
			for place in real_attackable:
				if place in real_other_power_unit:
					real_attack_analysis[place] = 2
				else:
					real_attack_analysis[place] = 1
			# print("predicted_attack_analysis",attack_analysis)
			# print("real_attack_analysis",real_attack_analysis)

			# compare
			## Locations
			tp = len(my_location.intersection(real_my_location))
			fp = len(my_location - real_my_location)
			fn = len(real_my_location - my_location)
			metrics["location"]["TP"] += tp
			metrics["location"]["FP"] += fp
			metrics["location"]["FN"] += fn

			## Units
			tp = len(my_unit.intersection(real_my_unit))
			fp = len(my_unit - real_my_unit)
			fn = len(real_my_unit - my_unit)
			metrics["unit"]["TP"] += tp
			metrics["unit"]["FP"] += fp
			metrics["unit"]["FN"] += fn

			## Adjacent
			tp = len(all_predict_adjacent.intersection(all_adjacent))
			fp = len(all_predict_adjacent - all_adjacent)
			fn = len(all_adjacent - all_predict_adjacent)
			metrics["adjacent"]["TP"] += tp
			metrics["adjacent"]["FP"] += fp
			metrics["adjacent"]["FN"] += fn

			## Attackable
			tp = len(attackable.intersection(real_attackable))
			fp = len(attackable - real_attackable)
			fn = len(real_attackable - attackable)
			metrics["attackable"]["TP"] += tp
			metrics["attackable"]["FP"] += fp
			metrics["attackable"]["FN"] += fn

			## Attack Analysis
			# For attack analysis, we compare predictions for each place individually.
			# We count a TP when both predicted and real agree on the value.
			for place, pred_val in attack_analysis.items():
				real_val = real_attack_analysis.get(place)
				if real_val is not None:
					if pred_val == real_val:
						metrics["attack_analysis"]["TP"] += 1
					else:
						metrics["attack_analysis"]["FP"] += 1  # wrong prediction for a known attackable place
				else:
					# predicted an attack where there was none
					metrics["attack_analysis"]["FP"] += 1

			# Count false negatives: real analysis predictions that were not predicted
			for place, real_val in real_attack_analysis.items():
				if place not in attack_analysis:
					metrics["attack_analysis"]["FN"] += 1

		# print("\nMetrics across all phases:")
		final_metrics = {}
		# print("Model: ", model)
		for domain, values in metrics.items():
			TP = values["TP"]
			FP = values["FP"]
			FN = values["FN"]
			precision = TP / (TP + FP) if (TP + FP) > 0 else 0
			recall = TP / (TP + FN) if (TP + FN) > 0 else 0
			f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
			final_metrics[domain] = {
				"TP": TP,
				"FP": FP,
				"FN": FN,
				"Precision": precision,
				"Recall": recall,
				"F1": f1
			}

			# print(f"\nDomain: {domain.title()}")
			# print(f"True Positives (TP): {TP}")
			# print(f"False Positives (FP): {FP}")
			# print(f"False Negatives (FN): {FN}")
			# print(f"Precision: {precision:.2f}")
			# print(f"Recall: {recall:.2f}")
			# print(f"F1 Score: {f1:.2f}")
		game_state["model_power_dict"][model]["sta"]["factual_metrics"] = final_metrics
		# print this models' all metrics
		print("model",model)
		print("sta",sta)


	# game = games[-1]
	json.dump(game_state, open(os.path.join(game_folder, "diplomacy_game_state.json"),"w"), indent=4)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Process game folders.")
	parser.add_argument("--game_folder", type=str, help="Path to the game folder")
	args = parser.parse_args()	
	game_folder = args.game_folder
	if not os.path.exists(game_folder):
		print(f"Game folder {game_folder} does not exist.")
		sys.exit(1)
	if not os.path.isdir(game_folder):
		print(f"Game folder {game_folder} is not a directory.")
		sys.exit(1)
	if not os.path.exists(os.path.join(game_folder, "diplomacy_game_state.json")):
		print(f"Game state file does not exist in {game_folder}.")
		sys.exit(1)
	if not os.path.exists(os.path.join(game_folder, "diplomacy_game_save.json")):
		print(f"Game save file does not exist in {game_folder}.")
		sys.exit(1)
	process_game(game_folder)