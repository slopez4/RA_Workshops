# Teaching Guide · Workshop 5: Analysis Scripts with Real Data

For whoever runs the session: prep, how to teach the new "predict" format, the answer to
every prompt (with the real numbers), and the errors you'll see.

---

## 1. Before the session

### One week before
- [ ] **Push this folder to GitHub.** Colab opens the notebook from GitHub, and the SETUP
      cell clones the repo to get the data. Unpushed files mean a 404 or an empty folder.
- [ ] **Check that you're allowed to put these data in the repo.** The repo is public
      (Colab needs that). The files are real pilot data with re-coded IDs and no
      demographics, but they are still human-subjects data: confirm that the consent form
      and IRB protocol allow sharing de-identified data, or keep the repo private and run
      the workshop from downloaded copies (see "No GitHub" below).
- [ ] The ID key is **not** in this repo. It lives with the GGP project
      (`RDT/workshop_export/ws05_id_key.csv`, made by `make_ws05_data.py` in the same
      folder). Keep both private: with the script's seed and the original files, anyone
      could rebuild the key.

### Day before
- [ ] Open the [student notebook](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/05_analysis_scripts_ggp/notebooks/workshop_student.ipynb) in an incognito window and run every cell. TODO cells error (expected); the rest should run. The Part 6 TODO cell is only a comment, so it does nothing.
- [ ] Same with the [solutions notebook](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/05_analysis_scripts_ggp/notebooks/workshop_solutions.ipynb): every cell runs, including both `!python` cells in Part 7.

### 10 minutes before
- [ ] Three tabs: slides (`F` fullscreen), your copy of the *student* notebook (fill it in live), the solutions notebook (don't project it).
- [ ] Runtime → Run all once to warm up, then Edit → Clear all outputs.

### No GitHub / no internet?
Download the repo ZIP, open `notebooks/workshop_student.ipynb` in Jupyter or VS Code. The
SETUP cell finds `../data/rawdata` and skips the download.

### Editing the notebooks
Edit `notebooks/build_notebooks.py`, then run `python notebooks/build_notebooks.py`. Both
notebooks are rewritten from the same cells, so the student and solutions versions can't
drift. Don't edit the `.ipynb` files by hand.

---

## 2. How to teach it

Same rhythm as Workshop 1 (**I do, we do, you do**), plus one new move:

**🔮 Predict before you run.** Before running a predict cell, ask everyone to write their
guess in the comment. Then run it. Ask "who was surprised?" and have that person say which
line they misread. Say it out loud: *a wrong prediction is the most useful outcome; it
shows exactly where your mental model of the code differs from Python's.* Keep it to
30–60 seconds per predict cell.

**Real data changes the tone.** Nothing here was planted. When something looks strange,
ask "what happened in the room, or in the code, to produce this?" before "should we
delete it?". The negative RTs are the best example: the answer is a bug in the
experiment, and Workshop 6 fixes it.

**Remind them it's real people's data**, once, at setup: no sharing, no screenshots on
social media.

---

## 3. Answers, part by part

Numbers are from the solutions notebook with the default settings.

### Part 0 · The study
- 🤔 *Where does the repeated pair pop out?* In the WITHIN displays: the two squares sit
  inside one group (close together, same color, same box). In BETWEEN displays the pair
  is split across two groups and is harder to spot. That's the prediction:
  BETWEEN RT > WITHIN RT.

### Part 1 · Predict, then run
- `len(trials)` → `4`; `trials[1]["rt"]` → `1.2` (index 1 is the *second* trial).
- Loop → `within: [0.81]`, `between: [1.2, 1.05]`. The third trial is an error;
  `continue` jumps to the next trial before it's sorted.
- TODO → `effect = mean(between) - mean(within)` → **315 ms** (1.125 − 0.81).
- 🤔 *Why not 395 ms?* 395 ms would include the error trial (0.65 s) in WITHIN:
  (0.81 + 0.65) / 2 = 0.73. Error RTs measure guesses and slips, not how fast the
  repetition was seen.

### Part 2 · Many files
- 26 files. The last is `RDTdata_999.csv`: the **debug ID**, with a header and 0 trials.
  Lab rule (STUDY_CONVENTIONS section 2): 1–100 pilots, 999 debug, 101+ real.
- `first.shape` → `(720, 13)`.
- `[7, 101]`: "007" loses its zeros as a number and stops matching its file name.
- TODO → `"999"` (in quotes: `subject` is text, so `subject == 999` would never be true).
  Result: `25 participants, 19440 trials`.
- 🤔 `path.stem` → `"RDTdata_102"`, `.split("_")` → `["RDTdata", "102"]`, `[1]` → `"102"`.
- **Why skip empty files before `concat`?** With pandas 3, stacking an empty table makes
  the number columns `object` (text-like), and later maths fails in confusing ways
  (`scipy` raises a `dtype('O')` error). Skipping it is the fix.

### Part 3 · Look first
- `value_counts` → 720 trials: 22 people; 1200 trials: 3 people.
- TODO → `n_trials[n_trials > 720]` → **237, 359, 921**. They ran **5 blocks** (early
  pilots, before the task was shortened to 3).
- 🤔 *Options:* keep all (they get more weight and more practice than everyone else),
  drop them (wastes good data), **keep blocks 1–3** (the lab's choice: everyone did the
  same task).
- `describe`: min **−1.152 s**, max **64.785 s**, median 1.02 s.
- Strange trials (`rt < 0.2`): five rows. Two are **negative**: participant 768, block 3,
  trial 1 (−0.94 s) and participant 921, block 3, trial 121 (−1.15 s). Both are errors
  (`ac = 0`).
- 🤔 *What happened?* Trial 1 follows the "About to start block, press space" screen;
  trial 121 follows the "Halfway through this block, press space" screen. The participant
  pressed a **response key** (`n` or `m`) while that screen was up. In `RDT02_Lab.py`,
  `event.waitKeys(keyList=['space'])` only removes space presses from the key buffer, and
  the buffer is only cleared at the *end* of each trial. So the old `n`/`m` press was
  still waiting, became the next trial's answer, and was timestamped before that trial's
  clock started: a negative RT. **It's an experiment bug, not participant behaviour.**
  Workshop 6 shows the fix (`kb.clearEvents()` right before the display, and starting
  the RT clock on the flip).
- The 64.8 s trial (participant 921, block 5): someone looked away for a minute. It's
  outside blocks 1–3 anyway.
- TODO → `sort_values("accuracy")`. Lowest: **726** (0.829 correct, 24% of trials slower
  than 5 s), 768 (0.868), 370 (0.869).
- 🤔 *Exclude 726?* No single right answer. Chance is 50%, so 83% is clearly doing the
  task; their slow trials will be removed by the RT rule anyway. The point is **when** to
  decide: now, as a rule (`MIN_ACCURACY`), before seeing anyone's effect. The notebook
  uses 0.80, which keeps everyone.

### Part 4 · Clean with a log
- TODO → `&`.
- Log: blocks 1–3 → 18,000 trials, 25 people; accuracy rule → 18,000, 25; correct trials →
  17,148, 25; RT window → **16,726**, 25.
- 🤔 *Share lost:* (18,000 − 16,726) / 18,000 = **7.1%**. Errors removed the most (852);
  the RT window removed 422. A person who loses far more trials than the rest has noisier
  means; report it, and consider a minimum-trials rule (decided in advance).

### Part 5 · The effect
- TODO 1 → `means["BETWEEN"] - means["WITHIN"]`. TODO 2 → `effects > 0`.
- Summary (ms, mean ± SEM, positive / 25):

  | cue | mean | SEM | positive |
  |---|---|---|---|
  | SIM | 559 | 47 | 25 |
  | SYNCHRONY | 390 | 45 | 25 |
  | CR | 364 | 45 | 24 |
  | PROX | 351 | 31 | 25 |
  | COMMONFATE | 215 | 27 | 24 |
  | IPG | 169 | 33 | 23 |
  | EC | 111 | 39 | 18 |

- 🤔 *Why per person first?* (1) People with more kept trials would weigh more.
  (2) The SEM would treat ~16,700 trials as independent; the sample is 25 people.
- 🤔 *Strongest / weakest:* SIM strongest; EC weakest, and **7 of 25** people show EC in
  the wrong direction. The bar alone hides that.
- t-tests: all p < .01 (EC t = 2.83, p = .009; the rest t > 5).

### Part 6 · Find the bugs
Buggy output: `trials used: 11322 | slowest RT kept: 36.4`, every effect negative.

| Bug | Symptom | Fix | Check |
|---|---|---|---|
| `df["block"] < 3` keeps blocks 1–2 | 11,322 trials instead of 16,726 | `<= 3` | `assert keep["block"].max() == 3` |
| `\|` (OR) in the RT filter keeps every trial | slowest RT kept is 36 s | `&` | `assert keep["rt"].between(0.2, 5.0).all()` |
| `WITHIN - BETWEEN` | all effects negative | `BETWEEN - WITHIN` | compare the sign with the prediction |

Fixed output matches Part 5 (SIM 559 … EC 111). 🤔 *Which bug changes the conclusion?*
Only the sign flip. Bugs 1 and 2 quietly change the numbers, which makes them more
dangerous: nobody looks twice at a plausible number.

If RAs are stuck: "run the first line on its own and print `keep['block'].unique()`."

### Part 7 · Script and robustness
- Default run prints the same summary as Part 5 and writes `prettydata/` and `figtree/`.
- `--max-rt 2` (16,726 → 14,836 trials):

  | cutoff | SIM | SYNC | CR | PROX | CF | IPG | EC |
  |---|---|---|---|---|---|---|---|
  | 5 s | 559 | 390 | 364 | 351 | 215 | 169 | 111 |
  | 2 s | 302 | 200 | 100 | 229 | 155 | 114 | 78 |

- 🤔 1. Every effect roughly halves; **CR falls from 3rd to 6th**. 2. Slow trials are
  mostly BETWEEN trials (69% of correct trials between 2 and 5 s), so cutting them removes
  the largest differences. 3. Choose the cutoff before seeing results (ideally
  preregistered), report it, and show the main conclusion under a second reasonable
  cutoff. Here "every cue groups" survives; "CR is the third strongest cue" does not.

### ⭐ Stretch (for you)
1. Accuracy: `groupby([...])["ac"].mean()` on blocks 1–3 *before* removing errors;
   effect = WITHIN − BETWEEN accuracy (positive = more accurate within a group).
2. Reliability: effects on block 1 vs block 3 per person, `.corr()` per cue.
3. Baseline: per person, (WITHIN − NEUTRAL) and (BETWEEN − NEUTRAL).

---

## 4. Common errors

| Error | Cause | Fix |
|---|---|---|
| `NameError: name 'df' is not defined` | Skipped a cell | Runtime → Run before |
| `ValueError: No objects to concatenate` | Wrong folder; SETUP not run | Re-run SETUP; `print(DATA_DIR, list(DATA_DIR.glob("*")))` |
| `CalledProcessError … git clone` | Runtime has no internet, or repo not public | Runtime → Restart; check the repo URL in a browser |
| `TypeError` with `___` | Blank not filled | Fill it in |
| `ValueError: The truth value of a Series is ambiguous` | `and`/`or` instead of `&`/`\|`, or missing brackets | `(a) & (b)` |
| `KeyError: 'BETWEEN'` | `unstack` on the wrong level or skipped | Re-run the `unstack("wbn")` cell once (running it twice also fails: the level is gone) |
| `!python` cell prints nothing | `SCRIPT` path wrong | `print(SCRIPT, SCRIPT.exists())` |
