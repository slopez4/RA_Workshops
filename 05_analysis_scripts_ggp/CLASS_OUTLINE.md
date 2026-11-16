# Class Outline · Workshop 5: Reading and Writing Analysis Scripts with Real Data

## Session overview

| | |
|---|---|
| **Topic** | Practising analysis code on real data: load many files, check, clean, compute a per-participant effect, find bugs, turn it into a script |
| **Audience** | Research assistants who did Workshop 1 (or know variables, lists, loops, `groupby`) |
| **Format** | Live code-along in Google Colab (browser only, nothing to install) |
| **Length** | ~55 min core + 5 min buffer |
| **Data** | 25 real GGP/RDT pilot participants, IDs re-coded, demographics removed |
| **Materials** | [Slides](https://slopez4.github.io/RA_Workshops/05_analysis_scripts_ggp/slides.html) · [Student notebook](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/05_analysis_scripts_ggp/notebooks/workshop_student.ipynb) · [`rdt_analysis.py`](rdt_analysis.py) · [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) |

## Learning goals

By the end, RAs will be able to:

1. **Predict** what a short block of code (loop, `if`/`continue`, function) will output before running it.
2. **Load** one file per participant into one table, and skip debug IDs and empty files on purpose.
3. **Check** a real dataset (counts per participant, blocks, extremes, per-person accuracy) and explain strange values in terms of how the data were collected.
4. **Clean** with rules written in settings before seeing results, and report what each rule removed.
5. **Compute** a within-participant effect with `groupby` → `unstack` → subtract, summarize across people, and plot individuals.
6. **Debug** code that runs but is wrong, by checking what each step produces, and write `assert`s that catch it.
7. **Read** an analysis script (header, settings, functions, `main`) and test whether its conclusion survives a different reasonable setting.

## Agenda

| Time | Part | What happens | Coding ideas | Data-thinking idea |
|---|---|---|---|---|
| 0:00–0:03 | **Setup** | Open Colab, save a copy, run SETUP | — | Real data: handle with care |
| 0:03–0:06 | **0. The study** | Displays, WITHIN vs BETWEEN, the prediction | (reading a plotting function) | What one trial is; what the effect means |
| 0:06–0:13 | **1. Predict, then run** | 4 toy trials; loop with `continue`; a `mean` function | lists of dicts, `for`, `if`/`continue`, `def`/`return`, f-strings | Why error trials are left out of RTs |
| 0:13–0:20 | **2. Many files** | `glob` → loop → `concat`; IDs as text | `Path.glob`, `.stem.split`, `dtype=str`, `pd.concat` | The debug file; leading zeros |
| 0:20–0:28 | **3. Look first** | Trials per person, blocks, `describe`, strange RTs, per-person accuracy | `size`, `value_counts`, boolean indexing, `sort_values` | 5-block pilots; negative RTs; when to exclude a person |
| 0:28–0:33 | **4. Clean with a log** | Settings cell; four filters, each logged | `&`, `~`, `isin` | Decide before results; report what was removed |
| 0:33–0:41 | **5. The effect** | Per-person means → effect → summary → plot; optional t-test | `groupby` on 3 columns, `unstack`, `sem`, `dropna` | Per person first; the bar hides 7 of 25 people for EC |
| 0:41–0:49 | **6. Find the bugs** | A function that runs but has 3 bugs | `assert`, checking intermediate results | Silent bugs are the dangerous ones |
| 0:49–0:55 | **7. Script + robustness** | Run `rdt_analysis.py`, then with `--max-rt 2` | script anatomy, command-line options | A cutoff can change the ranking; decide and report it |
| 0:55–1:00 | **Wrap-up / buffer** | Five habits; point to stretch | — | — |

## Where to cut if time runs short

- Part 0: show the display slide instead of running the plotting cell.
- Part 1: do the `mean` TODO yourself; keep the 315 vs 395 ms question.
- Part 3: skip the histogram.
- Part 5: skip the t-test cell.
- Part 7: show the robustness table on the slide instead of running the script twice.
- **Don't cut** Part 3's strange RTs or Part 6 (the bugs): they are the point of using real data.

## After the session

- RAs keep their Colab copy. Solutions notebook linked in the README.
- Optional homework: the ⭐ stretch exercises.
- Bridge to [Workshop 6](../06_advanced_psychopy/): the negative RTs were an experiment bug, fixed there.
