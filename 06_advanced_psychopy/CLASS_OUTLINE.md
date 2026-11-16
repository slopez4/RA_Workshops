# Class Outline · Workshop 6: Experiments That Don't Lose Data

## Session overview

| | |
|---|---|
| **Topic** | Advanced experiment scripting in Python/PsychoPy: building and storing a trial matrix, frame-accurate timing, and data-loss prevention (ESC, crashes, resume, overwrite, counterbalancing), plus annotation |
| **Audience** | RAs who did Workshop 2 (PsychoPy basics). Workshop 5 helps: its negative RTs are fixed here |
| **Format** | Walk-through of `grouping_task.py` against two lab scripts (MATLAB attentional blink, PsychoPy RDT), then hands-on "break it and recover" |
| **Length** | ~75 min, or two sittings (Parts 1–2, then Parts 3–4 + hands-on) |
| **Setup** | PsychoPy 2026.1 on the lab computers; repo ZIP downloaded |
| **Materials** | [Slides](https://slopez4.github.io/RA_Workshops/06_advanced_psychopy/slides.html) · [`grouping_task.py`](grouping_task.py) · [`trial_matrix.py`](trial_matrix.py) · [`test_trial_matrix.py`](test_trial_matrix.py) · [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) |

## Learning goals

By the end, RAs will be able to:

1. **Build** a full-factorial trial table with named columns, shuffle it under a constraint, and make it reproducible with a saved seed.
2. **Explain** why the whole session's plan is written to `_trials.csv` before trial 1, and how a resume uses it.
3. **Test** design code without PsychoPy, and say what a test of the displays catches that the data never would.
4. **Time** stimuli in frames from a measured refresh rate, take onsets from flips, and time RTs from the flip that shows the display.
5. **Diagnose** the key-buffer bug (negative RTs) and fix it with `clearEvents` + `callOnFlip`.
6. **Make** every way out of an experiment (ESC, crash, end) save first and record its status, through one exit path.
7. **Resume**, overwrite (archive) and counterbalance the way STUDY_CONVENTIONS.md describes, and read the resulting files.
8. **Annotate** a script so someone else can check it: header, units, why-comments, named workarounds.

## Agenda

| Time | Slides | Part | Hands-on |
|---|---|---|---|
| 0:00–0:05 | 1–5 | Setup; the task; three jobs of an experiment script | Run as 999 through practice + 1 block; open the 3 files |
| 0:05–0:25 | 6–11 | **1. Trial matrix**: factorial table, names vs numbers, constrained shuffle + seed, plan saved first, debug mode, tests | `python trial_matrix.py`; `python test_trial_matrix.py` |
| 0:25–0:45 | 12–16 | **2. Timing**: frames, create once, the negative-RT bug, the response loop, when to touch the disk | Find `clearEvents` and `callOnFlip` in the script |
| 0:45–1:05 | 17–22 | **3. Never lose data**: ESC, one exit path, resume, overwrite, counterbalancing, what's on disk when | — |
| 1:05–1:10 | 23 | **4. Annotate** | Read the header; find one comment that explains *why* |
| 1:10–1:25 | 24–25 | **Break it on purpose** + checklist | Exercises 1–3 for everyone; 4–5 for fast groups |

Slides 26–28 are reference (cheat sheet, common problems, close the loop).

## Splitting into two sittings

- **Sitting 1** (35 min): slides 1–16. Homework: run `test_trial_matrix.py`, read `trial_matrix.py`.
- **Sitting 2** (40 min): recap slide 9 (the plan) and 14 (the bug), then 17–25.

## Where to cut if time runs short

- Slide 7 (names vs numbers): one sentence.
- Slide 13 (create once): one sentence; both lab scripts already do it.
- Hands-on: do exercise 2 (crash + resume) live on the projector instead of in pairs.
- **Don't cut** slides 9 (plan first), 14 (the negative-RT bug), 18 (one exit path) or 19 (resume).

## After the session

- Exercises 4–5 of the hands-on slide as homework.
- Run a debug session and analyse its `_behav.csv` with the Workshop 5 habits.
