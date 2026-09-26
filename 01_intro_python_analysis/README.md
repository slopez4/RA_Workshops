# Workshop 1 — Intro to Simple Analysis Scripts in Python

**Session:** 09/28 · **Length:** 30–40 min · **No installation needed**
**📊 Slides / reference guide:** [open the slides](https://slopez4.github.io/RA_Workshops/01_intro_python_analysis/slides.html) — keep it open while you work (press `R` to switch between slide view and a scrollable reference page).

In this workshop you'll write a short Python analysis of a (fake) reward experiment:
bring a data file in, check whether you can trust it, clean it, and ask whether
reward changed how people performed — and whether that changed over the session.

No coding experience is needed. The goal is to learn a few coding basics **and**
the habit of thinking carefully about data before trusting any average.

---

## Start here (2 minutes)

1. Sign in to a Google account in your browser (any Gmail works).
2. Click this button to open the workshop notebook:

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/01_intro_python_analysis/notebooks/workshop_student.ipynb)

3. If Colab shows *"Warning: This notebook was not authored by Google"*, click **Run anyway**.
4. Click **File → Save a copy in Drive**. Work in *your copy* so your changes are saved.
5. Click the first grey code cell and press **Shift + Enter**. If you see output, you're ready.

> **No Google account?** Use this backup (no login, but takes 1–2 min to start):
> [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/slopez4/RA_Workshops/main?labpath=01_intro_python_analysis%2Fnotebooks%2Fworkshop_student.ipynb)
> Binder does **not** save your work — download the notebook before closing the tab.

---

## What's in this folder

| File | What it is | Who it's for |
|---|---|---|
| [`notebooks/workshop_student.ipynb`](notebooks/workshop_student.ipynb) | The notebook we work through together, with blanks (`___`) to fill in | RAs |
| [`notebooks/workshop_solutions.ipynb`](notebooks/workshop_solutions.ipynb) | Same notebook, blanks filled in | Checking your work afterward |
| [`analysis.py`](analysis.py) | The whole analysis as one clean script — what "real" analysis code looks like | Everyone, after the workshop |
| [`data/reward_task_mock.csv`](data/reward_task_mock.csv) | The fake dataset (20 participants × 80 trials) | — |
| [`data/make_mock_data.py`](data/make_mock_data.py) | How the fake data was generated | Instructors |
| [`slides.html`](https://slopez4.github.io/RA_Workshops/01_intro_python_analysis/slides.html) | Slides for class, and a scrollable reference page (cheat sheet, common errors) | Everyone |
| [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md) | The session plan: goals, timing, and agenda | Everyone |
| [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) | How to run the session, answers to every prompt, common errors | Instructors |

[![Open solutions in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/01_intro_python_analysis/notebooks/workshop_solutions.ipynb) ← solutions

---

## The mock experiment

Participants did a quick two-choice task in 4 blocks of 20 trials. In **reward**
blocks they earned points for fast, correct answers; in **no-reward** blocks they
didn't. Block order was counterbalanced. After each block they rated their
motivation from 1 to 7.

| column | meaning |
|---|---|
| `participant_id` | who (P01–P20) |
| `order` | `reward_first` or `no_reward_first` |
| `block` | 1–4 |
| `trial` | 1–20 within each block |
| `condition` | `reward` or `no_reward` |
| `rt_ms` | reaction time in ms (empty = no response) |
| `correct` | 1 = correct, 0 = wrong or missed |
| `motivation_rating` | 1–7, asked once per block (repeated on every row of that block) |

The data are **simulated** — not from a real study — and contain a few problems
on purpose. Finding them is part of the workshop.

---

## What you'll be able to do afterward

- Read a Python script and explain what each part does
- Use variables, lists, `for` loops, and `if` statements
- Load a CSV file and check its shape, columns, and missing values
- Spot suspicious data (impossible reaction times, a participant who was guessing)
- Filter rows, group data, and compute per-participant averages
- Make a plot that shows individual participants, not just the group mean

## Keep practicing

- Re-open your saved copy in Google Drive any time.
- Try the ⭐ stretch exercise at the end of the notebook.
- Read [`analysis.py`](analysis.py) top to bottom — you should recognise every line.
- Free follow-ups: [Python for Everybody](https://www.py4e.com/) (chapters 1–5),
  [pandas "10 minutes to pandas"](https://pandas.pydata.org/docs/user_guide/10min.html).
