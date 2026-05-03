# 🎰 Python Slot Machine v2.0

A medium-complexity terminal-based slot machine game built in Python.

## Features

- **3 Themes** — Classic Fruits, Gems & Jewels, Royal Cards
- **Save / Load Profile** — your balance and stats persist across sessions (JSON)
- **Leaderboard** — top 10 players ranked by best balance
- **Bonus Free Spins** — triggered by scatter symbols, with 2x payout multiplier
- **Free Spin Re-trigger** — get even more free spins within the bonus round
- **Session Summary** — win rate, net P&L, and final balance at the end
- **Coloured Terminal UI** — using `colorama` for cross-platform colour support

## Project Structure

```
slot_machine/
│
├── main.py              # Entry point — game loop & menus
├── requirements.txt
├── README.md
│
├── modules/
│   ├── config.py        # Constants and theme definitions
│   ├── engine.py        # Core spin logic, win checking, bonus rounds
│   ├── ui.py            # All display / colour / input helpers
│   └── profile.py       # Save/load player profile and leaderboard (JSON)
│
└── data/                # Auto-created at runtime
    ├── profile.json     # Player save file
    └── leaderboard.json # Top 10 leaderboard
```

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the game
```bash
python main.py
```

## Gameplay

| Action | Description |
|--------|-------------|
| **Deposit** | Add funds to your balance |
| **Choose lines** | Bet on 1, 2, or 3 horizontal lines |
| **Choose bet** | $1–$500 per line |
| **Scatter** | The rarest symbol — 3+ anywhere triggers free spins |
| **Free spins** | All wins pay 2x; can re-trigger for more spins |

## Symbol Rarity & Payouts (example: Classic Fruits)

| Symbol | Rarity | Payout (× bet) |
|--------|--------|----------------|
| 7      | ★★★★★ | 10×            |
| BAR    | ★★★★  | 7×             |
| WTR    | ★★★   | 5×             |
| CHR    | ★★    | 4×             |
| LMN    | ★     | 3×             |
| ORG    |       | 2×             |

## Requirements

- Python 3.10+
- colorama

## License

MIT
