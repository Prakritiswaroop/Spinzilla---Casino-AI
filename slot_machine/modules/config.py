# =============================================================================
#  config.py  —  All game constants and theme definitions
# =============================================================================

MAX_LINES = 3
MAX_BET   = 500
MIN_BET   = 1
ROWS      = 3
COLS      = 3

STARTING_BALANCE = 0          # players deposit on first run
FREE_SPIN_TRIGGER = 3         # how many scatters trigger free spins
BONUS_MULTIPLIER  = 2         # free-spin winnings multiplier

DATA_DIR          = "data"
PROFILE_FILE      = "data/profile.json"
LEADERBOARD_FILE  = "data/leaderboard.json"
MAX_LEADERBOARD   = 10

# =============================================================================
#  THEMES
#  Each theme has:
#    symbols  : dict  symbol -> count in the reel pool (lower = rarer)
#    values   : dict  symbol -> payout multiplier
#    scatter  : str   symbol that triggers free spins
#    display  : dict  symbol -> coloured display string (built at runtime)
# =============================================================================

THEMES = {
    "1": {
        "name": "Classic Fruits",
        "symbols": {
            "7":  1,
            "BAR":2,
            "WTR":3,   # Watermelon
            "CHR":4,   # Cherry
            "LMN":5,   # Lemon
            "ORG":6,   # Orange
        },
        "values": {
            "7":  10,
            "BAR": 7,
            "WTR": 5,
            "CHR": 4,
            "LMN": 3,
            "ORG": 2,
        },
        "scatter": "7",
        "emojis": {
            "7":   "  7  ",
            "BAR": " BAR ",
            "WTR": " WTR ",
            "CHR": " CHR ",
            "LMN": " LMN ",
            "ORG": " ORG ",
        },
    },
    "2": {
        "name": "Gems & Jewels",
        "symbols": {
            "DIA": 1,   # Diamond
            "RUB": 2,   # Ruby
            "EMR": 3,   # Emerald
            "SPH": 4,   # Sapphire
            "AMT": 5,   # Amethyst
            "OPL": 6,   # Opal
        },
        "values": {
            "DIA": 10,
            "RUB":  7,
            "EMR":  5,
            "SPH":  4,
            "AMT":  3,
            "OPL":  2,
        },
        "scatter": "DIA",
        "emojis": {
            "DIA": " DIA ",
            "RUB": " RUB ",
            "EMR": " EMR ",
            "SPH": " SPH ",
            "AMT": " AMT ",
            "OPL": " OPL ",
        },
    },
    "3": {
        "name": "Royal Cards",
        "symbols": {
            "ACE": 1,
            "KNG": 2,   # King
            "QEN": 3,   # Queen
            "JCK": 4,   # Jack
            "TEN": 5,
            "NIN": 6,   # Nine
        },
        "values": {
            "ACE": 10,
            "KNG":  7,
            "QEN":  5,
            "JCK":  4,
            "TEN":  3,
            "NIN":  2,
        },
        "scatter": "ACE",
        "emojis": {
            "ACE": " ACE ",
            "KNG": " KNG ",
            "QEN": " QEN ",
            "JCK": " JCK ",
            "TEN": " TEN ",
            "NIN": " NIN ",
        },
    },
}
