# Teaching Guide — Intro to Simple Analysis Scripts

For whoever is running the session. Covers prep, how to teach it, a minute-by-minute
script, the answer to every 🤔 prompt, and fixes for the errors you'll see.

---

## 1. Before the session

### One week before
- [ ] **Push this folder to GitHub, and make sure the repo is public.** Colab opens notebooks
      from GitHub, and the notebook loads the data from a GitHub URL. A private repo or
      unpushed files give a 404.
- [ ] Ask RAs to confirm they can sign in to a Google account in a browser (personal
      Gmail is fine; some university accounts block Colab — personal is safer).

### Day before
- [ ] Open the [student notebook](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/01_intro_python_analysis/notebooks/workshop_student.ipynb)
      in an **incognito window** and run every cell. The TODO cells will error (that's
      expected); everything else should run.
- [ ] Do the same with the [solutions notebook](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/01_intro_python_analysis/notebooks/workshop_solutions.ipynb) — every cell should run.
- [ ] Put the Colab link somewhere easy (calendar invite, Slack/Teams, a short link, or a QR code on the first slide).

### 10 minutes before
- [ ] Open **three tabs**: the [slides](https://slopez4.github.io/RA_Workshops/01_intro_python_analysis/slides.html) (press `F` for fullscreen, arrow keys to move; answers are hidden behind *What we found* toggles until you click them), your own saved copy of the *student* notebook (you'll fill it in live), and the *solutions* notebook (your cheat sheet — don't project it).
- [ ] Tip: during class, share the slides link too. RAs can press `R` for the reference view and keep the cheat sheet and common-errors pages open beside Colab.
- [ ] Browser zoom to 125–150% so code is readable on the projector / screen-share.
- [ ] In Colab: **Runtime → Run all** once in your copy so the runtime is warm, then **Edit → Clear all outputs** so RAs see a fresh notebook.
- [ ] Have a co-instructor or experienced RA ready to float, if possible.

---

## 2. How to teach it

**Live-code, don't lecture.** Keep the notebook on screen and run cells as you talk. RAs follow along in their own copy.

**Rhythm for each part — "I do, we do, you do":**
1. **I do** — run the demo cell, say out loud what each line does in plain English.
2. **We do** — ask the 🤔 question. Wait (count to 5 in your head). Take 1–2 answers.
3. **You do** — for a `# TODO` cell, give **60–90 seconds**. Then fill it in on your screen so nobody falls behind.

**Signals:** ask RAs to give a 👍 (Zoom reaction or thumbs up in the room) when a cell runs,
and a ✋ when stuck. Move on when most thumbs are up; the floater helps the rest.

**Language to use:**
- "A DataFrame is an Excel sheet that Python can talk to."
- "`groupby` = sort the rows into piles, then do the same calculation on every pile."
- "An error is Python telling you exactly what confused it. Read the last line."
- Avoid: "just", "simply", "obviously". Nothing is obvious the first time.

**Keep the data questions front and center.** The syntax will be forgotten; the habits
(*check counts, look at distributions, decide exclusions before results, summarize per
person, plot individuals*) are the point. When in doubt, spend time on 🤔 prompts rather than
on syntax.

**If RAs are fast:** point them at the ⭐ stretch cell at the end.
**If RAs are stuck:** tell them to copy the line from your screen — understanding comes on the second pass, and the solutions notebook is always available.

---

## 3. Minute-by-minute script

### 0:00–0:03 · Setup
- Share the link. Walk through: sign in → open → *Run anyway* → **File → Save a copy in Drive**.
- Emphasize: "Work in your copy — the tab title should say *Copy of…*"
- Show **Shift + Enter** on the first code cell. Wait for 👍s.

### 0:03–0:10 · Part 0 — Python in 5 minutes
- **Variables cell:** "The `=` sign means *store*, not *equals*. The name goes on the left."
- **List cell:** stop on `rts[0]`. "Python starts counting at zero — this trips everyone up once."
- **TODO `min`:** 60 s. Answer: `print(min(rts))` → `101`.
- 🤔 *Which RTs are suspicious?* → **101 ms** (faster than humanly possible to see and respond — likely an anticipatory press) and **2950 ms** (they were probably distracted). "Hold onto this — the real data has the same problems."
- **Loop cell:** point at the indentation. "The 4 spaces are how Python knows what's inside the loop. Most beginner errors are indentation."
- **TODO `elif`:** 90 s. Answer: `elif rt > 2500:`. Point out the colon.

### 0:10–0:15 · Part 1 — Bring the data in
- **Import cell:** "Nobody writes everything from scratch. `import` borrows a toolbox."
- **Load cell:** "One line brought in 1,600 rows. That's the payoff."
- Read the codebook table together. 🤔 *What is one row?* → **one trial** for one participant.
- **TODO `df.shape`:** → `(1600, 8)`.
- `value_counts`: every participant has **80** rows. 🤔 20 × 4 × 20 = **1600** ✔. "Always check the counts add up — it's how you catch a missing file or a double-merged one."

### 0:15–0:22 · Part 2 — Look before you analyze
- **`describe()`** — 🤔 on `rt_ms`:
  - **min = 81 ms** (impossible), **max = 5944 ms** (almost 6 seconds — zoned out).
  - `rt_ms` **count = 1579**, others 1600 → **21 missing** RTs (no response).
- **`isna().sum()`** confirms 21 missing, all in `rt_ms`.
- **Histogram:** most trials 400–900 ms with a long right tail; a small cluster near 100. "This is what RT data always looks like — skewed right."
- **Accuracy per participant** — 🤔:
  - **P07 = 48.75%**. Everyone else is **80–94%**.
  - Two buttons → guessing gives **50%**. P07 was guessing (not paying attention, misunderstood instructions, or pressing randomly).
  - *Why decide before seeing the results?* If you drop people **after** seeing which way they push the effect, you can manufacture any result you want. Exclusion rules should be written in advance (ideally preregistered).

### 0:22–0:27 · Part 3 — Clean the data
- `too_fast.sum()` → **24** trials < 150 ms.
- **TODO:** `too_slow = df["rt_ms"] > 2500` → **21** trials.
- **Cleaning cell:** read the filter aloud: "Keep rows where the participant is **not** excluded, **and** RT ≥ 150, **and** RT ≤ 2500."
  - "We wrote the *rule* (< 60%), not the *name* P07. If more data comes in, the rule still works, and a reader can see exactly what we did."
  - `.copy()` — "makes `clean` its own table so we can add columns later without warnings." Don't go deeper.
  - Result: **1600 → 1458 rows**.
- 🤔 *Where did the missing RTs go?* An empty cell is not `>= 150`, so the comparison is `False` and those rows are dropped automatically.
  *Is that right for accuracy?* Debatable — a missed response is arguably an error. For RT, dropping is correct (there is no RT). Good lesson: **every cleaning step is a decision**, and the same rule can be right for one measure and wrong for another. Write it down either way.

### 0:27–0:33 · Part 4 — Does reward change behavior?
- **Condition means:** reward **598 ms / 91.5%** vs. no-reward **645 ms / 86.7%**. Faster *and* more accurate with reward — so it's not just a speed–accuracy trade-off (worth saying out loud).
- **Per person:** "If one person had 80 trials and another had 40 after cleaning, a trial-level average weights them unequally. One number per person makes everyone count once." `unstack()` = pivot table.
- **TODO:** `(per_person["reward_effect"] < 0).sum()` → **17 of 19**.
- **Spaghetti plot** — 🤔 *Does everyone show it?* Most lines go down; **2** go up, and the size of the drop varies a lot. "An average of −47 ms can hide people with no effect at all. Plot individuals."
- Note the `for` loop: "This is the same loop from Part 0, doing real work now."

### 0:33–0:37 · Part 5 — Does the effect change over time?
- Explain the design point: every participant has one reward and one no-reward block **in each half**, so we can compare within people.
- **Dictionary cell** — "a lookup table: give it a block, get back the half."
- **Result:**

  | half | no_reward | reward | reward effect |
  |---|---|---|---|
  | 1st | 658 ms | 594 ms | **−64 ms** |
  | 2nd | 631 ms | 601 ms | **−30 ms** |

  The reward advantage roughly **halves**.
- **Motivation cell** — `drop_duplicates`: "The rating was asked once per block but copied onto 20 rows. Keep one row per person per block, so we count each rating once."

  | half | no_reward | reward |
  |---|---|---|
  | 1st | 5.00 | 5.37 |
  | 2nd | **3.58** | 5.00 |

- 🤔 Discussion prompts — collect ideas, **don't resolve them**; hand them to the post-talk discussion:
  1. *Why does the advantage shrink?* Candidate answers: fatigue; habituation to the reward (it loses its value); practice makes everyone fast, leaving less room to speed up (floor effect); no-reward blocks become relatively *less* motivating; strategy change.
  2. *Which condition changed more?* **No-reward** motivation dropped ~1.4 points; reward dropped ~0.4. Interesting: yet no-reward **RT got faster** (practice). So self-reported motivation and behaviour don't move together — a nice tension for the discussion.
  3. *How would you tell explanations apart?* Ideas: a no-reward-only control group (pure practice/fatigue); varying reward size over time; adding rest breaks; measuring effort physiologically (pupil, grip force); asking about reward value, not just motivation.
- ⭐ **Stretch answer (accuracy by half):** the accuracy advantage stays about **+5 points** in both halves — so the *speed* benefit of reward fades but the *accuracy* benefit doesn't. Another good discussion seed.

### 0:37–0:40 · Wrap-up
- Open [`analysis.py`](analysis.py) on GitHub. "This is the whole workshop as a script. Settings at the top, then load, check, clean, analyze, plot. You now recognise every line."
- Read the **5 habits** at the bottom of the notebook.
- Hand off to Christian: "Keep the Part 5 question in mind — why would reward's effect change over a session? — Christian's project is about exactly this kind of thing."

---

## 4. Common errors and fixes

| What they see (last line of the error) | Why | Fix |
|---|---|---|
| `NameError: name 'pd' is not defined` (or `df`, `clean`, `rts`…) | Skipped a cell, or the runtime restarted | Click the cell, then **Runtime → Run before** |
| `SyntaxError: invalid syntax` pointing at `___` | Ran a TODO cell without filling the blank | Fill in the blank and re-run |
| `IndentationError` | Loop/if body not indented, or mixed spacing | Select the lines and press **Tab** / **Shift+Tab** to align |
| `SyntaxError: expected ':'` | Missing colon after `for …`, `if …`, `elif …` | Add the `:` at the end of the line |
| `KeyError: 'rt'` / `'Condition'` | Column name typo — names must match exactly, case included | Copy the name from `df.columns` |
| `HTTPError: HTTP Error 404` on `read_csv` | Repo private, or data not pushed | Make repo public / push; or upload the CSV via the 📁 sidebar and use `pd.read_csv("reward_task_mock.csv")` |
| Colab: *"not authored by Google"* | Normal for any GitHub notebook | Click **Run anyway** |
| Colab: *"Runtime disconnected"* | Idle too long | Reconnect, then **Runtime → Run before** |
| Changes disappeared | Worked in the original instead of *Save a copy in Drive* | **File → Save a copy in Drive** now; redo is quick with the solutions |
| Pink `SettingWithCopyWarning` box | Made `clean` without `.copy()` | It's a warning, not an error; results are fine. Add `.copy()` |

---

## 5. Access options, in order of preference

1. **Google Colab** (recommended) — free, fast, saves to Drive, nothing to install. Needs a Google account.
2. **Binder** (backup, no account) — [launch link](https://mybinder.org/v2/gh/slopez4/RA_Workshops/main?labpath=01_intro_python_analysis%2Fnotebooks%2Fworkshop_student.ipynb). Takes 1–2 min to start the first time, and does **not** save work — download the notebook before closing. Uses `requirements.txt` at the repo root.
3. **Pair up** — if a laptop or account fails, pair that RA with a neighbour. Pairing is often better for learning anyway.

---

## 6. Changing the materials

- **Notebooks:** edit in Colab (*File → Save a copy in GitHub*) or Jupyter, and keep the student and solutions versions in sync.
- **Data:** edit [`data/make_mock_data.py`](data/make_mock_data.py) and re-run it. The numbers in this guide come from seed `928` — if you change the seed or the effects, re-run the solutions notebook and update the answers above.
