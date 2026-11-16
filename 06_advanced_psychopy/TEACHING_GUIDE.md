# Teaching Guide · Workshop 6: Experiments That Don't Lose Data

For whoever runs the session: prep, what to emphasize on each slide, answers to the
prompts and exercises, and troubleshooting.

---

## 1. Before the session

### A week before
- [ ] Push the folder to GitHub (RAs download the ZIP).
- [ ] On **one lab computer**, run a full debug session (ID `999`) by hand, including one
      ESC, and check the three files open. Then run
      `"C:\Program Files\PsychoPy\python.exe" grouping_task.py --auto --crash-at 20`
      followed by `--auto --resume` from a terminal.
- [ ] **The PsychoPy dialogs have not been clicked through yet.** The scripted
      (`--auto`) path, the counterbalancing sheet and the crash report's terminal version
      were tested on PsychoPy 2026.1.3 (see "What was tested" below). The start dialog,
      the existing-participant dialog (Resume / Overwrite / Crash report / Cancel), the
      overwrite confirmation and the crash report's dialog version have not. Click through
      each once before class.
- [ ] Decide whether to show the MATLAB script on screen. The slides quote short excerpts;
      the full file stays in the lab's Box folder.

### 10 minutes before
- [ ] Delete `data/` from your demo copy so the first run is fresh.
- [ ] If you'll demo a real ID: `python counterbalancing.py --new A B --n 10`.
- [ ] Slides in one window, PsychoPy Coder with `grouping_task.py` in another.

---

## 2. How to teach it

**Compare, don't scold.** The lab scripts worked: they collected real data. The point is
what happens *on the bad day*, and every problem we show actually happened or easily
could. Frame it as "here's what this script would do if…".

**Keep pointing at the files.** After each Part, open `data/debug/` and show what's there.
The abstract rules ("save at breaks") become concrete when they see `Status = aborted`.

**The two moments to slow down:** slide 14 (the negative-RT bug ties Workshop 5 to this
one) and slide 19 (resume: the `Valid = False` rows).

---

## 3. Answers

### Slide 3 · Why save the full plan before trial 1?
If the session crashes, you can replay exactly the trials not yet run, in the same order,
and you can check afterwards that the experiment showed what it planned (compare
`_trials.csv` with `_behav.csv`).

### Slide 6 · `Tmat(:,4)==2`
Column 4 is the lag, coded 1–3 by `fullfact`. The comment above
`Tmat(Tmat(:,4)==2, 4) = 7` says it turns "lags 2 and 3 into 3 and 7", but the code turns
level 2 into 7 and leaves 3 alone. And it doesn't matter: a few lines later the whole
column is overwritten (first ninth = 7, the rest = 3). So the line is dead code with a
comment that doesn't match it. Nobody can tell that from `Tmat(:,4)==2`;
`row["WBN"] == "WITHIN"` explains itself.

### Slide 10 · Why not a separate test version?
You'd be testing a different program. Debug mode runs the same code with fewer trials.

### Slide 11 · Swapped WITHIN/BETWEEN
The data would just show negative effects, which could be published as a surprising
finding. Only a check on the displays catches it. (The test does: swapping the line in
`layout()` makes the last check fail. This was verified.)

### Slide 12 · `off_time = 0.033; % 50 ms`
Value 33 ms, comment 50 ms. One of them is wrong, and the comment is the one people read.

### Slide 14 · Negative RTs
In `RDT02_Lab.py`, `event.waitKeys(keyList=['space'])` removes only space presses from
the key buffer, and `event.clearEvents()` only runs at the end of each trial. An `n`/`m`
pressed on the "press space" screen (block start, or the halfway break) stays in the
buffer. The next trial's `event.getKeys(..., timeStamped=trial_clock)` returns it with a
time before the clock was created: a negative RT. Workshop 5 found two (−0.94 s and
−1.15 s), both on the first trial after a "press space" screen, both scored wrong.
Also: the RDT clock starts before the first flip, so every RT there includes the wait for
that flip (up to one frame, ~17 ms at 60 Hz).

### Slide 21 · Pilot key mapping
`"A12".isdigit()` is `False`, so `sub_number = 0`, which is even: every A-numbered pilot
got square = `n`, circle = `m`. No counterbalancing at all for those sessions, and nothing
in the data file records the mapping.

### Slide 24 · Hands-on
1. **ESC**: `Status = aborted`, `Session_End` filled, `Last_Block_Completed` = the last
   finished block. `_behav.csv` has every trial up to the ESC (they're saved on the way
   out even though the block didn't finish).
2. **Crash + resume**: run 1 `crashed`, `Last_Block_Completed = 0`. Run 2 starts at block
   1. The 12 block-1 rows from run 1 are `Valid = False`; block 1 is re-run from its first
   trial with the same trials in the same order. Valid trials: 7 + 14 + 14 = 35, each
   `Trial_ID` once.
3. **Overwrite**: the old files are in `data/debug/overwritten/999_<timestamp>/`.
4. **Add EC**: the first failing check is "56 conditions", because the test encodes the
   design (it's now 72). Update it and the display check fails: `layout()` has no EC
   branch, so EC displays look like NEUTRAL (no grouping), and the test's `groups()` has no
   EC rule (it returns `None`, so the check crashes). The fix needs both: draw EC (bars
   joining pairs: add bar stimuli in `setup_screen`, positions in `layout()`), and teach
   the test how to read EC groups. Good discussion: the test refused a cue that didn't
   actually group anything.
5. **More ways to lose data** (any of these):
   - AB: saves `.mat` files in whatever folder MATLAB is in (no path), so a session can
     land in the wrong folder or overwrite another participant's file of the same name
     without asking.
   - AB: `clear all` at the top, so a restart wipes anything in memory.
   - AB: the subject number from the dialog isn't checked; a typo silently picks another
     row of the counterbalancing CSV (or crashes on an empty `rowIndex`).
   - RDT: the overwrite check only covers the exact file name; ID `012` vs `12` makes two
     files for one person.
   - RDT: `debug = True` is the default in CONFIG.
   - RDT: no record of the key mapping, the refresh rate or the PsychoPy version.

---

## 4. What was tested (and what wasn't)

Tested on 2026-11-15, Windows, PsychoPy 2026.1.3 standalone:
- `test_trial_matrix.py`: all 14 checks pass; swapping WITHIN/BETWEEN in `layout()` makes
  the display check fail.
- `grouping_task.py --auto --crash-at 20` then `--auto --resume`: crash saved with
  `Status = crashed`; resume started at block 1; 12 rows `Valid = False`; 35 valid rows with
  unique `Trial_ID`; refresh measured at 60 Hz; 0 dropped frames.
- `new_session()` with the sheet: 101 → A, 102 → B, 101 again → A (same slot), pilot 50 →
  no slot; `crash_report.run("102", use_console=True)` excluded 102 and the reopened B slot
  went to 103; 102 can no longer be assigned.

Not tested: every PsychoPy dialog (see the checklist above), real keypresses and ESC
(the simulated participant doesn't press keys), fullscreen mode, other monitors.

---

## 5. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: psychopy` | You ran it with another Python. Use Coder, or PsychoPy's `python.exe`. |
| `ModuleNotFoundError: trial_matrix` | The script was moved without its folder. Keep the files together. |
| `SheetError: No counterbalancing sheet` with a real ID | `python counterbalancing.py --new A B --n 40` |
| Window opens and closes at once | Read the terminal: an error after the window opened is saved as `crashed` and then printed. |
| `Refresh_Hz` is 60 but the monitor is 144 Hz | Measurement failed and the fallback was used (a warning is printed). Close other programs, one screen only. |
| The next launch hangs | Leftover PsychoPy process after a crash: close it in Task Manager. |
