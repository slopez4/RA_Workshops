# Study Design Conventions

How I set up experiment repositories. This project (Dispupil) is the worked example, but everything here is meant to carry over to the next study unchanged. If a new study breaks one of these rules, say so in its README and say why.

---

## 1. Folder structure

```
<Study>/
├── README.md               what the study is, how to run it
├── STUDY_CONVENTIONS.md    this file
├── IRB/                    protocol, consent forms, approvals (git-ignored: kept private)
├── experiment_files/       what the testing machine runs: the experiment and its sheet
├── scripts/                everything after collection: export, analysis, figures
├── calibration/            display measurements (colorimeter readings), never participant data
├── rawdata/                exactly what the experiment wrote. Never edited by hand.
│   ├── debug/              debug runs (git-ignored, never analysed)
│   └── overwritten/        archived files from overwritten participants
├── prettydata/             derived/processed data. Safe to delete and regenerate.
└── figtree/                figures. Regenerated from prettydata, never hand-edited.
```

- **Data flows one way:** `rawdata → prettydata → figtree`. A script may read from a folder to its left and write to the right, never the other direction.
- **`experiment_files/` is separate from `scripts/`.** It holds everything the testing machine needs to run a session and nothing else: the experiment script, the modules it imports (`display_config.py`), the hardware test scripts, the counterbalancing sheet and the crash report (section 18). `scripts/` holds what runs afterwards (export, analysis, figures) and never needs the hardware.
- Each data folder has its own `README.md` listing every file that lands there and which script writes it.
- Scripts resolve paths from their own location (`os.path.abspath(__file__)`), never from the working directory, so output always lands in the right folder no matter where the script is launched from.
- Test output (debug runs, synthetic demo data) goes in its own subfolder (`debug/`, `demo/`). It never sits next to real participants, and it's git-ignored.

## 2. File naming

Every participant file is `<subid>_<kind>.<ext>`: one prefix, one kind, no dates or condition names in the file name. Anything else about the session goes *inside* `_info.csv`.

By the end of a session, each participant has **four files**:

| File | Role |
|---|---|
| `<subid>_trials.csv` | The plan: the full trial sequence, generated and saved before the first trial is shown. |
| `<subid>_behav.csv` | What happened: every trial from the plan plus responses, RTs and onset timestamps. |
| `<subid>_pupil.hdf5` | Physiology: the continuous eye-tracker record, with a marker at every trial onset. |
| `<subid>_info.csv` | Who and when: demographics, timestamps, condition order, setup, crash notes. One row per run. |

Plus `<subid>_calibration.json` whenever an eye tracker is used.

- Derived files keep the same prefix and describe what they are (`<subid>_pupil_samples.csv`, `<subid>_pupil_sync.csv`).
- Group-level derived files have no prefix (`pupil_trial_metrics.csv`).

### Participant IDs

The number in a participant ID says what kind of data it is.

| ID | Reserved for | Rule |
|---|---|---|
| `1` to `100` | Piloting | Not part of the final sample. |
| `101` and up (except `999`) | Real participants | Counterbalanced through the sheet (section 18). |
| `999` | Debugging | Always excluded from analysis. |

- Pilot and debug IDs never take a counterbalancing slot.
- Analysis scripts drop `999` by ID, so a debug file can never reach a result even if it ends up in the wrong folder.

## 3. Column conventions

- Column names use `Capitalized_Snake_Case` (`Block_Num`, `Trial_ID`, `Onset_Time`).
- Blocks and trials are numbered **from 1**. Practice is **block 0**.
- `Trial_ID` is unique across the whole session. `Block_Num` + `Trial_Num` is unique among valid rows.
- Boolean flags start with `Is_` (`Is_Special`, `Is_Probe`, `Is_Catch`).
- Times are in seconds on the experiment clock (`Onset_Time`, `RT`), unless the name says otherwise (`Time_ms`).
- Every row repeats `Participant` and `Run`, so files can be concatenated across participants without losing anything.

## 4. Escapesafes

The rule: **no crash, keypress or experimenter mistake should ever lose data or force a participant to redo work.**

1. **Pre-generate the trial sequence.** All trials for the session are randomized up front and written to `_trials.csv` before the first trial is shown. If the session crashes, the same trials can be replayed.
2. **Save at every break, never mid-trial.**
   - `_behav.csv` and `_info.csv` are rewritten, and the eye-tracker file is flushed, on the between-block break screen.
   - Disk I/O never happens while a stimulus is on screen, so it can't disturb timing.
3. **ESC saves before quitting.**
   - ESC is a global key that writes everything collected so far and marks the run `aborted` in `_info.csv`.
   - It then stops the tracker and closes the window.
   - It never just quits.
4. **Write `_info.csv` at the start.** Even a session that dies in the first minute leaves a record of who, when, and which condition order.
5. **Track progress.** `_info.csv` records `Last_Block_Completed` after every block, so after a crash you know exactly where the session stopped.
6. **Resume an incomplete session.**
   - Starting the script with an existing participant ID offers *Resume incomplete experiment*.
   - Enter the last completed block (pre-filled from `_info.csv`) and any **Crash comments**.
   - The session continues at the next block with the same trials, and the eye tracker is recalibrated.
7. **Keep everything, flag what's superseded.**
   - Rows from a partly-finished block that gets re-run stay in `_behav.csv`, marked `Valid = False`.
   - Each run is its own row in `_info.csv` and its own session in the `.hdf5`.
   - Analyses use `Valid == True`.
8. **Overwriting takes two steps and is reversible.**
   - *Overwrite participant* asks for a second confirmation.
   - It then **moves** the old files to `rawdata/overwritten/<subid>_<timestamp>/`. Nothing is ever deleted.
9. **Demographics and counterbalancing are fixed at run 1.** A resume reads them from the original `_info.csv`, so they can't drift between runs.

## 5. Timing and synchronization

- Every stimulus onset is the value returned by `win.flip()`, logged as `Onset_Time`.
- The **same timestamp** is sent to the eye-tracker file as a marker (`TRIAL_START_RUN_<r>_ID_<id>_BLOCK_<b>_TRIAL_<t>`). The experiment and the tracker share one clock, so behavior and physiology map one-to-one by `Run` + `Trial_ID`.
- RTs are measured from `Onset_Time`, not from a timer started after the flip.
- The export script produces a **sync check** (`_pupil_sync.csv`) comparing every behavioral onset with its marker. Run it after every pilot session.
- Response windows are fixed durations. Self-paced screens (ratings, instructions) are logged with their own onset.

## 6. Eye tracking

- Calibrate at the start of every run, including resumed ones. Calibrating in the manufacturer's software (e.g., Tobii Pro Eye Tracker Manager) is fine, but the script must then **verify** it:
  - It reads the calibration stored on the tracker and fingerprints it.
  - It refuses (or warns about) a calibration already used for an earlier participant or run.
- Follow every calibration with a short **validation**: gaze accuracy in degrees and the share of valid samples, shown to the experimenter, who continues or recalibrates.
- Save the calibration itself (the tracker's calibration data, so it can be inspected or re-applied), the validation and the full tracker configuration to `<subid>_calibration.json`, with a summary in `_info.csv`.
- **Record continuously** from calibration to the end of the run, practice included; markers tag what each stretch is.
  - Don't pause and resume the stream. In testing, the Tobii stopped sending samples after a pause/resume, and also on its own during long idle screens.
- **Check the stream at every break.** Confirm samples are still arriving, restart recording if not, and alert the experimenter if that fails. Log every check in `_info.csv`.
- If the tracker is requested but doesn't connect, stop and ask. Never continue silently without physiological data.
- Resumed runs are appended to the existing `.hdf5` as a new session, never written over it.
- After a crash, make sure PsychoPy has fully closed before restarting. A leftover ioHub process can make the next launch hang.

## 7. Participant info

Collected in the start dialog and saved to `_info.csv`:

- **Participant:** ID, Age, Sex, Gender (free text, self-described).
- **Session:** start and end timestamps, status, run number, start block, last block completed, crash comments.
- **Design:** the counterbalancing factor and the full block order, both as one string (`Block_Order`) and one column per block (`Block_1`…`Block_N`).
- **Setup:**
  - screen width (cm) and resolution (px), plus viewing distance (cm)
  - pixels per degree, stimulus parameters, software version
  - debug and eye-tracker flags

## 8. Stimulus geometry

- Specify visual stimuli in **degrees of visual angle** (spatial frequency in cycles/deg).
- Compute degrees from the **measured** screen width and the viewing distance, never from a hard-coded monitor profile:
  - The dialog pre-fills the width from the monitor's own report; confirm it with a ruler.
  - Resolution is read from the actual fullscreen window.
- Print the resulting pixels/degree and pixels/cycle at startup, and warn if a stimulus is too fine for the display to draw properly.
- Size instruction text relative to the screen, not in degrees, so it always fits.

## 8b. Colors and luminance

- All stimulus colors live in one shared module (`experiment_files/display_config.py`). The experiment and the luminance-check script both import it, so what you measure is exactly what participants see.
- Colors are written in PsychoPy's `rgb1` space (0–1). Never mix them with the default `rgb` space (−1 to 1): that silently washes colors out.
- A "luminance-calibrated" monitor usually means calibrated to a standard gamma (~2.2), **not** linear. A gray control only matches a grating's mean luminance on a linear display. Measure black, gray and white with a colorimeter (`experiment_files/luminance_check.py`), and set the gamma correction from the result.
- Re-measure before the first participant, after any monitor change, and periodically during collection. Keep every measurement file in `calibration/`.

## 9. Debug mode

- A **Debug** checkbox in the start dialog runs the *same code path* with minimal trial counts. It keeps every block type, practice, and special trial type, so a full run-through takes a few minutes.
- Debug runs use participant ID `999` (section 2).
- Debug output goes to `rawdata/debug/`. The analysis never reads it, and the overwrite check can't be confused by it.
- Before any real participant, a debug run on the testing machine should finish cleanly, and its pupil export should pass the sync check.

## 10. Analysis hygiene

- Raw data is read-only **once real data collection begins**. Before that, pilot and test files may be renamed, cleaned or deleted. Cleaning, epoching and exclusions all happen in scripts that write to `prettydata/`.
- Figures are regenerated from `prettydata/` by script. No hand-edited figures.
- Synthetic demo data (`--demo`) validates the pipeline before real data exists, and lives in `demo/` subfolders.

## 11. Python & VS Code environment setup

One-time per machine, not per study:

- **Install Anaconda**, not the bare python.org installer and not the
  Microsoft Store stub (that one just opens the Store without installing
  anything runnable). Anaconda bundles pandas/numpy/matplotlib/scipy/
  statsmodels, which analysis scripts assume are already available.
- **Select the interpreter in VS Code**: `Ctrl+Shift+P` -> "Python: Select
  Interpreter" -> the one showing `anaconda3`. Until this is done, VS Code
  doesn't know which Python to run anything with, and a script that works
  from a terminal can still show unresolved-import errors in the editor.
- **Open a *new* integrated terminal after selecting the interpreter** -- a
  terminal already open when you switch interpreters keeps using the old
  one.
- **Secrets (API tokens) go through `setx`, not `$env:VAR = "..."`.**
  `$env:VAR = "..."` only lasts for that one PowerShell session and is gone
  the moment it closes -- easy to think a token is set because it worked
  once, then have it silently vanish later. `setx VAR "value"` persists it,
  but **only new processes see it** -- the window it was set from (and
  anything already running, including a long-lived tool session or an
  already-open terminal) needs to be closed and reopened before it can read
  the value, same for a scheduled task picking it up for the first time.
  When verifying a token is actually set, check from a freshly-opened
  terminal, not the one `setx` was run in.
- **Never type a real secret into a script file or commit one.** Scripts
  read tokens from environment variables with a placeholder default (e.g.
  `"${VAR:-PASTE_X_HERE}"` in bash) so the script is safe to commit as-is.
- **Each study gets its own conda environment**, defined in an
  `environment.yml` at the repo's top folder (`conda env create -f
  environment.yml`, then select it as the VS Code interpreter), so one
  study's package updates can't break another's analysis.
- **Each study has one entry-point script, `scripts/run_analysis.py`**, that
  runs the standard full analysis in order (analysis -> power -> figures);
  the other scripts are its steps. Open it and click Run. It puts the
  env's `Library\bin` on PATH itself, so it also works from a terminal
  where `conda activate` isn't available.
- `scripts/requirements.txt` lists anything a study's own scripts need
  beyond the Anaconda base (rare) -- `pip install -r
  scripts/requirements.txt` if VS Code flags an import as unresolved.

## 12. Participant data and de-identification

**The rule:** raw data goes into the repo, so it is versioned and backed up. It must be **de-identified at the source**: the experiment never records anything that identifies a person.
- The repo stays **private** during data collection.
- A public version is released only after a de-identification check (below).
- `rawdata/` is untouched once real data collection begins. Tag that commit (e.g. `git tag data-collection-start`), so the history shows nothing was edited after it.

### What counts as identifiable

Confirm the final rules with your IRB; these are the usual reference points:
- **The Common Rule** (45 CFR 46.102(e)(5)): information is identifiable if the participant's identity "is or may readily be ascertained by the investigator or associated with the information."
- **HIPAA's Safe Harbor list** (45 CFR 164.514(b)(2)) is the benchmark IRBs commonly use for "de-identified", even outside medical research. Its 18 identifiers that are relevant here:
  - names (most IRBs treat initials as identifying too)
  - geographic units smaller than a state
  - **all elements of dates (except the year) directly related to a person**, such as session dates
  - phone numbers, email addresses and other contact information
  - account or ID numbers (e.g. SONA ID, student ID, any "unique identifying number or code" that isn't the study's own random code)
  - IP addresses and URLs
  - biometric identifiers (e.g. voice or fingerprints) and full-face photos
- **Indirect identifiers:** a combination of harmless-looking fields can single someone out in a small sample, e.g. age + gender + exact session date + a rare category.
- **The final word is the approved IRB protocol** (in this study: "recorded under a code number with no link to names"). Whatever the protocol says is collected and shared is the limit.

### Applied to the files this kind of study writes

| Field | Status | Rule |
|---|---|---|
| Participant ID | identifier if it's initials, a name, or a SONA/student ID | Use study codes (`101`, `102`, ...; section 2 lists the reserved ranges). Rename pilot files that used initials before any release. |
| Code ↔ person link (e.g. SONA ID ↔ code) | identifying | Never in the repo. Keep it only if the protocol allows, in approved secure storage. |
| `Session_Start`/`Session_End`, `Checked_At`, `First_Seen` | dates tied to a person | Fine in the private repo. For public release, reduce to the year, or convert to relative times. |
| `Age` | quasi-identifier | Keep. Top-code at 90+ if it ever applies. |
| `Sex`, `Gender` (free text) | quasi-identifier | Keep. For public release, recode rare free-text answers into broader categories. |
| `Crash_Comments` | free text | Never write names or identifying details, only what happened. |
| Behavioral, pupil and gaze data | not identifying on their own | Keep. |
| Equipment serial numbers (e.g. the eye tracker's) | lab equipment, not the participant | Keep. |

Commit messages, file names and folder names follow the same rules: no participant names, ever.

### Public release
- Run a de-identification pass (ideally a script) that produces the public copy.
- Check that copy against the table above, and confirm the consent form / information sheet allows sharing de-identified data.
- Strip anything else that shouldn't be public: tokens and API keys, IRB documents (already git-ignored), and local paths.

## 13. AI disclosure

Any AI-assisted work on a study is disclosed and traceable.

- **`AI_Disclosure.md`** at the repo root is a running log with one entry per working session:
  - the date and the AI tool/model
  - a summary of the prompts (what was asked)
  - a summary of the outputs (what changed, which files, which commits)
  - how the work was verified
  - flags for anything that still needs verification
- **Commits** with AI-written changes end with a `Co-Authored-By:` trailer naming the model. `git log` then lists every AI-assisted change, and each commit's diff shows exactly what changed.
- **How the AI's work is verified:**
  - The researcher reviews the diffs and makes or approves every commit.
  - The scripts are run on the actual testing hardware (debug mode first), and their output files and rendered screens are checked.
  - Hardware is checked with the test scripts (eye tracker, response pad, colorimeter), since the AI can't test real devices.
  - Design decisions are reviewed with the PIs.
- **Flag anything prone to hallucination** in `AI_Disclosure.md`, with a status (*open* until someone verifies it, then *verified: who/how/date*):
  - citations, references, DOIs and quotes
  - regulatory, IRB or legal statements
  - hardware protocols, device specs, button numbering and driver behavior written without the device present
  - numbers presented as facts (thresholds, norms, specs) rather than computed from the study's own data
  - explanations for a failure whose cause wasn't confirmed
- **Code is the least risky**, because it is run and tested. Code paths that couldn't be run (e.g. drivers for hardware the AI couldn't access) stay flagged until they've been run for real.

## 14. Code comments and script headers

The rule: **someone who didn't write the code (a PI, a new lab member, me in a year) can follow it without running it.**

### Script header

Every script starts with a header block, with these fields in this order:

```python
"""
Project:       Dispupil
Script:        scripts/export_pupil.py
Creator:       <name>
Purpose:       One or two sentences: what the script does and where it sits
               in the pipeline (rawdata -> prettydata -> figtree).
Last updated:  YYYY-MM-DD

Usage (example):
    python scripts/export_pupil.py              export every participant
    python scripts/export_pupil.py --sub 101    export one participant
    python scripts/export_pupil.py --demo       run on synthetic demo data

Dependencies:  pandas, numpy, h5py (all in environment.yml)
Reads:         rawdata/<subid>_pupil.hdf5, rawdata/<subid>_behav.csv
Writes:        prettydata/<subid>_pupil_samples.csv
               prettydata/<subid>_pupil_sync.csv
"""
```

- **Usage** lists every command-line flag and dialog option the script supports. A script with none says so (`Usage: open and click Run`).
- **Dependencies** names every package beyond the standard library, any other study module the script imports, and any hardware it needs (eye tracker, response pad, colorimeter).
- **Reads / Writes** must match the README in each data folder (section 1). If the two disagree, one of them is wrong.
- **Last updated** changes whenever the script's behavior changes, not for typo fixes. `git log` is the full history; the header is for anyone reading a copy outside git (Box, Drive, email).
- Other languages use the same fields in their own comment style (`%` in MATLAB, `#` in bash and R).

### Comments

- **Comment the why, not the what.** `# flush here so disk I/O never overlaps a stimulus` is useful; `# flush the file` is not.
- Each logical section of a script starts with a short comment saying what that section does, so the script can be skimmed by its comments alone.
- Every function has a docstring: what it does, its inputs, its outputs, and the **units** of anything numeric (seconds, degrees, pixels, cd/m²).
- Every constant says its unit and where the value came from (measured, from the protocol, from a paper, chosen by hand).
- A workaround names the problem it works around (e.g. the Tobii stream stopping after pause/resume), so nobody "cleans it up" later.
- No commented-out code. Git keeps the old version.
- When code changes, its comments and the header change in the same commit.
- **Comments are claims.** A comment written by an AI is checked like the code it describes. One that states a hardware fact, a spec or a number falls under the hallucination flags in section 13.

## 15. Sandboxing AI agents

The rule: **an AI agent that can run commands works only inside an isolated environment that holds one study's working copy and nothing else.** No credentials, no synced folders, no other studies.

### Access tiers

| Tier | What the AI can do | Where it's allowed |
|---|---|---|
| 0. Chat | Sees only what is pasted or uploaded | Anywhere |
| 1. Files | Reads and edits files in one working copy, no shell | A working copy outside any synced folder |
| 2. Shell | Runs commands, installs packages, runs scripts | Only inside the sandbox (below) |

### The sandbox

- A "this folder only" option in an app's settings is a guardrail, not a boundary. The boundary is enforced by the operating system: a sandbox or a container.
- Shell-capable agents run on **Linux (WSL2 on the Windows machines) or macOS**. Claude Code's built-in sandbox does not run on native Windows; commands there run unsandboxed.
- The built-in sandbox covers shell commands only, and by default it can still **read** most of the machine. Reads are restricted to the project explicitly.
- These settings live in `.claude/settings.json`, committed with the repo so every machine gets them:

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "filesystem": { "denyRead": ["~/"], "allowRead": ["."] }
  },
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./IRB/**)",
      "Edit(./rawdata/**)",
      "Bash(git commit *)",
      "Bash(git push *)"
    ]
  }
}
```

- If scripts must run inside the sandbox, add the conda install path to `allowRead`; with the home folder read-denied, an environment installed there can't load.
- For longer or unattended work, use a **dev container** (`.devcontainer/` committed in the repo), so the environment is identical on every machine. Never mount `~/.ssh` or any host credential file into it.
- **Check before the first agent session on a machine:**
  - `/status` lists the settings file as loaded.
  - Asking the agent to list the home folder fails.
  - `env` inside the sandbox shows no tokens or keys.
- The settings above come from the Claude Code documentation (read 2026-11-11). They stay an *open* flag in `AI_Disclosure.md` until tested on each machine.

### Working copies and synced folders

- An agent never works inside a Box, Drive or OneDrive folder. A bad edit there syncs to everyone before it can be reviewed.
- **Studies on GitHub:** the agent works in a fresh clone inside the sandbox's own filesystem (in WSL2, the Linux home, not `/mnt/c`). A fresh clone has no git-ignored material (`IRB/`, `rawdata/debug/`), which is intended.
- **Studies that live only in Box or Drive:** copy the files needed into a working folder in the sandbox and run `git init` there (local only is fine), for diffs and rollback. Reviewed results are copied back by hand.
- Nothing leaves the sandbox automatically. Work leaves through a commit the researcher reviewed, or a manual copy.

### Credentials

- The agent's shell never sees credentials: the home folder is read-denied, and no token is exported in the session the agent is launched from.
- The `setx` tokens in section 11 are for scripts run natively on Windows. They are never set inside the sandbox.
- Pushing to GitHub happens from a separate terminal, by the researcher.
- A key that must live in the sandbox environment is scoped to one repository (a fine-grained token or a deploy key), so a leak costs one repo.

### Commits

- The agent does not commit or push (the deny rules above). The researcher reviews `git diff`, writes the commit, adds the `Co-Authored-By:` trailer by hand (section 13) and pushes.
- Commit messages describe the change. They never contain conversation text.
- Before every commit, `git status` shows nothing changed under `rawdata/`. The deny rule stops the agent's file tools, not a shell command, so git is the backstop.
- Repos that will become public run a secret scan (e.g. gitleaks) as a pre-commit hook.

### AI tool files

| File | Rule |
|---|---|
| `.claude/settings.json`, `CLAUDE.md` | Committed. Rules only: never secrets, names or participant details. |
| `.claude/settings.local.json`, `CLAUDE.local.md`, `.claude/agent-memory-local/` | Git-ignored. Personal to one machine. |
| `~/.claude/` (transcripts, prompt history, login) | Never in a synced or shared folder. Stored unencrypted, so retention is shortened (`cleanupPeriodDays`). |

- Transcripts keep everything the agent read. Anything that must not sit on disk in plain text is kept out of its reach by the deny rules.
- When copying a working folder back to Box or Drive, leave out `.claude/`, `CLAUDE.local.md` and `.git/`.

### What stays outside the sandbox

- The experiment itself runs natively on the testing hardware, launched by the researcher.
- The sandbox can't reach the eye tracker, response pad or colorimeter. That is why hardware code stays flagged in `AI_Disclosure.md` until it has been run for real (section 13).

## 16. Collection sheet

One sheet per study, one row per participant. It records what happened in each session and where that participant's data stands.

### Anatomy

| Part | What it holds | Example |
|---|---|---|
| 1. Header | Who was run, who ran them, and when | Participant ID, experimenter, date |
| 2. Body | The steps that were followed, in order: one column per protocol step | Consented, each task, demographics, credit |
| 3. Comments | What happened in the room | Written by the experimenter, at the session |
| 4. Analysis pipeline | Where the data is in processing | `Flag`, plus one status column per task |
| 5. Analysis Notes | What was done to the data, and why | Written by the analyst, after the session |

### Comments vs. Analysis Notes

- **Comments** belong to the experimenter, during or right after the session: deviations, equipment problems, participant behavior. Written once, never edited later.
- **Analysis Notes** belong to the analyst, during processing: corrections, exclusions, scoring decisions. Dated and initialed, so every change is traceable.
- They stay in separate columns:
  - Observation and decision stay distinguishable.
  - The original comment survives every correction.
  - One column can be scanned for open data issues.
- Neither column ever contains names or identifying details (section 12).

### Row colors

The `Flag` column decides the color, and the whole row is colored, not one cell.

| Color | `Flag` value | Meaning |
|---|---|---|
| Green | `NA` or `Flag Resolved` | Complete and clean |
| Red | `Flag` | Needs a correction before analysis |
| Gray | `NO SHOW` | No data to analyse |

A resolved flag stays as `Flag Resolved`. It is never deleted.

### Correct before analysis

1. **Spot.** The experimenter writes the problem in Comments.
2. **Flag.** `Flag` is set to `Flag`, and the row turns red.
3. **Fix.** The correction is made in a script that writes to `prettydata/`. Raw data stays as recorded (section 10).
4. **Log.** What changed, and why, goes in Analysis Notes with initials and date.
5. **Resolve.** `Flag` is set to `Flag Resolved`, and the row turns green.

If a fix turns out to be wrong, delete `prettydata/` and rerun. The original is always there.

## 17. Study README

The `README.md` at the top of each study answers six questions:

1. **What.** The question, the design, and the IRB protocol number.
2. **How to run it.** The environment, the command, and debug mode first.
3. **Where things are.** The folder map. Each data folder has its own README listing every file and the script that writes it.
4. **How to read the sheet.** The collection sheet's columns, row colors and `Flag` values.
5. **Exceptions.** Anything that breaks these conventions, and why.
6. **History.** Who to ask, and dated changes to the protocol.

## 18. Counterbalancing and crash reports

The rule: **the counterbalancing sheet decides every participant's condition, and it only counts participants whose data can be used.**

### The sheet

`experiment_files/counterbalancing.csv` has one row per slot, in the order the slots are filled.

| Column | Holds |
|---|---|
| `Slot` | Unique slot number, never reused |
| `Condition` | The counterbalancing configuration for this slot |
| `Participant` | Study code of whoever filled the slot |
| `Status` | `open`, `assigned`, `complete` or `excluded` |
| `Assigned_At` | When the experiment gave the slot out |
| `Replaces_Slot` | The slot whose lost data this row makes up for |
| `Exclusion_Reason`, `Exclusion_Notes` | Why the participant was excluded |
| `Excluded_By`, `Excluded_At` | RA initials, and when the crash report was filed |

- **The experiment never computes a condition itself.** Each new participant takes the first `open` row, top to bottom. If the sheet is missing or full, the experiment stops and asks.
- The slot is marked `assigned` at the start of run 1, together with `_info.csv` (escapesafe 4), and `complete` at the end of the last block. A resumed session gets the same row back.
- Pilot (`1` to `100`) and debug (`999`) IDs take no slot.
- Only `experiment_files/counterbalancing.py` writes to the sheet. Every change first copies the old sheet to `experiment_files/counterbalancing_backups/`.
- Don't keep the sheet open in Excel during a session: Windows locks the file, and Excel strips leading zeros from IDs when it saves.
- `Assigned_At` and `Excluded_At` are dates tied to a person. They stay in the private repo (section 12).

### Crash report

A session with a problem must not count toward its condition. The crash report (`experiment_files/crash_report.py`) is how an RA records that, in under a minute.

- **How to open it:** start the experiment with the participant's ID and choose *Crash report* in the existing-participant dialog, next to Resume and Overwrite. It also runs on its own (`python experiment_files/crash_report.py`).
- **What the RA enters:** the participant, a reason from a fixed list, optional notes, and their initials. Notes say what happened, never names or identifying details.
- **What it changes, after a second confirmation:**
  - The participant's row is marked `excluded`, with the reason, notes, initials and time.
  - A new `open` row with the same `Condition` is placed at the front of the queue, so the next participant makes up the lost configuration.
- **What it never changes:** the excluded row stays in the sheet, and `rawdata/` is not touched.
- An excluded ID is not reused. If the same person is run again, they get a new ID.
- The RA also writes what happened in the collection sheet's Comments (section 16).

Use it when a session can't be resumed, the eye tracker or other equipment failed, the participant withdrew or didn't follow instructions, or the experimenter made an error. A crash that was resumed and finished needs no crash report.

---

## New-study checklist

- [ ] Folder skeleton with a README in each data folder
- [ ] Start dialog: ID, demographics, counterbalancing, screen width, viewing distance, tracker, debug
- [ ] Existing-participant dialog: resume (last block completed and crash comments), overwrite (confirm, then archive), crash report (exclude with a reason, reopen the slot), cancel
- [ ] `_trials.csv` pre-generated and saved before trial 1
- [ ] `_behav.csv` and `_info.csv` saved at every break, on ESC, and at the end
- [ ] Flip-locked onsets logged and sent as tracker markers with the same timestamp
- [ ] Calibration saved each run
- [ ] Debug mode writing to `rawdata/debug/`
- [ ] Export script with a sync check
- [ ] Debug run completed on the testing machine
- [ ] Participant IDs are study codes (no initials, names or SONA IDs); `Crash_Comments` free of names
- [ ] Repo private during collection; `data-collection-start` tag set when real data collection begins
- [ ] `AI_Disclosure.md` kept up to date, with every flag verified before publication
- [ ] De-identification check done before any public release
- [ ] Every script has the header block, and its Usage matches the flags the script actually accepts
- [ ] `.gitignore` covers `.claude/settings.local.json`, `CLAUDE.local.md` and `.claude/agent-memory-local/`
- [ ] Collection sheet has Comments, `Flag` and Analysis Notes columns; the study README covers all six parts
- [ ] Experiment lives in `experiment_files/` with its counterbalancing sheet; pilot (`1` to `100`) and debug (`999`) IDs take no slot
- [ ] Agent working copy sits outside any synced folder; sandbox settings load (`/status`) and `env` shows no tokens
