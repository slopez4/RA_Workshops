"""
Project:       RA Workshops, Workshop 6 (advanced experiment scripting)
Script:        06_advanced_psychopy/trial_matrix.py
Creator:       <name> (AI-assisted: Claude)
Purpose:       Builds the whole trial sequence for one session BEFORE the first
               trial is shown, and works out what each display looks like. No
               PsychoPy in here on purpose: the design can be checked on any
               computer (test_trial_matrix.py), without a screen or keyboard.
Last updated:  2026-11-15

Usage:
    import trial_matrix as tm                 (in grouping_task.py)
    python trial_matrix.py                    print one example session

Dependencies:  pandas
Reads:         nothing
Writes:        nothing (grouping_task.py saves the table as <subid>_trials.csv)
"""

import itertools
import random

import pandas as pd

# ---------------------------------------------------------------------------
# The design: every factor and its levels. One block = every combination once.
# ---------------------------------------------------------------------------
CUES = ["PROX", "SIM", "CR"]          # grouping cues (a subset of the lab's RDT)
WBN_LEVELS = ["WITHIN", "BETWEEN"]    # is the repeated pair inside one group?
TARG_POSITIONS = [3, 4, 5, 6]         # where the repeated pair starts (1-indexed)
TARG_TYPES = ["SQUARE", "CIRCLE"]     # which shape repeats
N_ITEMS = 9                           # shapes in the row

MAX_RUN = 3          # never more than 3 trials in a row with the same cue (chosen by hand)
MAX_SHUFFLES = 1000  # give up (and say so) if the constraint can't be met
PROX_SHIFT = 0.125   # proximity: each shape moves 1/8 of the spacing toward its partner
                     # (10 px of 80 px in the lab's RDT02_Lab.py)


def conditions():
    """Every combination of the factors, once. Returns a list of dicts.

    NEUTRAL has no WITHIN/BETWEEN, so it only crosses position x shape.
    3 cues x 2 x 4 x 2 = 48, plus 4 x 2 = 8 NEUTRAL: 56 conditions.
    """
    rows = []
    for pos, shape in itertools.product(TARG_POSITIONS, TARG_TYPES):
        rows.append({"Cue": "NEUTRAL", "WBN": "NEUTRAL", "Targ_Pos": pos, "Targ_Type": shape})
    for cue, wbn, pos, shape in itertools.product(CUES, WBN_LEVELS, TARG_POSITIONS, TARG_TYPES):
        rows.append({"Cue": cue, "WBN": wbn, "Targ_Pos": pos, "Targ_Type": shape})
    for number, row in enumerate(rows, start=1):
        row["Condition_ID"] = number
    return rows


def longest_run(values):
    """Length of the longest stretch of identical neighbours in a list."""
    longest = current = 1
    for before, after in zip(values, values[1:]):
        current = current + 1 if after == before else 1
        longest = max(longest, current)
    return longest if values else 0


def shuffle_with_limit(rows, rng, max_run=MAX_RUN):
    """Shuffle until no cue repeats more than `max_run` times in a row.

    Shuffling and checking ("rejection sampling") is simple and unbiased;
    MAX_SHUFFLES stops it from looping forever if the limit is impossible.
    """
    rows = list(rows)
    for _ in range(MAX_SHUFFLES):
        rng.shuffle(rows)
        if longest_run([r["Cue"] for r in rows]) <= max_run:
            return rows
    raise RuntimeError("Could not meet the run limit in %d shuffles." % MAX_SHUFFLES)


def one_per_cell(rows, rng, per_cell):
    """Pick `per_cell` random rows from each Cue x WBN cell (practice, debug).

    Keeps every trial type in a short version, so a debug run still tests
    every code path.
    """
    picked = []
    cells = sorted({(r["Cue"], r["WBN"]) for r in rows})
    for cue, wbn in cells:
        members = [r for r in rows if r["Cue"] == cue and r["WBN"] == wbn]
        picked += rng.sample(members, per_cell)
    return picked


def build_session(n_blocks, seed, debug=False):
    """The full trial sequence for one session, as a table.

    Block 0 is practice (one trial per Cue x WBN cell). Blocks 1..n_blocks
    contain every condition once (debug: 2 per cell), in a new constrained
    random order each block. The same seed always gives the same table.

    Returns a DataFrame, one row per trial, with Trial_ID unique across the
    whole session.
    """
    rng = random.Random(seed)
    design = conditions()
    blocks = [(0, one_per_cell(design, rng, 1))]
    for block in range(1, n_blocks + 1):
        rows = one_per_cell(design, rng, 2) if debug else design
        blocks.append((block, rows))

    table = []
    for block, rows in blocks:
        for trial, row in enumerate(shuffle_with_limit(rows, rng), start=1):
            table.append({"Block_Num": block, "Trial_Num": trial, **row})
    table = pd.DataFrame(table)
    table.insert(0, "Trial_ID", range(1, len(table) + 1))
    table["Is_Practice"] = table["Block_Num"] == 0
    return table


def add_response_keys(trials, key_square, key_circle):
    """Add the correct key for every trial (it depends on the counterbalancing)."""
    trials = trials.copy()
    trials["Correct_Key"] = trials["Targ_Type"].map({"SQUARE": key_square, "CIRCLE": key_circle})
    return trials


# ---------------------------------------------------------------------------
# What one display looks like. Logic follows RDT02_Lab.py (the lab's task).
# ---------------------------------------------------------------------------
def layout(cue, wbn, targ_pos, targ_type):
    """Shapes, positions and colors for one trial.

    Returns a dict:
      shapes  list of "SQUARE"/"CIRCLE", left to right
      x       horizontal positions in units of item spacing (0 = centre)
      colors  "black" or "white" for each shape
      boxes   centres (same units) of the common-region frames, [] if none
    The repeated pair is items targ_pos-1 and targ_pos (0-indexed).
    """
    other = "CIRCLE" if targ_type == "SQUARE" else "SQUARE"
    # Pairing 1 groups items (0,1) (2,3) ...; pairing 2 groups (1,2) (3,4) ...
    # Choosing the pairing is what puts the repeated pair WITHIN or BETWEEN groups.
    pairing1 = (targ_pos % 2 == 1) == (wbn == "WITHIN")

    shapes = [targ_type if targ_pos % 2 == 1 else other]
    for i in range(1, N_ITEMS):
        if i == targ_pos:
            shapes.append(shapes[-1])
        else:
            shapes.append("CIRCLE" if shapes[-1] == "SQUARE" else "SQUARE")

    x = [i - (N_ITEMS - 1) / 2 for i in range(N_ITEMS)]
    colors = ["black"] * N_ITEMS
    boxes = []
    first = 0 if pairing1 else 1                       # first item of the first pair
    if cue == "PROX":
        for i in range(N_ITEMS):
            moves_right = (i % 2 == first)             # first of a pair moves toward the second
            if i >= first and (i - first) // 2 < 4:    # only items that belong to a pair
                x[i] += PROX_SHIFT if moves_right else -PROX_SHIFT
    elif cue == "SIM":
        for i in range(N_ITEMS):
            group = (i - first) // 2 if i >= first else -1
            colors[i] = "white" if group % 2 == 1 else "black"
    elif cue == "CR":
        boxes = [x[first + 2 * p] + 0.5 for p in range(4)]
    return {"shapes": shapes, "x": x, "colors": colors, "boxes": boxes}


if __name__ == "__main__":
    example = build_session(n_blocks=2, seed=1)
    print(example.groupby("Block_Num").size().rename("trials per block"))
    print(example.head(10).to_string(index=False))
