"""
Project:       RA Workshops, Workshop 6
Script:        06_advanced_psychopy/test_trial_matrix.py
Creator:       <name> (AI-assisted: Claude)
Purpose:       Checks the trial matrix and the display layouts without PsychoPy,
               so a design mistake is caught before anyone sits in front of the
               screen. Run it after every change to trial_matrix.py.
Last updated:  2026-11-15

Usage:
    python test_trial_matrix.py        prints PASS for each check, stops at the first FAIL

Dependencies:  pandas, trial_matrix.py (same folder)
Reads:         nothing
Writes:        nothing
"""

import trial_matrix as tm


def check(name, condition):
    """Print PASS, or stop with a clear message."""
    if not condition:
        raise SystemExit("FAIL: " + name)
    print("PASS:", name)


# ---------------------------------------------------------------------------
# The design
# ---------------------------------------------------------------------------
design = tm.conditions()
check("56 conditions (48 cued + 8 neutral)", len(design) == 56)
check("no duplicate conditions",
      len({(r["Cue"], r["WBN"], r["Targ_Pos"], r["Targ_Type"]) for r in design}) == 56)

session = tm.build_session(n_blocks=3, seed=42)
main = session[session["Block_Num"] > 0]
check("every main block has every condition exactly once",
      all(sorted(b["Condition_ID"]) == list(range(1, 57)) for _, b in main.groupby("Block_Num")))
check("practice has one trial per Cue x WBN cell",
      session[session["Block_Num"] == 0].groupby(["Cue", "WBN"]).size().eq(1).all())
check("Trial_ID is unique across the session", session["Trial_ID"].is_unique)
check("Trial_Num restarts at 1 in every block",
      session.groupby("Block_Num")["Trial_Num"].min().eq(1).all())
check("no cue appears more than MAX_RUN times in a row",
      all(tm.longest_run(list(b["Cue"])) <= tm.MAX_RUN for _, b in session.groupby("Block_Num")))
check("blocks are in different orders",
      list(main[main["Block_Num"] == 1]["Condition_ID"]) != list(main[main["Block_Num"] == 2]["Condition_ID"]))
check("same seed -> same session (a crash can replay it exactly)",
      session.equals(tm.build_session(n_blocks=3, seed=42)))
check("different seed -> different session",
      not session.equals(tm.build_session(n_blocks=3, seed=43)))

debug = tm.build_session(n_blocks=2, seed=1, debug=True)
check("debug keeps every Cue x WBN cell in every block",
      debug.groupby("Block_Num")["Cue"].nunique().eq(len(tm.CUES) + 1).all())
check("debug blocks are short (14 trials)",
      debug[debug["Block_Num"] > 0].groupby("Block_Num").size().eq(14).all())

keyed = tm.add_response_keys(session, key_square="n", key_circle="m")
check("correct key follows the shape",
      (keyed["Correct_Key"] == keyed["Targ_Type"].map({"SQUARE": "n", "CIRCLE": "m"})).all())

# ---------------------------------------------------------------------------
# The displays: is the repeated pair really WITHIN or BETWEEN a group?
# ---------------------------------------------------------------------------
def groups(display, cue):
    """Which group each item belongs to, read back from the drawn layout."""
    if cue == "PROX":       # a new group starts wherever the gap is wide
        gaps = [b - a for a, b in zip(display["x"], display["x"][1:])]
        labels, g = [0], 0
        for gap in gaps:
            g += gap > 1.0
            labels.append(g)
        return labels
    if cue == "SIM":        # a new group starts wherever the color changes
        labels, g = [0], 0
        for a, b in zip(display["colors"], display["colors"][1:]):
            g += a != b
            labels.append(g)
        return labels
    if cue == "CR":         # items inside the same frame
        return [min(range(4), key=lambda p: abs(display["boxes"][p] - x)) if
                min(abs(c - x) for c in display["boxes"]) < 0.75 else -1 - i
                for i, x in enumerate(display["x"])]


all_ok = True
for row in design:
    d = tm.layout(row["Cue"], row["WBN"], row["Targ_Pos"], row["Targ_Type"])
    first, second = row["Targ_Pos"] - 1, row["Targ_Pos"]
    repeats = [i for i in range(tm.N_ITEMS - 1) if d["shapes"][i] == d["shapes"][i + 1]]
    all_ok &= repeats == [first] and d["shapes"][first] == row["Targ_Type"]
    if row["Cue"] != "NEUTRAL":
        g = groups(d, row["Cue"])
        same_group = g[first] == g[second]
        all_ok &= same_group == (row["WBN"] == "WITHIN")
check("every display: exactly one repeated pair, of the right shape, "
      "WITHIN or BETWEEN groups as labelled", all_ok)

print("\nAll checks passed.")
