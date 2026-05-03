import csv
import random

def generate_player_data(filename="synthetic_player_data.csv", num_samples=5000):
    """
    Generates synthetic slot machine player sessions and saves them to a CSV.
    Features: consecutive_losses, balance_ratio, avg_bet_size
    Target: churn (1 = quit, 0 = kept playing)
    """
    print(f"Generating {num_samples} synthetic player records...")
    
    # Define the CSV headers
    headers = ["consecutive_losses", "balance_ratio", "avg_bet_size", "churn"]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        churn_count = 0
        
        for _ in range(num_samples):
            # 1. Generate random feature ranges
            cons_losses = random.randint(0, 10)
            bal_ratio = round(random.uniform(0.1, 2.0), 2)  # Current balance / starting balance
            avg_bet = round(random.uniform(1.0, 100.0), 2)
            
            # 2. Calculate the Churn Score (The "hidden" logic the ML model has to learn)
            # Players with high losses and low balance ratio are more likely to churn.
            churn_score = (cons_losses * 0.4) + ((1.0 - bal_ratio) * 5)
            
            # Add some randomness (noise) so the data isn't perfectly linear
            churn_score += random.uniform(-2.0, 2.0)
            
            # 3. Assign the target label
            churn_label = 1 if churn_score > 3.5 else 0
            
            if churn_label == 1:
                churn_count += 1
                
            # 4. Write row to CSV
            writer.writerow([cons_losses, bal_ratio, avg_bet, churn_label])
            
    print(f"Dataset saved to '{filename}'.")
    print(f"Total Churned Players: {churn_count} ({(churn_count/num_samples)*100:.1f}%)")

if __name__ == "__main__":
    generate_player_data()