# Workshop 5: Reading and Writing Analysis Scripts with Real Data

**Length:** ~55 min · **No installation needed** (Google Colab)

**📊 Slides / reference guide:** [open the slides](https://slopez4.github.io/RA_Workshops/05_analysis_scripts_ggp/slides.html). Press `R` to switch between slide view and a scrollable reference page (cheat sheet, common errors).

Workshop 1 used fake data with planted problems. This time the data are **real**: 25
pilot participants from the lab's gestalt grouping study (GGP), which uses the
**Repetition Discrimination Task (RDT)**. You'll load one file per participant, check
them, clean them, and ask whether grouping cues make a repeated shape easier to see.
Along the way you'll practise *reading* code: predicting what a cell will do before
running it, and finding bugs in a script that runs without errors but gives the wrong
answer.

---

## Start here (3 minutes)

1. Open the workshop notebook:

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/05_analysis_scripts_ggp/notebooks/workshop_student.ipynb)

2. If Colab says *"This notebook was not authored by Google"*, click **Run anyway**.
3. **File → Save a copy in Drive**, and work in your copy.
4. Run the **SETUP** cell. It downloads the data (about 10 seconds).

---

## About the data

- **Real participants.** Their IDs were replaced with new random codes; only the
  instructor holds the key. Age and sex were removed. Please keep the files inside the
  workshop: don't share or post them.
- Codebook and file list: [`data/README.md`](data/README.md).
- Nothing was cleaned or changed apart from the IDs. The problems you'll find
  (participants who ran extra blocks, negative and 65-second reaction times, an empty
  debug file) are what the experiment really wrote.

## What's in this folder

| File | What it is | Who it's for |
|---|---|---|
| [`notebooks/workshop_student.ipynb`](notebooks/workshop_student.ipynb) | The notebook we work through, with blanks (`___`) and 🔮 predict cells | RAs |
| [`notebooks/workshop_solutions.ipynb`](notebooks/workshop_solutions.ipynb) | Same notebook, blanks filled in, bugs fixed | Checking your work afterward |
| [`rdt_analysis.py`](rdt_analysis.py) | The whole analysis as one script with a header, settings and functions | Everyone, after the workshop |
| [`data/rawdata/`](data/rawdata/) | 25 participant files + the empty debug file `RDTdata_999.csv` | — |
| [`slides.html`](https://slopez4.github.io/RA_Workshops/05_analysis_scripts_ggp/slides.html) | Slides + reference page | Everyone |
| [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md) | Goals, timing, agenda | Everyone |
| [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) | How to run it, answers to every prompt, common errors | Instructors |
| [`notebooks/build_notebooks.py`](notebooks/build_notebooks.py) | Writes both notebooks from one list of cells | Instructors (edit here, not the .ipynb) |

[![Open solutions in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/05_analysis_scripts_ggp/notebooks/workshop_solutions.ipynb) ← solutions

Running `rdt_analysis.py` writes tables to `prettydata/` and a figure to `figtree/`
(both git-ignored; they're regenerated every run).

## What you'll be able to do afterward

- Predict what a short piece of code does before running it
- Read and write loops, `if`/`continue`, dictionaries and functions
- Load and combine one file per participant, skipping debug and empty files
- Check counts and extremes, and explain a strange value instead of ignoring it
- Clean data with rules decided in advance, and log what each rule removes
- Compute an effect per participant, then across participants, and plot both
- Find bugs that don't crash, and write `assert` checks that would catch them
- Read an analysis script's header, settings and functions, and test how robust its answer is

## Keep practicing

- The ⭐ stretch exercises at the end of the notebook (accuracy, reliability, NEUTRAL baseline).
- Read [`rdt_analysis.py`](rdt_analysis.py) top to bottom and change one setting at a time.
- Next: [Workshop 6](../06_advanced_psychopy/) finds the experiment bug behind today's negative RTs.
