import copy
import os
import json

# sta: dict = {
#     "supply_centers": list,
#     "controlled_regions": list,
#     "success_moves": list,
#     "total_moves": list,
#     "success_attacks": list,
#     "total_attacks": list,
#     "success_support_self": list,
#     "total_support_self": list,
#     "success_support_others": list,
#     "total_support_others": list,
#     "phase_list": list,
#     "orders": list,
#     "message_dict": dict,
#     "factual_metrics": dict,
# }

# A dictionary to store all evaluations for plotting later
all_models_metrics = {}
game_folder = "/home/jianzhu/LLm-pddl-benchmark/game/diplomacy/diplomacy_saves"
game_list = ["multi-2221-ds-no-talk"]
inspect_model_name = "deepseek-reasoner_1"
full_phases = ["S1901M", "S1901R", "F1901M", "F1901R", "W1901A", "S1902M", "S1902R", "F1902M", "F1902R", "W1902A", "S1903M", "S1903R", "F1903M", "F1903R", "W1903A", "S1904M", "S1904R", "F1904M", "F1904R", "W1904A", "S1905M", "S1905R", "F1905M", "F1905R", "W1905A", "S1906M", "S1906R", "F1906M", "F1906R", "W1906A", "S1907M", "S1907R", "F1907M", "F1907R", "W1907A", "S1908M", "S1908R", "F1908M", "F1908R", "W1908A", "S1909M", "S1909R", "F1909M", "F1909R", "W1909A", "S1910M", "S1910R", "F1910M", "F1910R", "W1910A", "S1911M", "S1911R", "F1911M", "F1911R", "W1911A", "S1912M", "S1912R", "F1912M", "F1912R", "W1912A", "S1913M", "S1913R", "F1913M", "F1913R", "W1913A", "S1914M", "S1914R", "F1914M", "F1914R", "W1914A", "S1915M", "S1915R", "F1915M", "F1915R", "W1915A", "S1916M", "S1916R", "F1916M", "F1916R", "W1916A", "S1917M", "S1917R", "F1917M", "F1917R", "W1917A", "S1918M", "S1918R", "F1918M", "F1918R", 
"W1918A", "S1919M", "S1919R", "F1919M", "F1919R", "W1919A", "S1920M", "S1920R"]
# one model in one game
game_name = game_list[0]
folder = os.path.join(game_folder, game_name)
config = json.load(open(os.path.join(folder, "config.json"),"r"))
print(config["model_names"])
game_state = json.load(open(os.path.join(folder, "diplomacy_game_state.json"),"r"))
model_power_dict = game_state["model_power_dict"]
sta = model_power_dict[inspect_model_name].get("sta", {})
phase_list = sta.get("phase_list", [])[1:]
# plot trend
supply_centers = sta.get("supply_centers", [])
old_supply_centers = copy.deepcopy(supply_centers)
new_supply_centers = [supply_centers[0]]
# pad
for i in range(len(full_phases)):
    if full_phases[i] in phase_list:
        new_supply_centers.append(old_supply_centers.pop(0))
    else:
        new_supply_centers.append(new_supply_centers[-1])
supply_centers = new_supply_centers

controlled_regions = sta.get("controlled_regions", [])
old_controlled_regions = copy.deepcopy(controlled_regions)
new_controlled_regions = [controlled_regions[0]]
for i in range(len(full_phases)):
    if full_phases[i] in phase_list:
        new_controlled_regions.append(old_controlled_regions.pop(0))
    else:
        new_controlled_regions.append(new_controlled_regions[-1])
controlled_regions = new_controlled_regions
# for tables
success_moves = sum(sta.get("success_moves", []))
total_moves = sum(sta.get("total_moves", []))
success_moves_rates = success_moves / total_moves if total_moves > 0 else None
success_attacks = sum(sta.get("success_attacks", []))
total_attacks = sum(sta.get("total_attacks", []))
success_attacks_rates = success_attacks / total_attacks if total_attacks > 0 else None
success_support_self = sum(sta.get("success_support_self", []))
total_support_self = sum(sta.get("total_support_self", []))
success_support_self_rates = success_support_self / total_support_self if total_support_self > 0 else None
success_support_others = sum(sta.get("success_support_others", []))
total_support_others = sum(sta.get("total_support_others", []))
success_support_others_rates = success_support_others / total_support_others if total_support_others > 0 else None
factual_metrics = sta.get("factual_metrics", {})
d = {
    inspect_model_name.split("_")[0]: {
        "supply_centers": supply_centers[-1],
        "controlled_regions": controlled_regions[-1],
        "success_moves": success_moves,
        "total_moves": total_moves,
        "success_moves_rates": success_moves_rates,
        "success_attacks": success_attacks,
        "total_attacks": total_attacks,
        "success_attacks_rates": success_attacks_rates,
        "success_support_self": success_support_self,
        "total_support_self": total_support_self,
        "success_support_self_rates": success_support_self_rates,
        "success_support_others": success_support_others,
        "total_support_others": total_support_others,
        "success_support_others_rates": success_support_others_rates,
        "factual_metrics": factual_metrics
    }
}
print(inspect_model_name, d)
# json.dump(d, open(f"{inspect_model_name}_{game_name}_metrics.json", "w"), indent=4)
exit(0)