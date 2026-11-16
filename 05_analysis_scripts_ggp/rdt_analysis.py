"""
Project:       RA Workshops, Workshop 5 (real data from the lab's GGP study)
Script:        05_analysis_scripts_ggp/rdt_analysis.py
Creator:       <name> (AI-assisted: Claude)
Purpose:       The whole workshop analysis as one script. Reads every participant
               file in data/rawdata/, checks and cleans the trials, computes the
               grouping effect (BETWEEN - WITHIN reaction time) for each cue, and
               writes tables to prettydata/ and a figure to figtree/
               (rawdata -> prettydata -> figtree).
Last updated:  2026-11-15

Usage (example):
    python rdt_analysis.py                    the analysis with the settings below
    python rdt_analysis.py --max-rt 3         a stricter slow-RT cutoff (seconds)
    python rdt_analysis.py --min-acc 0.85     a stricter accuracy rule

    In Colab, after cloning the repo:
    !python RA_Workshops/05_analysis_scripts_ggp/rdt_analysis.py

Dependencies:  pandas, matplotlib, scipy (all preinstalled in Colab)
Reads:         data/rawdata/RDTdata_<id>.csv
Writes:        prettydata/rdt_cleaning_log.csv
               prettydata/rdt_effects_by_subject.csv
               prettydata/rdt_effects_summary.csv
               figtree/rdt_effects_by_cue.png
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # save figures to files; no screen needed
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# ---------------------------------------------------------------------------
# 1. SETTINGS: every analysis decision lives here, decided before looking at
#    the results. Change them here, never further down.
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent          # paths come from this file's
RAW_DIR = HERE / "data" / "rawdata"             # location, not the folder you
TABLE_DIR = HERE / "prettydata"                 # launched Python from
FIG_DIR = HERE / "figtree"

DEBUG_IDS = ["999"]   # reserved for test runs; never analysed
N_BLOCKS = 3          # early pilots ran 5 blocks, later ones 3: keep the first 3 for everyone
MIN_RT = 0.2          # seconds; faster than this is a press before the display was seen
MAX_RT = 5.0          # seconds; slower than this means attention wandered (the lab's cutoff)
MIN_ACCURACY = 0.80   # proportion correct; chance is 0.50 (two shapes)


def parse_args():
    """Optional command-line overrides for the RT and accuracy rules."""
    parser = argparse.ArgumentParser(description="RDT grouping-effect analysis.")
    parser.add_argument("--max-rt", type=float, default=MAX_RT, help="slow-RT cutoff (s)")
    parser.add_argument("--min-acc", type=float, default=MIN_ACCURACY,
                        help="minimum proportion correct per participant")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# 2. LOAD: one file per participant, stacked into one table
# ---------------------------------------------------------------------------
def load_all(folder):
    """Read every RDTdata_<id>.csv in `folder` into one DataFrame.

    Skips debug IDs and files with no trials. subjectId is read as text so an
    ID like "007" keeps its leading zeros. rt is in seconds.
    """
    tables = []
    for path in sorted(folder.glob("RDTdata_*.csv")):
        df = pd.read_csv(path, dtype={"subjectId": str})
        subject = path.stem.split("_")[1]          # "RDTdata_102" -> "102"
        if subject in DEBUG_IDS or df.empty:
            print(f"  skipped {path.name} ({len(df)} trials)")
            continue
        tables.append(df)
    return pd.concat(tables, ignore_index=True)


# ---------------------------------------------------------------------------
# 3. CHECK and 4. CLEAN: every step is counted, so the cleaning can be reported
# ---------------------------------------------------------------------------
def clean_trials(df, max_rt, min_acc):
    """Apply the exclusion rules in order. Returns (clean trials, log table).

    Accuracy is judged on all kept-block trials, before any RT trimming.
    """
    log = [("all trials", len(df), df["subjectId"].nunique())]

    df = df[df["block"] <= N_BLOCKS]
    log.append((f"blocks 1-{N_BLOCKS} only", len(df), df["subjectId"].nunique()))

    accuracy = df.groupby("subjectId")["ac"].mean()
    low = accuracy[accuracy < min_acc].index
    df = df[~df["subjectId"].isin(low)]
    log.append((f"participants with accuracy >= {min_acc:.0%}", len(df),
                df["subjectId"].nunique()))

    df = df[df["ac"] == 1]
    log.append(("correct trials only", len(df), df["subjectId"].nunique()))

    df = df[(df["rt"] >= MIN_RT) & (df["rt"] <= max_rt)]
    log.append((f"RT between {MIN_RT} and {max_rt} s", len(df), df["subjectId"].nunique()))

    log = pd.DataFrame(log, columns=["step", "trials_left", "participants_left"])
    return df.copy(), log


# ---------------------------------------------------------------------------
# 5. ANALYZE: one number per participant first, then across participants
# ---------------------------------------------------------------------------
def grouping_effects(df):
    """Grouping effect per participant and cue, in milliseconds.

    effect = mean RT on BETWEEN trials - mean RT on WITHIN trials.
    Positive = the repeated pair was found faster when it sat inside one group.
    NEUTRAL trials have no BETWEEN/WITHIN, so they drop out here.
    """
    cued = df[df["cueType"] != "NEUTRAL"]
    means = cued.groupby(["subjectId", "cueType", "wbn"])["rt"].mean().unstack("wbn")
    effect = (means["BETWEEN"] - means["WITHIN"]) * 1000
    return effect.unstack("cueType")     # rows = participants, columns = cues


def summarize(effects):
    """Group mean, SEM, how many participants show the effect, and a t-test."""
    rows = []
    for cue in effects.columns:
        values = effects[cue].dropna()
        t, p = stats.ttest_1samp(values, 0)
        rows.append({"cue": cue, "n": len(values),
                     "mean_ms": values.mean(), "sem_ms": values.sem(),
                     "n_positive": int((values > 0).sum()), "t": t, "p": p})
    return pd.DataFrame(rows).sort_values("mean_ms", ascending=False)


# ---------------------------------------------------------------------------
# 6. PLOT: every participant as a dot, the group mean as a bar
# ---------------------------------------------------------------------------
def plot_effects(effects, summary, path):
    order = summary["cue"].tolist()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(range(len(order)), summary["mean_ms"], yerr=summary["sem_ms"],
           color="#cfd8e8", edgecolor="#4a5a78", capsize=4, zorder=1)
    for i, cue in enumerate(order):
        y = effects[cue].dropna()
        x = [i + (j % 5 - 2) * 0.06 for j in range(len(y))]   # small spread so dots don't overlap
        ax.scatter(x, y, s=14, color="#2f4a7f", alpha=0.6, zorder=2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(range(len(order)), order, rotation=30, ha="right")
    ax.set_ylabel("Grouping effect (ms)\nBETWEEN - WITHIN")
    ax.set_title("Each dot is one participant; bars are the group mean ± SEM")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7. RUN: the steps above, top to bottom
# ---------------------------------------------------------------------------
def main():
    args = parse_args()
    TABLE_DIR.mkdir(exist_ok=True)
    FIG_DIR.mkdir(exist_ok=True)

    print(f"Reading {RAW_DIR}")
    raw = load_all(RAW_DIR)
    trials_per_subject = raw.groupby("subjectId").size()
    print(f"Loaded {len(raw)} trials from {raw['subjectId'].nunique()} participants")
    print("Trials per participant:", trials_per_subject.value_counts().to_dict())

    clean, log = clean_trials(raw, args.max_rt, args.min_acc)
    print("\nCleaning log:")
    print(log.to_string(index=False))

    effects = grouping_effects(clean)
    summary = summarize(effects)
    print("\nGrouping effect per cue (ms, positive = faster WITHIN a group):")
    print(summary.round({"mean_ms": 0, "sem_ms": 0, "t": 2, "p": 4}).to_string(index=False))

    log.to_csv(TABLE_DIR / "rdt_cleaning_log.csv", index=False)
    effects.round(1).to_csv(TABLE_DIR / "rdt_effects_by_subject.csv")
    summary.to_csv(TABLE_DIR / "rdt_effects_summary.csv", index=False)
    plot_effects(effects, summary, FIG_DIR / "rdt_effects_by_cue.png")
    print(f"\nTables in {TABLE_DIR}\nFigure in {FIG_DIR}")


if __name__ == "__main__":
    main()
