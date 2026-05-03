# =============================================================================
#  ui.py  —  All display, colour, and print helpers
# =============================================================================

from colorama import init, Fore, Style
init(autoreset=True)


# ---------------------------------------------------------------------------
# Colour wrappers
# ---------------------------------------------------------------------------
def green(t):   return Fore.GREEN   + Style.BRIGHT + str(t) + Style.RESET_ALL
def red(t):     return Fore.RED     + Style.BRIGHT + str(t) + Style.RESET_ALL
def yellow(t):  return Fore.YELLOW  + Style.BRIGHT + str(t) + Style.RESET_ALL
def cyan(t):    return Fore.CYAN    + Style.BRIGHT + str(t) + Style.RESET_ALL
def magenta(t): return Fore.MAGENTA + Style.BRIGHT + str(t) + Style.RESET_ALL
def bold(t):    return Style.BRIGHT + str(t) + Style.RESET_ALL
def white(t):   return Fore.WHITE   + Style.BRIGHT + str(t) + Style.RESET_ALL


# ---------------------------------------------------------------------------
# Banners
# ---------------------------------------------------------------------------
def print_welcome():
    print(cyan("╔══════════════════════════════════════╗"))
    print(cyan("║") + bold("     PYTHON SLOT MACHINE  v2.0        ") + cyan("║"))
    print(cyan("║") + "   Save • Leaderboard • Themes • Bonus  " + cyan("║"))
    print(cyan("╚══════════════════════════════════════╝"))
    print()


def print_section(title):
    bar = "─" * (len(title) + 4)
    print()
    print(cyan("┌" + bar + "┐"))
    print(cyan("│") + "  " + bold(title) + "  " + cyan("│"))
    print(cyan("└" + bar + "┘"))


def print_divider():
    print(cyan("  " + "─" * 38))


# ---------------------------------------------------------------------------
# Slot machine display
# ---------------------------------------------------------------------------
def print_slot_machine(columns, winning_lines=None):
    """
    Print the 3x3 grid.  Highlight winning rows in green.
    winning_lines is 1-indexed list e.g. [1, 3]
    """
    winning_lines = winning_lines or []
    num_rows = len(columns[0])

    print()
    print(cyan("  ╔═══════╦═══════╦═══════╗"))
    for row in range(num_rows):
        line_num = row + 1
        is_winner = line_num in winning_lines

        row_str = cyan("  ║")
        for col_idx, column in enumerate(columns):
            sym = column[row]
            cell = f" {sym:^5} "
            if is_winner:
                row_str += green(cell)
            else:
                row_str += yellow(cell) if col_idx == 0 else cell
            row_str += cyan("║")

        # Line number indicator on the left
        indicator = green(f"<{line_num}>") if is_winner else f" {line_num} "
        print(f"{indicator}{row_str}")

        if row < num_rows - 1:
            print(cyan("  ╠═══════╬═══════╬═══════╣"))

    print(cyan("  ╚═══════╩═══════╩═══════╝"))
    print()


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
def print_win(winnings, winning_lines, free_spin=False, multiplier=1):
    tag = magenta(" [FREE SPIN x" + str(multiplier) + "]") if free_spin else ""
    print(green("  ★ YOU WON $" + str(winnings) + "!" + tag))
    print(green("  ★ Winning line(s): " + str(winning_lines)))


def print_loss():
    print(red("  ✗ No winning lines this time."))


def print_net(net):
    if net >= 0:
        print(green("  Net this spin: +" + str(net)))
    else:
        print(red("  Net this spin: -" + str(abs(net))))


# ---------------------------------------------------------------------------
# Free spin announcement
# ---------------------------------------------------------------------------
def print_free_spin_trigger(count):
    print()
    print(magenta("  ╔══════════════════════════════╗"))
    print(magenta("  ║   ★  BONUS FREE SPINS!  ★    ║"))
    print(magenta("  ║  " + str(count) + " free spins awarded!          ║"))
    print(magenta("  ║  All wins pay DOUBLE!         ║"))
    print(magenta("  ╚══════════════════════════════╝"))
    print()


def print_free_spin_header(remaining):
    print(magenta("  [ FREE SPIN — " + str(remaining) + " remaining | 2x payout ]"))


# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------
def print_leaderboard(entries):
    print_section("LEADERBOARD — Top Players")
    if not entries:
        print("  No entries yet. Be the first!")
        return

    print(f"  {'Rank':<5} {'Name':<16} {'Best Balance':>13} {'Spins':>7} {'Win%':>6}")
    print(cyan("  " + "─" * 52))
    for i, e in enumerate(entries, 1):
        rank_str = bold(f"  #{i:<4}")
        win_pct  = (e['wins'] / e['spins'] * 100) if e['spins'] else 0
        row = (f"{e['name']:<16} "
               f"${e['best_balance']:>12,} "
               f"{e['spins']:>7} "
               f"{win_pct:>5.1f}%")
        if i == 1:
            print(rank_str + yellow(row))
        elif i == 2:
            print(rank_str + white(row))
        elif i == 3:
            print(rank_str + cyan(row))
        else:
            print(rank_str + row)


# ---------------------------------------------------------------------------
# Profile summary
# ---------------------------------------------------------------------------
def print_profile(profile):
    print_section("YOUR PROFILE")
    win_pct = (profile['wins'] / profile['spins'] * 100) if profile['spins'] else 0
    print(f"  Name         : {bold(profile['name'])}")
    print(f"  Balance      : {green('$' + str(profile['balance']))}")
    print(f"  Best Balance : {yellow('$' + str(profile['best_balance']))}")
    print(f"  Total Spins  : {profile['spins']}")
    print(f"  Wins         : {profile['wins']}")
    print(f"  Win Rate     : {win_pct:.1f}%")
    print(f"  Free Spins   : {profile['total_free_spins']}")


# ---------------------------------------------------------------------------
# Theme selector
# ---------------------------------------------------------------------------
def print_theme_menu(themes):
    print_section("SELECT THEME")
    for key, theme in themes.items():
        syms = "  ".join(theme["emojis"].values())
        print(f"  [{key}] {bold(theme['name'])}")
        print(f"       {cyan(syms)}")
        print()


# ---------------------------------------------------------------------------
# Input helpers (with validation)
# ---------------------------------------------------------------------------
def ask_int(prompt, lo, hi):
    """Ask for an integer between lo and hi inclusive."""
    while True:
        raw = input(bold("  > " + prompt)).strip()
        if raw.isdigit():
            val = int(raw)
            if lo <= val <= hi:
                return val
            else:
                print(red(f"  Enter a number between {lo} and {hi}."))
        else:
            print(red("  Please enter a whole number."))


def ask_yn(prompt):
    """Ask a yes/no question, return True for yes."""
    while True:
        raw = input(bold("  > " + prompt + " (y/n): ")).strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print(red("  Please enter y or n."))


def ask_str(prompt, max_len=20):
    """Ask for a non-empty string."""
    while True:
        raw = input(bold("  > " + prompt)).strip()
        if 1 <= len(raw) <= max_len:
            return raw
        print(red(f"  Please enter between 1 and {max_len} characters."))
