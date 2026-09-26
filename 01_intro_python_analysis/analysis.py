"""
analysis.py — Reward task: from raw file to results.

This is the workshop notebook boiled down to a plain script. A script runs
top to bottom every time, so anyone can reproduce the exact same results.

Run it in Colab (in any code cell):
    !wget -q https://raw.githubusercontent.com/slopez4/RA_Workshops/main/01_intro_python_analysis/analysis.py
    !python analysis.py
Run it on a computer:   python analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. SETTINGS — every decision lives here, at the top, where people can see it
# ---------------------------------------------------------------------------
DATA_URL = ("https://raw.githubusercontent.com/slopez4/RA_Workshops/main/"
            "01_intro_python_analysis/data/reward_task_mock.csv")
MIN_ACCURACY = 0.60   # participants below this are treated as guessing
MIN_RT = 150          # ms; faster than this is an anticipatory press
MAX_RT = 2500         # ms; slower than this means they weren't paying attention

# ---------------------------------------------------------------------------
# 2. LOAD
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_URL)
print(f"Loaded {len(df)} rows from {df['participant_id'].nunique()} participants")

# ---------------------------------------------------------------------------
# 3. CHECK — can we trust this data?
# ---------------------------------------------------------------------------
print("\nMissing values per column:")
print(df.isna().sum())

acc_by_participant = df.groupby("participant_id")["correct"].mean()
excluded = acc_by_participant[acc_by_participant < MIN_ACCURACY].index.tolist()
print(f"\nParticipants below {MIN_ACCURACY:.0%} accuracy: {excluded}")

# ---------------------------------------------------------------------------
# 4. CLEAN
# ---------------------------------------------------------------------------
clean = df[
    ~df["participant_id"].isin(excluded)
    & (df["rt_ms"] >= MIN_RT)
    & (df["rt_ms"] <= MAX_RT)
].copy()
print(f"Kept {len(clean)} of {len(df)} trials after cleaning")

half_of_block = {1: "1st half", 2: "1st half", 3: "2nd half", 4: "2nd half"}
clean["half"] = clean["block"].map(half_of_block)

# ---------------------------------------------------------------------------
# 5. ANALYZE — one number per participant first, then average across people
# ---------------------------------------------------------------------------
per_person = clean.groupby(["participant_id", "condition"])["rt_ms"].mean().unstack()
per_person["reward_effect"] = per_person["reward"] - per_person["no_reward"]
n_faster = (per_person["reward_effect"] < 0).sum()

print("\nMean RT per condition (ms):")
print(per_person[["no_reward", "reward"]].mean().round(0))
print(f"{n_faster} of {len(per_person)} participants were faster with reward")

by_half = clean.groupby(["participant_id", "half", "condition"])["rt_ms"].mean().unstack()
by_half["reward_effect"] = by_half["reward"] - by_half["no_reward"]
print("\nReward effect across the session (ms, negative = faster with reward):")
print(by_half.groupby("half")["reward_effect"].mean().round(0))

ratings = clean.drop_duplicates(["participant_id", "block"])
motivation = ratings.groupby(["half", "condition"])["motivation_rating"].mean().unstack()
print("\nMean motivation rating (1-7):")
print(motivation.round(2))

# ---------------------------------------------------------------------------
# 6. PLOT — saved as image files so they can go straight into slides
# ---------------------------------------------------------------------------
fig, ax = plt.subplots()
for pid, row in per_person.iterrows():
    ax.plot(["no_reward", "reward"], [row["no_reward"], row["reward"]],
            color="gray", alpha=0.5, marker="o")
ax.plot(["no_reward", "reward"],
        [per_person["no_reward"].mean(), per_person["reward"].mean()],
        color="black", linewidth=3, marker="o")
ax.set_ylabel("Mean reaction time (ms)")
ax.set_title("Reward effect (each gray line is one participant)")
fig.savefig("fig_reward_effect.png", dpi=150, bbox_inches="tight")

fig, ax = plt.subplots()
motivation.plot(kind="bar", rot=0, ax=ax)
ax.set_ylabel("Mean motivation rating (1-7)")
ax.set_title("Self-reported motivation across the session")
fig.savefig("fig_motivation.png", dpi=150, bbox_inches="tight")

print("\nSaved fig_reward_effect.png and fig_motivation.png")
