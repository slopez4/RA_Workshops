"""
Project:       RA Workshops, Workshop 5
Script:        05_analysis_scripts_ggp/notebooks/build_notebooks.py
Creator:       <name> (AI-assisted: Claude)
Purpose:       Writes the student and solutions notebooks from ONE list of cells,
               so the two can never drift apart. Edit the cells here, then rerun.
Last updated:  2026-11-15

Usage:
    python notebooks/build_notebooks.py

    In a code cell, «answer» becomes ___ in the student notebook and the answer
    in the solutions notebook. A ("code2", solution, student) cell has two
    different versions.

Dependencies:  Python standard library only
Reads:         nothing
Writes:        notebooks/workshop_student.ipynb, notebooks/workshop_solutions.ipynb
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLANK = re.compile(r"«(.*?)»", re.S)

CELLS = []


def md(text):
    CELLS.append(("md", text.strip("\n")))


def code(text):
    CELLS.append(("code", text.strip("\n")))


def code2(solution, student):
    CELLS.append(("code2", solution.strip("\n"), student.strip("\n")))


# ===========================================================================
# Title and setup
# ===========================================================================
md("""
# Workshop 5 · Reading and Writing Analysis Scripts with Real Data
### Do grouping cues change how fast people see a repeated shape?

**This time the data are real.** They come from the lab's gestalt grouping study (GGP),
which uses the **Repetition Discrimination Task (RDT)**. You'll analyze 25 pilot
participants. Their IDs were replaced with new random codes, and age and sex were removed.
Please keep the files inside this workshop: don't share them or post them anywhere.

**How this notebook works** (same as Workshop 1)
- Click a grey code cell and press **Shift + Enter** to run it. Run cells **top to bottom**.
- `# TODO` cells have a blank `___` for you to fill in.
- 🔮 **Predict** cells: write your guess in the comment *before* you run the cell. Being
  wrong is the point: it shows you exactly which part of the code you misread.
- 🤔 **Think** prompts: stop and talk it over with your neighbour.

**Before you start:** File → *Save a copy in Drive*, so your work is saved.
""")

code("""
# SETUP: run this once. It finds the data, or downloads the workshop files if
# they aren't here yet (that's what happens in Colab).
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

if Path("../data/rawdata").exists():                     # running from a downloaded copy
    DATA_DIR = Path("../data/rawdata")
else:                                                    # running in Colab
    if not Path("RA_Workshops").exists():
        subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                        "https://github.com/slopez4/RA_Workshops.git"], check=True)
    DATA_DIR = Path("RA_Workshops/05_analysis_scripts_ggp/data/rawdata")

SCRIPT = DATA_DIR.parent.parent / "rdt_analysis.py"      # the finished script (Part 7)
print("Data folder:", DATA_DIR)
""")

# ===========================================================================
# Part 0: the study
# ===========================================================================
md("""
---
## Part 0 · The study in 3 minutes

On every trial, a row of **9 shapes** appears. Squares and circles alternate, except for
**one pair that repeats** (two squares or two circles side by side). The participant
presses a key to say **which shape repeated**, as fast as they can.

A **grouping cue** splits the row into pairs: shapes closer together (**PROX**imity),
the same color (**SIM**ilarity), inside a box (**CR**, common region), joined by a bar
(**EC**, element connectedness), moving together (**COMMONFATE**), flickering together
(**SYNCHRONY**), or sharing flankers (**IPG**). **NEUTRAL** trials have no cue.

- **WITHIN**: the repeated pair sits *inside* one group.
- **BETWEEN**: the repeated pair is split *across* two groups.

**The prediction:** a repetition is easier to see when both shapes belong to the same
group, so WITHIN trials should be faster. For each cue, the **grouping effect** is

> **effect = mean RT on BETWEEN trials − mean RT on WITHIN trials**

A positive effect means the cue grouped the shapes. Run the next cell to see what
participants saw. You don't need to understand this cell's code yet: by the end of today
you'll be able to read most of it.
""")

code("""
# Draws one RDT display. Logic copied from the lab's experiment script (RDT02_Lab.py).
def draw_display(ax, cue, wbn, targ_pos=3, targ_type="square"):
    other = "circle" if targ_type == "square" else "square"
    pairing1 = (targ_pos % 2 == 1) == (wbn == "WITHIN")    # which shapes get grouped
    shapes = [targ_type if targ_pos % 2 == 1 else other]
    for i in range(1, 9):
        if i == targ_pos:
            shapes.append(shapes[-1])                        # the repeated pair
        else:
            shapes.append("circle" if shapes[-1] == "square" else "square")
    for i, shape in enumerate(shapes):
        x = i - 4
        if cue == "PROX":                                    # pull pairs together
            toward = 0.125 if (i % 2 == 0) == pairing1 else -0.125
            x = x + toward
        if cue == "SIM":                                     # color pairs alike
            pattern = [0, 0, 1, 1, 0, 0, 1, 1, 0] if pairing1 else [0, 1, 1, 0, 0, 1, 1, 0, 0]
            color = "black" if pattern[i] == 0 else "white"
        else:
            color = "black"
        if shape == "square":
            ax.add_patch(plt.Rectangle((x - 0.19, -0.19), 0.38, 0.38, color=color))
        else:
            ax.add_patch(plt.Circle((x, 0), 0.19, color=color))
    ax.set_xlim(-5, 5); ax.set_ylim(-0.8, 0.8); ax.set_aspect("equal")
    ax.set_facecolor("#808080"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{cue} · {wbn}")

fig, axes = plt.subplots(2, 2, figsize=(11, 3.4))
draw_display(axes[0, 0], "PROX", "WITHIN")
draw_display(axes[0, 1], "PROX", "BETWEEN")
draw_display(axes[1, 0], "SIM", "WITHIN")
draw_display(axes[1, 1], "SIM", "BETWEEN")
plt.tight_layout()
plt.show()
""")

md("""
🤔 **Think:** find the repeated pair (two squares) in each display. In which displays does
it "pop out"? Does that match the prediction?
""")

# ===========================================================================
# Part 1: reading code
# ===========================================================================
md("""
---
## Part 1 · Reading code: predict, then run

Analysis code is mostly **read**, not written. The habit we're building: before running a
cell, say what it will print. Here are four made-up trials stored as a **list of
dictionaries**: each `{...}` is one trial, and each `"key": value` is one column.
""")

code("""
trials = [
    {"cue": "PROX", "wbn": "WITHIN",  "correct": 1, "rt": 0.81},
    {"cue": "PROX", "wbn": "BETWEEN", "correct": 1, "rt": 1.20},
    {"cue": "PROX", "wbn": "WITHIN",  "correct": 0, "rt": 0.65},
    {"cue": "PROX", "wbn": "BETWEEN", "correct": 1, "rt": 1.05},
]

# 🔮 Predict: what will these two lines print?   My guess: ...
print(len(trials))
print(trials[1]["rt"])
""")

code("""
# 🔮 Predict: which RTs end up in each list? Write them here before running:
#    within  = ...
#    between = ...
within = []
between = []
for trial in trials:
    if trial["correct"] == 0:
        continue                      # skip to the next trial: errors don't count
    if trial["wbn"] == "WITHIN":
        within.append(trial["rt"])
    else:
        between.append(trial["rt"])

print("within: ", within)
print("between:", between)
""")

md("""
A **function** packages a few lines under a name, so you can reuse them. `def` defines
it, the names in brackets are its **inputs**, and `return` sends back its **output**.
""")

code("""
def mean(values):
    \"\"\"Average of a list of numbers.\"\"\"
    return sum(values) / len(values)

# TODO: the grouping effect is mean BETWEEN RT minus mean WITHIN RT
effect = «mean(between) - mean(within)»
print(f"Grouping effect: {effect * 1000:.0f} ms")
""")

md("""
🤔 **Think:** the answer is **315 ms**, not 395 ms. Why? (Hint: which trial never made it
into `within`?) Why do we leave error trials out of an RT analysis?
""")

# ===========================================================================
# Part 2: load many files
# ===========================================================================
md("""
---
## Part 2 · Bring in many files

The experiment writes **one file per participant**: `RDTdata_<ID>.csv`. Real analyses
start by finding every file and stacking them into one table.
""")

code("""
files = sorted(DATA_DIR.glob("RDTdata_*.csv"))     # every file whose name fits the pattern
print(len(files), "files")
for path in files[:3]:                             # the first three
    print(path.name)
""")

md("""
🤔 **Think:** we said 25 participants. How many files are there? Scroll to the end of the
list with `print(files[-1].name)`: which ID is that, and what is it for? (Lab rule: IDs
`1`–`100` are pilots, `999` is **debugging**, `101` and up are real participants.)
""")

code("""
first = pd.read_csv(files[0], dtype={"subjectId": str})
print(first.shape)        # (rows, columns)
first.head()
""")

md("""
**Codebook: one row = one trial**

| column | meaning |
|---|---|
| `subjectId` | participant code (re-coded for this workshop) |
| `block`, `trial` | block number (from 1); trial number, restarting at 1 in every block |
| `trialID` | which of the 240 conditions this was (1–240) |
| `cueType` | grouping cue: PROX, SIM, CR, EC, COMMONFATE, SYNCHRONY, IPG, or NEUTRAL |
| `wbn` | WITHIN, BETWEEN, or NEUTRAL (only for NEUTRAL trials) |
| `targPos` | position of the repeated pair (3–6) |
| `colorCond`, `ipgColor` | colors used on that trial |
| `targType` | which shape repeated: SQUARE or CIRCLE |
| `resp` | which shape the participant chose |
| `ac` | 1 = correct, 0 = wrong |
| `rt` | reaction time in **seconds** |

Why `dtype={"subjectId": str}`? Without it, pandas reads IDs as numbers. Run this:
""")

code("""
ids_as_text = pd.Series(["007", "101"])
print(ids_as_text.astype(int).tolist())     # what happens to "007"?
""")

md("""
Now the loop that reads every file. Read it line by line first.
""")

code("""
tables = []
for path in files:
    one = pd.read_csv(path, dtype={"subjectId": str})
    subject = path.stem.split("_")[1]           # "RDTdata_102" -> "102"
    # TODO: skip the debugging ID (as text, in quotes)
    if subject == «"999"» or len(one) == 0:
        print("skipping", path.name, "-", len(one), "trials")
        continue
    tables.append(one)

df = pd.concat(tables, ignore_index=True)       # stack all tables into one
print(len(tables), "participants,", len(df), "trials")
""")

md("""
🤔 **Think:** `path.stem.split("_")[1]` is three steps chained together. Take
`RDTdata_102.csv` and say what each step gives you. (Try `print(files[0].stem)` in a new
cell.)
""")

# ===========================================================================
# Part 3: check
# ===========================================================================
md("""
---
## Part 3 · Look before you analyze

Every participant did the same task, so every participant should have the same number
of trials. Let's check.
""")

code("""
n_trials = df.groupby("subjectId").size()      # rows per participant
print(n_trials.value_counts())                 # how many participants have each count?
""")

code("""
# TODO: show only the participants with MORE than 720 trials
n_trials[«n_trials > 720»]
""")

code("""
# How many blocks did each participant run?
df.groupby("subjectId")["block"].max().value_counts()
""")

md("""
🤔 **Think:** three participants ran **5 blocks** instead of 3. (They were early pilots,
before the task was shortened.) What are our options, and what could go wrong with
each? Keep everything? Drop those three people? Keep only their first 3 blocks?
""")

code("""
df["rt"].describe().round(3)
""")

md("""
🤔 **Think:** look at `min` and `max`. Can a reaction time be **negative**? Can it be
**65 seconds**? Find the strange trials:
""")

code("""
df[df["rt"] < 0.2][["subjectId", "block", "trial", "cueType", "ac", "rt"]]
""")

md("""
🤔 **Think:** one negative RT is on **trial 1** of a block. The other is on **trial 121**,
the first trial after the "halfway through, press space to resume" break. Both came
right after a "press space" screen. A negative RT means the key was pressed *before* the
display appeared. What could the participant have pressed while that screen was up, and
why would the experiment count it as their answer? (We'll find this bug in the
experiment code in Workshop 6.)
""")

code("""
df["rt"].plot.hist(bins=60, range=(0, 6))
plt.xlabel("Reaction time (s)")
plt.ylabel("Number of trials")
plt.show()
""")

md("""
Now each participant's accuracy and their share of very slow trials, **in blocks 1–3
only** (the part everyone did). `ac` is 1 or 0, so its mean is the proportion correct.
""")

code("""
first3 = df[df["block"] <= 3]

per_person = pd.DataFrame({
    "accuracy": first3.groupby("subjectId")["ac"].mean(),
    "share_slower_than_5s": (first3["rt"] > 5).groupby(first3["subjectId"]).mean(),
})
# TODO: sort so the LEAST accurate participants come first
per_person.sort_values(«"accuracy"»).head().round(3)
""")

md("""
🤔 **Think:** one participant is at 83% correct and is slower than 5 s on almost a quarter
of their trials. Chance on this task is 50%. Would you exclude them? **Decide your rule
now, before you see anyone's grouping effect,** and write it in the settings below.
""")

# ===========================================================================
# Part 4: clean
# ===========================================================================
md("""
---
## Part 4 · Clean the data, and keep a log

Every decision goes in one **settings** cell. Then each cleaning step records how many
trials and participants are left, so you can report exactly what you removed.
""")

code("""
# SETTINGS: decided before looking at the results
N_BLOCKS = 3          # keep blocks 1-3 for everyone
MIN_ACCURACY = 0.80   # proportion correct; chance is 0.50
MIN_RT = 0.2          # seconds; faster = pressed before seeing the display
MAX_RT = 5.0          # seconds; slower = attention wandered (the lab's cutoff)
""")

code("""
log = []                                                      # one entry per step
clean = df[df["block"] <= N_BLOCKS]
log.append(("blocks 1-3", len(clean), clean["subjectId"].nunique()))

accuracy = clean.groupby("subjectId")["ac"].mean()
too_low = accuracy[accuracy < MIN_ACCURACY].index             # IDs below the rule
clean = clean[~clean["subjectId"].isin(too_low)]              # ~ means NOT
log.append(("accuracy rule", len(clean), clean["subjectId"].nunique()))

clean = clean[clean["ac"] == 1]
log.append(("correct trials", len(clean), clean["subjectId"].nunique()))

# TODO: keep trials with RT >= MIN_RT AND RT <= MAX_RT (the symbol for AND is &)
clean = clean[(clean["rt"] >= MIN_RT) «&» (clean["rt"] <= MAX_RT)]
log.append(("RT window", len(clean), clean["subjectId"].nunique()))

pd.DataFrame(log, columns=["step", "trials_left", "participants_left"])
""")

md("""
🤔 **Think:** what percentage of the blocks 1–3 trials did we lose in total? Which step
removed the most? If one participant lost far more trials than the others, would that
worry you?
""")

# ===========================================================================
# Part 5: analyze
# ===========================================================================
md("""
---
## Part 5 · The grouping effect, one participant at a time

`groupby` sorts rows into piles and computes something for each pile. With three
columns, every pile is **one participant × one cue × WITHIN or BETWEEN**.
""")

code("""
means = clean.groupby(["subjectId", "cueType", "wbn"])["rt"].mean()
means.head(8)
""")

code("""
# unstack moves "wbn" from the rows into columns: BETWEEN, NEUTRAL, WITHIN side by side
means = means.unstack("wbn")
means.head(8)
""")

code("""
# TODO: effect in milliseconds = (BETWEEN minus WITHIN) times 1000
means["effect_ms"] = («means["BETWEEN"] - means["WITHIN"]») * 1000

# one row per participant, one column per cue (NEUTRAL has no effect, so it's dropped)
effects = means["effect_ms"].unstack("cueType").dropna(axis=1, how="all")
effects.round(0).head()
""")

code("""
summary = pd.DataFrame({
    "mean_ms": effects.mean(),
    "sem_ms": effects.sem(),                 # standard error: spread across PEOPLE
    # TODO: how many participants show a positive effect?
    "n_positive": («effects > 0»).sum(),
    "n": effects.count(),
}).sort_values("mean_ms", ascending=False)
summary.round(0)
""")

md("""
🤔 **Think:** we averaged each person's trials first, then averaged across people. What
would go wrong if we averaged all 16,000 trials at once? (Hint: who has more trials? What
does the SEM assume each row is?)
""")

code("""
order = summary.index.tolist()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(order, summary["mean_ms"], yerr=summary["sem_ms"], color="#cfd8e8", capsize=4)
for i, cue in enumerate(order):
    ax.scatter([i] * len(effects), effects[cue], s=12, color="#2f4a7f", alpha=0.5)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Grouping effect (ms)")
ax.set_title("Each dot is one participant")
plt.xticks(rotation=30)
plt.show()
""")

md("""
🤔 **Think:** which cue groups most strongly? Which is weakest? For the weakest cue, how
many participants go the "wrong" way? Is the bar enough to describe that cue?

**Optional:** a one-sample t-test asks whether the mean effect differs from 0.
""")

code("""
from scipy import stats
for cue in order:
    t, p = stats.ttest_1samp(effects[cue], 0)
    print(f"{cue:<11} t = {t:5.2f}   p = {p:.4f}")
""")

# ===========================================================================
# Part 6: find the bugs
# ===========================================================================
md("""
---
## Part 6 · Find the bugs

Below is someone else's analysis of the same data. **It runs without any error, and its
numbers look plausible. It has 3 bugs.** This is what most real analysis bugs look like:
no red message, just a wrong answer.

Run it, compare its output with your Part 5 results, then find the bugs. Don't look for
"wrong-looking code". Instead, **check what each step produces** (`print(len(...))`,
`.max()`, `.head()`).
""")

code("""
def buggy_analysis(df):
    keep = df[df["block"] < 3]
    keep = keep[keep["ac"] == 1]
    keep = keep[(keep["rt"] >= 0.2) | (keep["rt"] <= 5.0)]
    means = keep.groupby(["subjectId", "cueType", "wbn"])["rt"].mean().unstack("wbn")
    means["effect_ms"] = (means["WITHIN"] - means["BETWEEN"]) * 1000
    effects = means["effect_ms"].unstack("cueType").dropna(axis=1, how="all")
    print("trials used:", len(keep), "| slowest RT kept:", keep["rt"].max())
    return effects.mean().round(0)

buggy_analysis(df)
""")

code2(
    solution="""
def fixed_analysis(df):
    keep = df[df["block"] <= 3]                                    # BUG 1: < 3 kept only blocks 1-2
    keep = keep[keep["ac"] == 1]
    keep = keep[(keep["rt"] >= 0.2) & (keep["rt"] <= 5.0)]         # BUG 2: | (OR) kept every trial
    means = keep.groupby(["subjectId", "cueType", "wbn"])["rt"].mean().unstack("wbn")
    means["effect_ms"] = (means["BETWEEN"] - means["WITHIN"]) * 1000   # BUG 3: sign was flipped
    effects = means["effect_ms"].unstack("cueType").dropna(axis=1, how="all")

    # Checks that would have caught each bug. assert stops the code if it's False.
    assert keep["block"].max() == 3, "should keep blocks 1-3"
    assert keep["rt"].between(0.2, 5.0).all(), "RT window not applied"
    assert (effects.mean() > 0).sum() > 0, "every effect negative: check the subtraction"
    print("trials used:", len(keep), "| slowest RT kept:", keep["rt"].max())
    return effects.mean().round(0)

fixed_analysis(df)
""",
    student="""
# TODO: copy the buggy function here, rename it fixed_analysis, and fix the 3 bugs.
# Your fixed version should give the same means as your Part 5 summary.
# Hint: run pieces of it on their own. What should len(keep) be after each line?
""")

md("""
🤔 **Think:** for each bug, write one line of code that would have **caught it
automatically**. (Look up `assert`.) Which bug changes the conclusion, and which ones
only change the numbers?
""")

# ===========================================================================
# Part 7: script
# ===========================================================================
md("""
---
## Part 7 · From notebook to script, and how robust is the answer?

A notebook is for exploring. A **script** runs top to bottom every time, so anyone gets
the same result. [`rdt_analysis.py`](https://github.com/slopez4/RA_Workshops/blob/main/05_analysis_scripts_ggp/rdt_analysis.py)
is today's analysis as one script: settings at the top, one function per step, a header
that says what it reads and writes. Open it and find each Part of today in it.

Run it:
""")

code("""
!python {SCRIPT}
""")

md("""
The RT cutoff of 5 s was a decision. Would a different reasonable decision change the
answer? The script takes the cutoff as an option:
""")

code("""
!python {SCRIPT} --max-rt 2
""")

md("""
🤔 **Think:**
1. With a 2 s cutoff, what happens to the size of every effect? Does the **order** of the
   cues stay the same? Look at CR.
2. Why would cutting slow trials shrink the effect? (Which trials are slow: WITHIN or
   BETWEEN?)
3. Both cutoffs are defensible. What should a paper report, and when should the cutoff be
   chosen?

---
## ⭐ Stretch (homework)

1. **Accuracy:** repeat Part 5 with `ac` instead of `rt` (use all trials, not only correct
   ones). Is the effect also there in accuracy? Which way should it go?
2. **Reliability:** compute each person's effect separately on blocks 1 and 3. Do people
   with a big effect in block 1 also have a big one in block 3? (`.corr()`)
3. **Baseline:** compare WITHIN and BETWEEN RTs with each person's NEUTRAL RT. Does
   grouping *speed up* WITHIN trials, *slow down* BETWEEN trials, or both?

## Five habits to take with you
1. Count before you compute (files, participants, trials, blocks).
2. Look at the extremes (`describe`, histograms): impossible values are clues.
3. Decide exclusion rules before you see results, and log what each one removes.
4. One number per participant first, then across participants.
5. A bug rarely crashes. Check what each step produces, and write checks (`assert`).
""")


# ===========================================================================
# Writing the notebooks
# ===========================================================================
def as_source(text):
    lines = text.split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def build(student):
    cells = []
    for cell in CELLS:
        kind = cell[0]
        if kind == "md":
            cells.append({"cell_type": "markdown", "metadata": {}, "source": as_source(cell[1])})
            continue
        if kind == "code2":
            text = cell[2] if student else cell[1]
        else:
            text = BLANK.sub("___" if student else r"\1", cell[1])
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {},
                      "outputs": [], "source": as_source(text)})
    title = cells[0]["source"]
    if not student:
        title[0] = title[0].rstrip("\n") + " (SOLUTIONS)\n"
    return {
        "cells": cells,
        "metadata": {"colab": {"provenance": []},
                     "kernelspec": {"display_name": "Python 3", "name": "python3"},
                     "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 0,
    }


if __name__ == "__main__":
    for name, student in [("workshop_student.ipynb", True), ("workshop_solutions.ipynb", False)]:
        path = HERE / name
        path.write_text(json.dumps(build(student), indent=1, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print("wrote", path)
