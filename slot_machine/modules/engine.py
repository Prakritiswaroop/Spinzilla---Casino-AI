# =============================================================================
#  engine.py  —  Core slot machine logic
# =============================================================================

import random
from modules.config import FREE_SPIN_TRIGGER, BONUS_MULTIPLIER


# ---------------------------------------------------------------------------
# Reel generation
# ---------------------------------------------------------------------------
def build_reel_pool(symbols: dict) -> list:
    """
    Build a flat list of symbols weighted by their count values.
    e.g. {"A": 2, "B": 4}  →  ["A","A","B","B","B","B"]
    """
    pool = []
    for symbol, count in symbols.items():
        pool.extend([symbol] * count)
    return pool


def spin_reels(rows: int, cols: int, symbols: dict) -> list[list]:
    """
    Return a list of `cols` columns, each a list of `rows` symbols.
    Sampling is done WITHOUT replacement per column so the same
    symbol cannot appear twice in the same column on one spin.
    """
    pool = build_reel_pool(symbols)
    columns = []
    for _ in range(cols):
        column = []
        available = pool[:]
        for _ in range(rows):
            pick = random.choice(available)
            available.remove(pick)
            column.append(pick)
        columns.append(column)
    return columns


# ---------------------------------------------------------------------------
# Win checking
# ---------------------------------------------------------------------------
def check_winnings(columns: list, lines: int, bet: int, values: dict):
    """
    Check each active line (row) for a matching triple.

    Returns
    -------
    winnings     : int   total payout before multiplier
    winning_lines: list  1-indexed winning row numbers
    """
    winnings = 0
    winning_lines = []

    for line in range(lines):                  # line = 0-indexed row
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:                                  # all columns matched
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)    # store 1-indexed

    return winnings, winning_lines


# ---------------------------------------------------------------------------
# Scatter / bonus detection
# ---------------------------------------------------------------------------
def count_scatter(columns: list, scatter_symbol: str) -> int:
    """Count how many times the scatter symbol appears anywhere on the grid."""
    total = 0
    for column in columns:
        total += column.count(scatter_symbol)
    return total


def check_bonus_trigger(columns: list, scatter_symbol: str) -> tuple[bool, int]:
    """
    Returns (triggered, free_spins_awarded).
    Triggers when scatter count >= FREE_SPIN_TRIGGER.
    More scatters = more free spins.
    """
    count = count_scatter(columns, scatter_symbol)
    if count >= FREE_SPIN_TRIGGER:
        free_spins = count * 2          # e.g. 3 scatters → 6 free spins
        return True, free_spins
    return False, 0


# ---------------------------------------------------------------------------
# Free spin round
# ---------------------------------------------------------------------------
def run_free_spins(
    free_spins: int,
    lines: int,
    bet: int,
    theme: dict,
    print_slot_fn,
    ui,
):
    """
    Execute all awarded free spins.

    Parameters
    ----------
    free_spins   : number of free spins to play
    lines        : lines the player bet on (carried over from normal spin)
    bet          : bet amount (carried over)
    theme        : the active theme dict (has symbols, values, scatter)
    print_slot_fn: ui.print_slot_machine callable
    ui           : the ui module (for print helpers)

    Returns
    -------
    total_winnings : int  (already multiplied by BONUS_MULTIPLIER)
    """
    total = 0
    remaining = free_spins

    while remaining > 0:
        ui.print_free_spin_header(remaining)
        input(ui.bold("  > Press Enter for your free spin..."))

        reels = spin_reels(3, 3, theme["symbols"])
        winnings, winning_lines = check_winnings(reels, lines, bet, theme["values"])
        boosted = winnings * BONUS_MULTIPLIER

        print_slot_fn(reels, winning_lines)

        if winning_lines:
            ui.print_win(boosted, winning_lines, free_spin=True, multiplier=BONUS_MULTIPLIER)
        else:
            ui.print_loss()

        total    += boosted
        remaining -= 1

        # Re-trigger: check for bonus inside free spins
        triggered, extra = check_bonus_trigger(reels, theme["scatter"])
        if triggered:
            print()
            print(ui.magenta("  ★ RE-TRIGGER! +" + str(extra) + " more free spins!"))
            remaining += extra

    return total
