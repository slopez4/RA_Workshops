"""
Project:       RA Workshops, Workshop 6 (advanced experiment scripting)
Script:        06_advanced_psychopy/grouping_task.py
Creator:       <name> (AI-assisted: Claude)
Purpose:       A small version of the lab's Repetition Discrimination Task (RDT):
               9 shapes in a row, one adjacent pair repeats, and a grouping cue
               (proximity, color similarity, common region) puts that pair WITHIN
               one group or BETWEEN two. The participant reports which shape
               repeated. Built to show the habits in STUDY_CONVENTIONS.md: the
               whole trial sequence is generated and saved before trial 1, timing
               is counted in frames, files are saved at every break (never during
               a stimulus), ESC and crashes save before quitting, and a crashed
               session can be resumed with the same trials.
Last updated:  2026-11-15

Usage:
    Open in PsychoPy Coder and press Run (or: python grouping_task.py).
    Participant ID 999 = debug: short blocks, a small window, files in data/debug/.

    Testing without a person (a "simulated participant"):
    python grouping_task.py --auto                  ID 999, answers by itself, no dialogs
    python grouping_task.py --auto --crash-at 30    pretend the script crashes on trial 30
    python grouping_task.py --auto --resume         resume the last 999 session
    python grouping_task.py --auto --sub 101        a real-ID run (needs the counterbalancing sheet)

    Dialogs: start (Participant ID) -> if that ID already has files:
    Resume (enter crash comments) / Overwrite (confirm twice, old files archived) /
    Crash report (exclude the participant, reopen their slot) / Cancel.

Dependencies:  psychopy (2026.1), pandas, trial_matrix.py, counterbalancing.py,
               crash_report.py (all in this folder). Keyboard + monitor only.
Reads:         data/<subid>_info.csv, data/<subid>_trials.csv, data/<subid>_behav.csv
               (only when resuming), counterbalancing.csv
Writes:        data/<subid>_trials.csv   the plan, written before trial 1
               data/<subid>_behav.csv    every trial: responses, RTs, onsets
               data/<subid>_info.csv     one row per run: who, when, status, setup
               data/overwritten/<subid>_<timestamp>/   old files after an overwrite
               (debug ID 999: the same files in data/debug/)
               counterbalancing.csv (through counterbalancing.py)
"""

import argparse
import os
import random
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd
from psychopy import __version__ as PSYCHOPY_VERSION
from psychopy import core, gui, visual
from psychopy.hardware import keyboard

import counterbalancing as cb
import trial_matrix as tm

# ===========================================================================
# 1. SETTINGS: everything you might change is here, with its unit.
# ===========================================================================
HERE = Path(__file__).resolve().parent        # paths come from this file, never
DATA_DIR = HERE / "data"                      # from the folder Python was started in
DEBUG_DIR = DATA_DIR / "debug"
DEBUG_ID = "999"                              # STUDY_CONVENTIONS.md, section 2

N_BLOCKS = 2              # main blocks (56 trials each; debug: 14)
FIXATION_S = 0.5          # seconds, fixation cross before each display
MAX_RESPONSE_S = 3.0      # seconds the display stays up if nobody answers
ITI_S = 0.5               # seconds of blank screen between trials
FEEDBACK_S = 0.8          # seconds, practice feedback only
FALLBACK_HZ = 60          # used only if the refresh rate can't be measured (a warning is printed)

ITEM_SIZE = 0.04          # 'height' units: fraction of the screen height
SPACING = 0.1             # distance between neighbouring shape centres, 'height' units
BACKGROUND = [0.5, 0.5, 0.5]   # mid-gray in rgb1 (0-1) space, the lab's background

# Counterbalancing: which key means which shape. The sheet (counterbalancing.csv)
# decides A or B for real participants; pilot and debug IDs take no slot and get A.
KEY_MAPS = {"A": {"SQUARE": "n", "CIRCLE": "m"},
            "B": {"SQUARE": "m", "CIRCLE": "n"}}
UNSLOTTED_CONDITION = "A"
QUIT_KEY = "escape"


class QuitRequested(Exception):
    """Raised when the experimenter presses ESC, so ONE place saves and quits."""


# ===========================================================================
# 2. FILES: every disk read and write in the experiment goes through here.
# ===========================================================================
def paths_for(subid, debug):
    folder = DEBUG_DIR if debug else DATA_DIR
    return {kind: folder / f"{subid}_{kind}.csv" for kind in ("trials", "behav", "info")}


def write_csv(table, path):
    """Write to a temporary file, then swap it in. A crash mid-write can never
    leave a half-written data file (the same trick counterbalancing.py uses)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    table.to_csv(tmp, index=False)
    os.replace(tmp, path)


def archive(paths, subid):
    """Overwrite = MOVE the old files to overwritten/<subid>_<timestamp>/. Never delete."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = paths["info"].parent / "overwritten" / f"{subid}_{stamp}"
    target.mkdir(parents=True)
    for path in paths.values():
        if path.exists():
            shutil.move(str(path), str(target / path.name))
    print("Old files moved to", target)


def save(state):
    """Rewrite _behav.csv and _info.csv. Called ONLY at breaks and on the way
    out (ESC, crash, end), never while a stimulus is on screen."""
    write_csv(pd.DataFrame(state["behav"]), state["paths"]["behav"])
    write_csv(pd.DataFrame(state["runs"]), state["paths"]["info"])


# ===========================================================================
# 3. DIALOGS: who is this, and is it a new session or a resumed one?
# ===========================================================================
def dialog_values(data):
    """Dlg.show() returns a list in older PsychoPy and a dict in newer ones."""
    return list(data.values()) if isinstance(data, dict) else list(data)


def ask_participant():
    info = {"Participant ID": ""}
    dlg = gui.DlgFromDict(info, title="Grouping task")
    if not dlg.OK:
        core.quit()
    subid = str(info["Participant ID"]).strip()
    if cb.id_kind(subid) == "unknown":
        gui.criticalDlg("Grouping task", "The ID must contain a number (study codes: 101 and up).")
        core.quit()
    return subid


def ask_existing(subid):
    """Existing participant: Resume / Overwrite / Crash report / Cancel."""
    dlg = gui.Dlg(title="Participant %s already has data" % subid)
    dlg.addField("What now?", choices=["Resume incomplete experiment", "Overwrite participant",
                                       "Crash report", "Cancel"])
    dlg.addField("Crash comments (for Resume; what happened, no names)", initial="")
    values = dialog_values(dlg.show())
    if not dlg.OK:
        return "Cancel", ""
    return values[0].split()[0], str(values[1]).strip()


def confirm_overwrite(subid):
    """Second step of an overwrite, so it never happens by accident."""
    dlg = gui.Dlg(title="Overwrite %s?" % subid)
    dlg.addText("The old files will be MOVED to an 'overwritten' folder, not deleted.")
    dlg.addText("Press OK to overwrite participant %s, Cancel to stop." % subid)
    dlg.show()
    return dlg.OK


# ===========================================================================
# 4. STARTING A SESSION: new (run 1) or resumed (run 2, 3, ...)
# ===========================================================================
def new_session(subid, debug, paths):
    """Pick the condition, build and SAVE the whole trial plan, write _info.csv.

    Everything a resume needs is on disk before the first trial is shown
    (escapesafes 1 and 4 in STUDY_CONVENTIONS.md).
    """
    if cb.id_kind(subid) == "real":
        condition = cb.assign(subid)            # the sheet decides; raises SheetError if full
    else:
        condition = UNSLOTTED_CONDITION
    keys = KEY_MAPS[condition]
    seed = random.randrange(1, 10**6)           # saved, so the plan can be rebuilt if ever needed
    trials = tm.build_session(N_BLOCKS, seed, debug=debug)
    trials = tm.add_response_keys(trials, keys["SQUARE"], keys["CIRCLE"])
    write_csv(trials, paths["trials"])
    run = {"Participant": subid, "Run": 1, "Status": "running",
           "Session_Start": now(), "Session_End": "", "Start_Block": 0,
           "Last_Block_Completed": -1,           # -1 = not even practice yet
           "Condition": condition, "Key_Square": keys["SQUARE"], "Key_Circle": keys["CIRCLE"],
           "Seed": seed, "Is_Debug": debug, "Dropped_Frames": 0, "Crash_Comments": ""}
    return {"trials": trials, "behav": [], "runs": [run], "paths": paths}


def resume_session(subid, paths, comments):
    """Reload the saved plan and continue after the last completed block.

    Condition and keys come from run 1, so they can't drift (escapesafe 9).
    Rows from a block that was interrupted stay in the file, marked Valid = False.
    """
    runs = pd.read_csv(paths["info"], dtype={"Participant": str}).to_dict("records")
    trials = pd.read_csv(paths["trials"])
    behav = (pd.read_csv(paths["behav"], dtype={"Participant": str}).to_dict("records")
             if paths["behav"].exists() else [])
    last_done = int(runs[-1]["Last_Block_Completed"])
    for row in behav:
        if row["Block_Num"] > last_done:
            row["Valid"] = False                # superseded: this block is re-run from the start
    run = dict(runs[0])
    run.update({"Run": int(runs[-1]["Run"]) + 1, "Status": "running", "Session_Start": now(),
                "Session_End": "", "Start_Block": last_done + 1,
                "Last_Block_Completed": last_done, "Dropped_Frames": 0,
                "Crash_Comments": comments})
    return {"trials": trials, "behav": behav, "runs": runs + [run], "paths": paths}


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ===========================================================================
# 5. THE SCREEN: window and every stimulus, created ONCE before the trials.
#    Creating stimuli inside the trial loop is slow and can drop frames.
# ===========================================================================
def setup_screen(debug):
    win = visual.Window(size=(1000, 700) if debug else (1920, 1080), fullscr=not debug,
                        color=BACKGROUND, colorSpace="rgb1", units="height", allowGUI=debug)
    win.mouseVisible = debug
    hz = win.getActualFrameRate(nIdentical=20, nMaxFrames=120, threshold=1)
    if hz is None:
        print("WARNING: could not measure the refresh rate; assuming", FALLBACK_HZ, "Hz.")
        hz = FALLBACK_HZ
    win.refreshThreshold = 1 / hz + 0.004   # a frame longer than this counts as dropped
    stims = {
        "SQUARE": [visual.Rect(win, width=ITEM_SIZE, height=ITEM_SIZE, lineWidth=0)
                   for _ in range(tm.N_ITEMS)],
        "CIRCLE": [visual.Circle(win, radius=ITEM_SIZE / 2, edges=64, lineWidth=0)
                   for _ in range(tm.N_ITEMS)],
        "boxes": [visual.Rect(win, width=SPACING + 1.5 * ITEM_SIZE, height=1.5 * ITEM_SIZE,
                              lineColor="white", fillColor=None, lineWidth=3)
                  for _ in range(4)],
        "fixation": visual.TextStim(win, text="+", height=0.05, color="black"),
        "message": visual.TextStim(win, text="", height=0.035, color="black", wrapWidth=1.3),
    }
    return win, round(hz, 2), stims


def prepare_display(stims, row):
    """Move and color the pre-made shapes for this trial. Returns what to draw.

    Called during the fixation, so all the work is done before the display's flip.
    """
    display = tm.layout(row["Cue"], row["WBN"], int(row["Targ_Pos"]), row["Targ_Type"])
    to_draw = []
    for i, shape in enumerate(display["shapes"]):
        stim = stims[shape][i]
        stim.pos = (display["x"][i] * SPACING, 0)
        stim.color = display["colors"][i]
        to_draw.append(stim)
    for box, centre in zip(stims["boxes"], display["boxes"]):
        box.pos = (centre * SPACING, 0)
        to_draw.append(box)                      # frames drawn last, on top
    return to_draw


def frames(seconds, hz):
    """Durations are counted in screen refreshes: 0.5 s at 60 Hz = 30 frames."""
    return max(1, round(seconds * hz))


# ===========================================================================
# 6. KEYS: ESC is checked on every frame of every screen.
# ===========================================================================
def check_quit(kb):
    if kb.getKeys(keyList=[QUIT_KEY], waitRelease=False):
        raise QuitRequested


def show_frames(win, kb, to_draw, n_frames):
    """Show the same screen for exactly n_frames, checking ESC on each one."""
    for _ in range(n_frames):
        for stim in to_draw:
            stim.draw()
        win.flip()
        check_quit(kb)


def message(win, kb, stims, text, auto):
    """A text screen that waits for space (or ESC). The autopilot skips the wait."""
    stims["message"].text = text
    stims["message"].draw()
    win.flip()
    if auto:
        core.wait(0.2)
        return
    kb.clearEvents()                 # a space pressed DURING the block must not skip this screen
    keys = kb.waitKeys(keyList=["space", QUIT_KEY])
    if keys[0].name == QUIT_KEY:
        raise QuitRequested


# ===========================================================================
# 7. ONE TRIAL: fixation -> display until response or timeout -> blank ITI
# ===========================================================================
def run_trial(win, kb, stims, row, hz, auto, rng):
    to_draw = prepare_display(stims, row)
    show_frames(win, kb, [stims["fixation"]], frames(FIXATION_S, hz))

    # Throw away any key pressed before the display (e.g. a response key pressed
    # while the break screen was up), and start the RT clock ON the flip that
    # shows it. The lab's RDT02_Lab.py did neither, and logged negative RTs.
    kb.clearEvents()
    win.callOnFlip(kb.clock.reset)

    response_keys = [row["Correct_Key"], "n" if row["Correct_Key"] == "m" else "m"]
    auto_frame = rng.randint(frames(0.4, hz), frames(1.2, hz))   # simulated participant's RT
    onset, key, rt = None, "", None
    for frame in range(frames(MAX_RESPONSE_S, hz)):
        for stim in to_draw:
            stim.draw()
        flip_time = win.flip()
        if frame == 0:
            onset = flip_time                      # the display's real onset, from the flip
        pressed = kb.getKeys(keyList=response_keys + [QUIT_KEY], waitRelease=False)
        if any(k.name == QUIT_KEY for k in pressed):
            raise QuitRequested
        if pressed:
            key, rt = pressed[0].name, pressed[0].rt
            break
        if auto and frame == auto_frame:
            key = row["Correct_Key"] if rng.random() < 0.9 else response_keys[1]
            rt = frame / hz
            break

    correct = int(key == row["Correct_Key"])
    if row["Block_Num"] == 0:                      # practice: tell them how they did
        stims["message"].text = "Correct" if correct else (
            "Too slow" if not key else "Incorrect")
        show_frames(win, kb, [stims["message"]], frames(FEEDBACK_S, hz))
    show_frames(win, kb, [], frames(ITI_S, hz))    # blank screen

    return {"Response_Key": key, "Is_Correct": correct, "RT": rt,
            "Is_Timeout": key == "", "Onset_Time": onset}


# ===========================================================================
# 8. THE SESSION: blocks from where we start to the end, saving at each break
# ===========================================================================
def run_blocks(win, kb, stims, state, hz, auto, crash_at):
    run = state["runs"][-1]
    keys = {"SQUARE": run["Key_Square"], "CIRCLE": run["Key_Circle"]}
    rng = random.Random()
    message(win, kb, stims,
            "Each display shows a row of squares and circles.\n"
            "One pair of neighbours is the SAME shape.\n\n"
            f"Which shape repeats?\n\n'{keys['SQUARE']}' = SQUARE      '{keys['CIRCLE']}' = CIRCLE\n\n"
            "Answer as fast as you can without making mistakes.\n\nPress SPACE to start.",
            auto)

    trials = state["trials"]
    for block in range(int(run["Start_Block"]), N_BLOCKS + 1):
        block_trials = trials[trials["Block_Num"] == block]
        win.recordFrameIntervals = True          # count dropped frames during trials only
        dropped_before = win.nDroppedFrames
        for _, row in block_trials.iterrows():
            if crash_at is not None and row["Trial_ID"] == crash_at:
                raise RuntimeError("Simulated crash on trial %d (--crash-at)" % crash_at)
            result = run_trial(win, kb, stims, row, hz, auto, rng)
            state["behav"].append({"Participant": run["Participant"], "Run": run["Run"],
                                   **row[["Trial_ID", "Block_Num", "Trial_Num", "Is_Practice",
                                          "Cue", "WBN", "Targ_Pos", "Targ_Type",
                                          "Correct_Key"]].to_dict(),
                                   **result, "Valid": True})
        win.recordFrameIntervals = False

        # The break: the ONLY time files are written during a session.
        run["Last_Block_Completed"] = block
        run["Dropped_Frames"] += win.nDroppedFrames - dropped_before
        save(state)

        done = [r for r in state["behav"] if r["Block_Num"] == block and r["Run"] == run["Run"]]
        accuracy = sum(r["Is_Correct"] for r in done) / len(done)
        if block == 0:
            text = f"Practice done ({accuracy:.0%} correct).\n\nNow the real blocks.\n\nPress SPACE."
        elif block < N_BLOCKS:
            text = f"Block {block} of {N_BLOCKS} done.\n\nTake a short break.\n\nPress SPACE to continue."
        else:
            text = "All done, thank you!\n\nPlease get the experimenter."
        message(win, kb, stims, text, auto)


def finish(state, status):
    """The single exit path: stamp the run, save everything, update the sheet."""
    run = state["runs"][-1]
    run["Status"] = status
    run["Session_End"] = now()
    save(state)
    if status == "complete" and cb.id_kind(run["Participant"]) == "real":
        cb.mark_complete(run["Participant"])
    print(f"Participant {run['Participant']} run {run['Run']}: {status}, "
          f"last block completed = {run['Last_Block_Completed']}")
    print("Files:", state["paths"]["behav"].parent)


# ===========================================================================
# 9. MAIN: dialogs -> session -> screen -> blocks -> one exit path
# ===========================================================================
def parse_args():
    parser = argparse.ArgumentParser(description="Grouping task (mini RDT).")
    parser.add_argument("--auto", action="store_true",
                        help="simulated participant: no dialogs, answers by itself")
    parser.add_argument("--sub", default=DEBUG_ID, help="participant ID for --auto (default 999)")
    parser.add_argument("--resume", action="store_true", help="with --auto: resume, don't overwrite")
    parser.add_argument("--crash-at", type=int, default=None, metavar="TRIAL_ID",
                        help="raise an error on this trial, to practise resuming")
    return parser.parse_args()


def main():
    args = parse_args()
    subid = args.sub if args.auto else ask_participant()
    debug = subid == DEBUG_ID
    paths = paths_for(subid, debug)

    try:
        if paths["info"].exists():
            if args.auto:
                choice, comments = ("Resume", "--auto resume") if args.resume else ("Overwrite", "")
            else:
                choice, comments = ask_existing(subid)
            if choice == "Cancel":
                core.quit()
            if choice == "Crash":
                import crash_report
                crash_report.run(subid)
                core.quit()
            if choice == "Overwrite":
                if not args.auto and not confirm_overwrite(subid):
                    core.quit()
                archive(paths, subid)
                state = new_session(subid, debug, paths)
            else:
                state = resume_session(subid, paths, comments)
        else:
            state = new_session(subid, debug, paths)
    except cb.SheetError as err:
        # Missing or full sheet, or an excluded ID: stop and tell the experimenter.
        if not args.auto:
            gui.criticalDlg("Counterbalancing", str(err))
        raise SystemExit(str(err))
    if state["runs"][-1]["Start_Block"] > N_BLOCKS:
        raise SystemExit(f"Participant {subid} already completed every block. Nothing to resume.")
    save(state)                                   # _info.csv exists before anything is shown

    win, hz, stims = setup_screen(debug)
    state["runs"][-1].update({"Refresh_Hz": hz, "PsychoPy_Version": PSYCHOPY_VERSION})
    kb = keyboard.Keyboard()
    print(f"Participant {subid}, run {state['runs'][-1]['Run']}, starting at block "
          f"{state['runs'][-1]['Start_Block']}, {hz} Hz")

    try:
        run_blocks(win, kb, stims, state, hz, args.auto, args.crash_at)
        finish(state, "complete")
    except QuitRequested:
        finish(state, "aborted")                  # ESC: save first, then quit
    except Exception:
        finish(state, "crashed")                  # anything else: save, then show the error
        raise
    finally:
        win.close()
    core.quit()


if __name__ == "__main__":
    main()
