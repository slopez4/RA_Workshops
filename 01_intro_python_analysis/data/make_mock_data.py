"""
Generates reward_task_mock.csv — a FAKE dataset for the workshop.

Instructors only: RAs never need to run this. Re-run it if you want to change
the data (the random seed keeps the output identical every time).

Design of the mock experiment
-----------------------------
- 20 participants (P01-P20), 4 blocks x 20 trials = 80 trials each.
- Each block is either "reward" (earn points for fast, correct answers) or
  "no_reward". Order is counterbalanced: half do reward-first (R, N, R, N),
  half do no-reward-first (N, R, N, R).
- On each trial we record reaction time (rt_ms) and accuracy (correct: 1/0).
- At the end of each block participants rate their motivation (1-7). That
  single rating is repeated on every row of the block, as exported data often is.

Things deliberately hidden in the data (for the "look before you analyze" part)
-------------------------------------------------------------------------------
1. P07 responds at chance (~50% correct) with fast, erratic RTs -> exclude.
2. ~1.5% anticipatory responses (< 150 ms) and ~1% distracted ones (> 3000 ms).
3. ~1.5% missed responses: rt_ms is empty (NaN) and correct = 0.
4. Reward speeds people up and improves accuracy, BUT the reward advantage
   shrinks across blocks, and motivation in no-reward blocks drops over time.
   This is the "motivational shift" hook for the group discussion.
"""

from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(928)

N_PARTICIPANTS = 20
N_BLOCKS = 4
TRIALS_PER_BLOCK = 20
BAD_PARTICIPANT = "P07"

rows = []
for p in range(1, N_PARTICIPANTS + 1):
    pid = f"P{p:02d}"
    reward_first = p % 2 == 1
    order = "reward_first" if reward_first else "no_reward_first"
    base_rt = rng.normal(650, 80)       # each person has their own typical speed
    base_acc = rng.uniform(0.84, 0.93)  # ...and their own typical accuracy
    personal_reward_boost = rng.normal(1.0, 0.35)  # people differ in how much reward matters

    for block in range(1, N_BLOCKS + 1):
        is_reward_block = (block % 2 == 1) == reward_first
        condition = "reward" if is_reward_block else "no_reward"

        # Reward effect shrinks across blocks: -90, -65, -40, -15 ms
        reward_rt_effect = (-90 + 25 * (block - 1)) * personal_reward_boost
        reward_acc_effect = (0.06 - 0.015 * (block - 1)) * personal_reward_boost
        practice_rt = -15 * (block - 1)  # everyone gets a bit faster with practice

        if is_reward_block:
            mean_rt = base_rt + reward_rt_effect + practice_rt
            p_correct = base_acc + reward_acc_effect
            motivation = 5.8 - 0.3 * (block - 1)
        else:
            mean_rt = base_rt + practice_rt
            p_correct = base_acc - 0.01 * (block - 1)
            motivation = 4.8 - 0.5 * (block - 1)

        if pid == BAD_PARTICIPANT:
            mean_rt, p_correct, motivation = 420, 0.50, 2

        rating = int(np.clip(round(rng.normal(motivation, 0.8)), 1, 7))

        for trial in range(1, TRIALS_PER_BLOCK + 1):
            noise_sd = 0.45 if pid == BAD_PARTICIPANT else 0.18
            rt = mean_rt * np.exp(rng.normal(0, noise_sd))
            correct = int(rng.random() < min(p_correct, 0.99))

            roll = rng.random()
            if roll < 0.015:      # anticipatory button press
                rt = rng.uniform(80, 145)
                correct = int(rng.random() < 0.5)
            elif roll < 0.025:    # zoned out
                rt = rng.uniform(3000, 6000)
            elif roll < 0.040:    # no response at all
                rt = np.nan
                correct = 0

            rows.append({
                "participant_id": pid,
                "order": order,
                "block": block,
                "trial": trial,
                "condition": condition,
                "rt_ms": None if np.isnan(rt) else round(rt),
                "correct": correct,
                "motivation_rating": rating,
            })

df = pd.DataFrame(rows)
out = Path(__file__).with_name("reward_task_mock.csv")
df.to_csv(out, index=False)
print(f"Wrote {len(df)} rows to {out}")
