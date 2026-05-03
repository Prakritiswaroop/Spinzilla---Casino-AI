#!/usr/bin/env python3
# =============================================================================
#  main.py  —  Entry point for Python Slot Machine v2.0 (ML Edition)
#
#  ML Feature Added:
#  • AI Casino Manager: Trains a Random Forest Classifier on synthetic 
#    player data to predict "Churn" (when a player is about to quit). 
#    If the churn probability crosses a threshold, the AI intervenes.
# =============================================================================

import sys
import os
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Make sure sibling modules are importable when running from project root
sys.path.insert(0, os.path.dirname(__file__))

from modules import config, ui, engine, profile as profile_mod

# ---------------------------------------------------------------------------
# Machine Learning: AI Casino Manager (Churn Prediction)
# ---------------------------------------------------------------------------
def train_ai_manager():
    """
    Trains a predictive model on synthetic player session data.
    Features: [consecutive_losses, balance_ratio, avg_bet_size]
    Target: 1 (Player Quit) or 0 (Player Kept Playing)
    """
    print(ui.cyan("  [System] AI Casino Manager is training on past player data..."))
    
    X_train = []
    y_train = []
    
    # Generate synthetic training data for the portfolio
    for _ in range(2000):
        # Simulated features
        cons_losses = random.randint(0, 10)
        bal_ratio = random.uniform(0.1, 2.0) # Current balance / starting balance
        avg_bet = random.uniform(1, 100)
        
        # Rule of thumb for our synthetic target:
        # High losses + low balance ratio = high chance of quitting
        churn_score = (cons_losses * 0.4) + ((1.0 - bal_ratio) * 5)
        
        # Add some noise
        churn_score += random.uniform(-2, 2)
        
        quit_label = 1 if churn_score > 3.5 else 0
        
        X_train.append([cons_losses, bal_ratio, avg_bet])
        y_train.append(quit_label)

    # Train a Random Forest Classifier
    model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    print(ui.green("  [System] AI Model Trained! Accuracy ready for session.\n"))
    return model

def predict_churn(model, consecutive_losses, current_balance, start_balance, avg_bet):
    """Returns the probability (0.0 to 1.0) that the player will quit."""
    bal_ratio = current_balance / start_balance if start_balance > 0 else 1.0
    features = np.array([[consecutive_losses, bal_ratio, avg_bet]])
    
    # predict_proba returns [[prob_0, prob_1]]
    churn_probability = model.predict_proba(features)[0][1]
    return churn_probability


# ---------------------------------------------------------------------------
# Profile setup (new player or returning player)
# ---------------------------------------------------------------------------
def setup_profile():
    existing = profile_mod.load_profile()

    if existing:
        ui.print_section("WELCOME BACK")
        print(f"  Saved profile found: {ui.bold(existing['name'])}")
        print(f"  Balance: {ui.green('$' + str(existing['balance']))}")
        print()
        use_existing = ui.ask_yn("Load your saved profile?")
        if use_existing:
            return existing

    # New profile
    print()
    print(ui.bold("  Let's set up your profile."))
    name    = ui.ask_str("Enter your name (max 16 chars): ", max_len=16)
    deposit = ui.ask_int("Initial deposit amount ($1-$10000): ", 1, 10000)

    p = profile_mod.default_profile(name)
    p["balance"] = deposit
    profile_mod.save_profile(p)
    print(ui.green("  Profile created! Good luck, " + name + "!"))
    return p


# ---------------------------------------------------------------------------
# Theme selection
# ---------------------------------------------------------------------------
def choose_theme(current_key="1"):
    ui.print_theme_menu(config.THEMES)
    key = input(ui.bold("  > Choose theme [1/2/3] (Enter to keep current): ")).strip()
    if key in config.THEMES:
        return key
    return current_key


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------
def main_menu(profile):
    ui.print_section("MAIN MENU")
    print("  [1] Play")
    print("  [2] Change Theme")
    print("  [3] View Profile")
    print("  [4] Leaderboard")
    print("  [5] Deposit More Funds")
    print("  [6] Quit")
    print()
    choice = input(ui.bold("  > Choose an option: ")).strip()
    return choice


# ---------------------------------------------------------------------------
# Deposit
# ---------------------------------------------------------------------------
def do_deposit(profile):
    amount = ui.ask_int("How much would you like to deposit? $", 1, 100_000)
    profile["balance"] += amount
    profile_mod.save_profile(profile)
    print(ui.green("  Deposited $" + str(amount) +
                   ". New balance: $" + str(profile["balance"])))


# ---------------------------------------------------------------------------
# Single spin (normal)
# ---------------------------------------------------------------------------
def do_spin(profile, theme_key):
    theme   = config.THEMES[theme_key]
    balance = profile["balance"]

    ui.print_section("SPIN — " + theme["name"])

    # ── Bet selection ────────────────────────────────────────────────────────
    lines = ui.ask_int(
        "Lines to bet on (1-" + str(config.MAX_LINES) + "): ",
        1, config.MAX_LINES
    )

    while True:
        bet       = ui.ask_int("Bet per line ($1-$" + str(config.MAX_BET) + "): $", 1, config.MAX_BET)
        total_bet = bet * lines
        if total_bet > balance:
            print(ui.red("  Not enough balance! "
                         "Balance=$" + str(balance) +
                         ", Total bet=$" + str(total_bet)))
        else:
            break

    print()
    print("  Betting " + ui.bold("$" + str(bet)) +
          " on " + ui.bold(str(lines)) + " line(s). " +
          "Total bet: " + ui.bold("$" + str(total_bet)))

    input(ui.bold("  > Press Enter to spin..."))

    # ── Spin the reels ───────────────────────────────────────────────────────
    reels                = engine.spin_reels(config.ROWS, config.COLS, theme["symbols"])
    winnings, win_lines  = engine.check_winnings(reels, lines, bet, theme["values"])

    ui.print_slot_machine(reels, win_lines)

    if win_lines:
        ui.print_win(winnings, win_lines)
    else:
        ui.print_loss()

    net = winnings - total_bet
    ui.print_net(net)

    profile["balance"] += net
    profile_mod.update_profile_stats(profile, net)

    # ── Bonus trigger check ──────────────────────────────────────────────────
    triggered, free_spins = engine.check_bonus_trigger(reels, theme["scatter"])
    if triggered:
        ui.print_free_spin_trigger(free_spins)
        bonus_total = engine.run_free_spins(
            free_spins, lines, bet, theme,
            ui.print_slot_machine, ui
        )
        profile["balance"]          += bonus_total
        profile["total_free_spins"] += free_spins
        print()
        print(ui.magenta("  ★ Bonus round over! Total bonus won: $" + str(bonus_total)))

    profile_mod.save_profile(profile)
    return net, total_bet


# ---------------------------------------------------------------------------
# Session summary
# ---------------------------------------------------------------------------
def print_session_summary(profile, session_spins, session_wins, session_net):
    ui.print_section("SESSION SUMMARY")
    print("  Spins this session : " + str(session_spins))
    print("  Wins  this session : " + str(session_wins))
    if session_spins:
        pct = session_wins / session_spins * 100
        print("  Win rate           : " + str(round(pct, 1)) + "%")
    col = ui.green if session_net >= 0 else ui.red
    print("  Net P&L            : " + col(("+" if session_net >= 0 else "") + str(session_net)))
    print("  Final balance      : " + ui.bold("$" + str(profile["balance"])))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    ui.print_welcome()
    
    # Initialize ML Model
    churn_model = train_ai_manager()

    profile = setup_profile()

    # Restore last used theme or default to "1"
    theme_key = profile.get("theme", "1")

    # Session stats for ML tracking
    start_balance = profile["balance"]
    session_spins = 0
    session_wins  = 0
    session_net   = 0
    consecutive_losses = 0
    total_wagered = 0

    while True:
        # Show balance reminder
        print()
        print("  Balance: " + ui.green("$" + str(profile["balance"])) +
              "   |   Theme: " + ui.cyan(config.THEMES[theme_key]["name"]))

        choice = main_menu(profile)

        if choice == "1":
            # ── Play ─────────────────────────────────────────────────────────
            if profile["balance"] <= 0:
                print(ui.red("  You have no balance! Please deposit funds."))
                do_deposit(profile)
                start_balance = profile["balance"] # Reset start balance after deposit
                continue

            net, bet_size = do_spin(profile, theme_key)
            
            # Update ML Tracking variables
            session_spins += 1
            session_net   += net
            total_wagered += bet_size
            avg_bet_size = total_wagered / session_spins
            
            if net > 0:
                session_wins += 1
                consecutive_losses = 0
            else:
                consecutive_losses += 1
                
            # ── AI Casino Manager Intervention ──────────────────────────────
            churn_risk = predict_churn(
                churn_model, 
                consecutive_losses, 
                profile["balance"], 
                start_balance, 
                avg_bet_size
            )
            
            # If the AI thinks there's a > 75% chance you quit, it intervenes!
            if churn_risk > 0.75 and profile["balance"] > 0:
                print(ui.magenta("\n  [AI MANAGER] Alert! Churn probability detected at " + str(round(churn_risk*100, 1)) + "%"))
                print(ui.magenta("  [AI MANAGER] Applying retention strategy..."))
                print(ui.bold("  🎁 The Casino Manager noticed your bad streak and awarded you $25 free play!"))
                
                profile["balance"] += 25
                consecutive_losses = 0 # Reset so it doesn't spam the player
                profile_mod.save_profile(profile)

        elif choice == "2":
            # ── Change theme ─────────────────────────────────────────────────
            theme_key        = choose_theme(theme_key)
            profile["theme"] = theme_key
            profile_mod.save_profile(profile)
            print(ui.cyan("  Theme set to: " + config.THEMES[theme_key]["name"]))

        elif choice == "3":
            # ── Profile ──────────────────────────────────────────────────────
            ui.print_profile(profile)

        elif choice == "4":
            # ── Leaderboard ──────────────────────────────────────────────────
            entries = profile_mod.load_leaderboard()
            ui.print_leaderboard(entries)

        elif choice == "5":
            # ── Deposit ──────────────────────────────────────────────────────
            do_deposit(profile)
            start_balance = profile["balance"] # Reset for ML calculation

        elif choice == "6":
            # ── Quit ─────────────────────────────────────────────────────────
            print_session_summary(profile, session_spins, session_wins, session_net)
            profile_mod.update_leaderboard(profile)
            print()
            print(ui.bold("  Thanks for playing, " + profile["name"] + "! See you next time."))
            print()
            break

        else:
            print(ui.red("  Invalid choice. Please enter 1-6."))


if __name__ == "__main__":
    main()
