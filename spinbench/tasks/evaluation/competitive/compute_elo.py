import csv
from tqdm import tqdm
import argparse

def compute_elo(filename):
    player_ratings_elo = {}
    matches = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            model1 = row['Model 1']
            model2 = row['Model 2']
            wins1 = int(row['Wins (Model 1)'])
            wins2 = int(row['Wins (Model 2)'])
            draws = int(row.get('Draws', 0)) 
            matches.append((model1, model2, wins1, wins2, draws))

            if model1 not in player_ratings_elo:
                player_ratings_elo[model1] = 1000
            if model2 not in player_ratings_elo:
                player_ratings_elo[model2] = 1000

    def elo_expected(rating1, rating2):
        return 1 / (1 + 10 ** ((rating2 - rating1) / 400))

    def elo_update(rating, expected, actual, k=32):
        return rating + k * (actual - expected)

    # Iterative Elo Rating Updates
    num_iterations = 1000  # Number of iterations for stability

    for iteration in tqdm(range(num_iterations)):
        for model1, model2, wins1, wins2, draws in matches:
            rating1 = player_ratings_elo[model1]
            rating2 = player_ratings_elo[model2]
            total_games = wins1 + wins2 + draws

            expected_score1 = elo_expected(rating1, rating2) * total_games
            expected_score2 = elo_expected(rating2, rating1) * total_games

            actual_score1 = wins1 + 0.5 * draws
            actual_score2 = wins2 + 0.5 * draws

            player_ratings_elo[model1] = elo_update(rating1, expected_score1, actual_score1)
            player_ratings_elo[model2] = elo_update(rating2, expected_score2, actual_score2)
    return player_ratings_elo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Elo ratings from win statistics.")
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file with win statistics.')
    args = parser.parse_args()
    
    input_csv = args.input
    print("Elo Ratings:")
    player_ratings_elo = compute_elo(input_csv)
    for model, rating in sorted(player_ratings_elo.items(), key=lambda x: x[1], reverse=True):
        print(f"{model}: {rating:.2f}")