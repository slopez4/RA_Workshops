# Workshop 6: Experiments That Don't Lose Data

**Length:** ~75 min (or two sittings: Parts 1–2, then Parts 3–4) · **PsychoPy is already installed on the lab computers**

**📊 Slides / reference guide:** [open the slides](https://slopez4.github.io/RA_Workshops/06_advanced_psychopy/slides.html). Press `R` for the scrollable reference view (cheat sheet, common problems).

The advanced follow-up to [Workshop 2](../02_psychopy_experiment/). We take a small
version of the lab's grouping task (the Repetition Discrimination Task you analysed in
[Workshop 5](../05_analysis_scripts_ggp/)) and look at what makes an experiment script
trustworthy:

1. **The trial matrix**: turning a design into a table, shuffling with constraints and a
   seed, and saving the whole session's plan *before* the first trial.
2. **Timing and efficiency**: counting in frames, creating stimuli once, timing RTs from
   the flip, and the key-buffer bug behind Workshop 5's negative reaction times.
3. **Never losing data**: ESC and crashes that save first, resuming with the same trials,
   overwriting that archives instead of deleting, and counterbalancing from a sheet.
4. **Annotation**: headers, units, and comments that explain why.

We compare three scripts along the way: a lab MATLAB/Psychtoolbox experiment (attentional
blink), the lab's PsychoPy RDT, and `grouping_task.py`. The rules come from the lab's
[`STUDY_CONVENTIONS.md`](STUDY_CONVENTIONS.md) (sections 1, 2, 4, 5, 9, 14 and 18).

---

## Get the files and test

1. On [the repo page](https://github.com/slopez4/RA_Workshops), **Code → Download ZIP**, unzip.
2. PsychoPy → **View → Coder** → open `06_advanced_psychopy/grouping_task.py` → **Run**.
3. Enter Participant ID **`999`** (debug mode: small window, short blocks).

If a window appears, the practice runs, and `data/debug/999_trials.csv` appears, you're ready.

No PsychoPy? The design code runs with plain Python and pandas:

```bash
python test_trial_matrix.py
```

## What's in this folder

| File | What it is |
|---|---|
| [`grouping_task.py`](grouping_task.py) | The experiment (PsychoPy). Resume / overwrite / crash report, ESC and crash saving, frame timing, a simulated participant (`--auto`) |
| [`trial_matrix.py`](trial_matrix.py) | Builds the session's trial table and each display's layout. No PsychoPy, so it can be tested anywhere |
| [`test_trial_matrix.py`](test_trial_matrix.py) | Checks the design: counts, balance, run limits, seeds, and that every display shows what its label says |
| [`counterbalancing.py`](counterbalancing.py) | Reads and updates the counterbalancing sheet (from the lab's study template; only the header changed) |
| [`crash_report.py`](crash_report.py) | Excludes a participant with a reason and reopens their condition (from the study template; only the header changed) |
| [`STUDY_CONVENTIONS.md`](STUDY_CONVENTIONS.md) | The lab's conventions this workshop follows |
| [`slides.html`](https://slopez4.github.io/RA_Workshops/06_advanced_psychopy/slides.html) | Slides + reference page |
| [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md) | Goals, timing, agenda |
| [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) | How to run it, answers, troubleshooting |

## Running it

| Command | What happens |
|---|---|
| Run in Coder, ID `999` | Debug: practice + 2 blocks of 14 trials, windowed, files in `data/debug/` |
| Run in Coder, ID `101`+ | Real: practice + 2 blocks of 56 trials, fullscreen, condition from the sheet |
| `python grouping_task.py --auto` | Simulated participant as 999: no dialogs, answers by itself |
| `python grouping_task.py --auto --crash-at 20` | Same, but "crashes" on trial 20 |
| `python grouping_task.py --auto --resume` | Resumes the last 999 session |
| `python counterbalancing.py --new A B --n 40` | Makes the counterbalancing sheet (needed before the first real ID) |
| `python counterbalancing.py --status` | Counts per condition |
| `python crash_report.py` | Exclude a participant and reopen their slot |

Run the `--auto` commands from a terminal that uses PsychoPy's Python (on the lab
computers: `"C:\Program Files\PsychoPy\python.exe" grouping_task.py --auto`).

### Files written per participant

| File | When | What |
|---|---|---|
| `<id>_trials.csv` | before trial 1 | the plan: every trial of every block, with its correct key |
| `<id>_info.csv` | at start, every break, and on exit | one row per run: status, blocks done, condition, keys, seed, refresh rate, dropped frames, crash comments |
| `<id>_behav.csv` | every break, and on exit | every trial: response, correct, RT (s, from the display's flip), onset, timeout, `Valid` |

`data/`, `counterbalancing.csv` and `counterbalancing_backups/` are git-ignored.

## What you'll be able to do afterward

- Turn a design into a full-factorial trial table, shuffle it under constraints, and make it reproducible with a seed
- Explain why the whole plan is saved before the first trial, and use it to resume a crashed session
- Write design code that can be tested without PsychoPy
- Time stimuli in frames, time RTs from the flip, and explain (and fix) a key-buffer bug
- Make ESC and crashes save before quitting, through one exit path
- Overwrite without deleting; assign conditions from a counterbalancing sheet
- Write a script header and comments that someone else can check

## Keep practicing

The "Break it on purpose" slide: press ESC mid-block, simulate a crash and resume,
overwrite, add a cue to the design, and review the lab scripts for another way to lose
data. Then load your debug `_behav.csv` with the Workshop 5 habits.
