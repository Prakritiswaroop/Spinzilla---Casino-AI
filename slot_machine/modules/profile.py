# =============================================================================
#  profile.py  —  Save / load player profile and leaderboard (JSON)
# =============================================================================

import json
import os
from modules.config import PROFILE_FILE, LEADERBOARD_FILE, MAX_LEADERBOARD, DATA_DIR


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save_json(path, data):
    _ensure_data_dir()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------
def default_profile(name="Player"):
    return {
        "name":             name,
        "balance":          0,
        "best_balance":     0,
        "spins":            0,
        "wins":             0,
        "total_free_spins": 0,
        "theme":            "1",
    }


def load_profile():
    return _load_json(PROFILE_FILE, None)


def save_profile(profile):
    # Keep best_balance up to date
    if profile["balance"] > profile["best_balance"]:
        profile["best_balance"] = profile["balance"]
    _save_json(PROFILE_FILE, profile)


def update_profile_stats(profile, net, free_spin_used=False):
    """Call after every spin to update counters."""
    profile["spins"] += 1
    if net > 0:
        profile["wins"] += 1
    if free_spin_used:
        profile["total_free_spins"] += 1
    if profile["balance"] > profile["best_balance"]:
        profile["best_balance"] = profile["balance"]


# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------
def load_leaderboard():
    return _load_json(LEADERBOARD_FILE, [])


def save_leaderboard(entries):
    _save_json(LEADERBOARD_FILE, entries)


def update_leaderboard(profile):
    """
    Insert / update this player in the leaderboard, keep top MAX_LEADERBOARD,
    sorted by best_balance descending.
    """
    entries = load_leaderboard()

    # Find existing entry for this player
    existing = next((e for e in entries if e["name"] == profile["name"]), None)

    if existing:
        # Update only if improved
        if profile["best_balance"] > existing["best_balance"]:
            existing["best_balance"] = profile["best_balance"]
        existing["spins"] = profile["spins"]
        existing["wins"]  = profile["wins"]
    else:
        entries.append({
            "name":         profile["name"],
            "best_balance": profile["best_balance"],
            "spins":        profile["spins"],
            "wins":         profile["wins"],
        })

    # Sort and trim
    entries.sort(key=lambda e: e["best_balance"], reverse=True)
    entries = entries[:MAX_LEADERBOARD]
    save_leaderboard(entries)
    return entries
