"""
animals_plants_starter.py — fill in the TODOs during the workshop.
The finished version is animals_plants.py.

This file RUNS at every step. Run it after each TODO to see what changed.

8 words (4 animals, 4 plants) are shown one at a time in random order.
The participant presses  A  if it's an Animal, or  P  if it's a Plant.
We record which key they pressed, whether it was correct, and how fast they were.

Run it: open this file in PsychoPy Coder and press the green Run button (Ctrl+R).
Quit early: press Escape at any time during a trial.
"""

import random
from pathlib import Path

import pandas as pd
from psychopy import core, data, gui, visual
from psychopy.hardware import keyboard

# ---------------------------------------------------------------------------
# 1. SETTINGS — change the experiment here, not further down
# ---------------------------------------------------------------------------
STIMULI = [
    {"word": "dog",    "category": "animal"},
    {"word": "oak",    "category": "plant"},
    # TODO 1: add 3 more animals and 3 more plants (8 stimuli in total)
]
KEYS = {"a": "animal", "p": "plant"}   # which key means which answer
FIXATION_TIME = 0.5                    # seconds the + is on screen
MAX_RESPONSE_TIME = 3.0                # seconds before a trial times out
FEEDBACK_TIME = 0.5                    # seconds "Correct!" / "Wrong" stays up

# ---------------------------------------------------------------------------
# 2. WHO IS THIS? — a pop-up box for the participant ID
# ---------------------------------------------------------------------------
info = {"participant": "", "session": "1"}
dialog = gui.DlgFromDict(info, title="Animals & Plants")
if not dialog.OK:          # they clicked Cancel
    core.quit()

# ---------------------------------------------------------------------------
# 3. SET UP — the window, the things we'll draw, and the keyboard
# ---------------------------------------------------------------------------
win = visual.Window(size=(1000, 700), color="black", units="height", fullscr=False)

fixation = visual.TextStim(win, text="+", height=0.08)
word = visual.TextStim(win, text="", height=0.1)
feedback = visual.TextStim(win, text="", height=0.06)
message = visual.TextStim(win, text="", height=0.04, wrapWidth=1.2)

kb = keyboard.Keyboard()


def show_message(text):
    """Show a screen of text and wait for the space bar."""
    message.text = text
    message.draw()
    win.flip()
    kb.waitKeys(keyList=["space"])


# ---------------------------------------------------------------------------
# 4. INSTRUCTIONS
# ---------------------------------------------------------------------------
show_message(
    "You will see a word.\n\n"
    "Press  A  if it is an ANIMAL\n"
    "Press  P  if it is a PLANT\n\n"
    "Be as fast and accurate as you can.\n\n"
    "Press SPACE to start."
)

# ---------------------------------------------------------------------------
# 5. TRIAL LOOP — shuffle, then run every trial
# ---------------------------------------------------------------------------
trials = STIMULI.copy()
# TODO 2: shuffle the trials so every participant gets a new random order

results = []               # we'll add one dictionary per trial

for trial_number, trial in enumerate(trials, start=1):

    # (a) fixation cross
    fixation.draw()
    win.flip()
    core.wait(FIXATION_TIME)

    # (b) the word — start the RT clock at the exact moment it appears
    # TODO 3: put this trial's word on the screen
    #         (set word.text, then draw it)
    win.callOnFlip(kb.clock.reset)
    kb.clearEvents()
    win.flip()

    # (c) wait for a response (or time out)
    keys = kb.waitKeys(maxWait=MAX_RESPONSE_TIME, keyList=list(KEYS) + ["escape"])

    if keys is None:                       # no key pressed in time
        response, rt, correct = None, None, 0
        feedback.text = "Too slow!"
    elif keys[0].name == "escape":         # emergency exit
        break
    else:
        response = KEYS[keys[0].name]      # "a" -> "animal", "p" -> "plant"
        rt = keys[0].rt                    # seconds since the word appeared
        correct = 0   # TODO 4: 1 if response matches the trial's category, else 0
        feedback.text = "Correct!" if correct else "Wrong"

    # (d) feedback
    feedback.draw()
    win.flip()
    core.wait(FEEDBACK_TIME)

    # (e) save this trial's data
    results.append({
        "participant": info["participant"],
        "session": info["session"],
        "trial": trial_number,
        "word": trial["word"],
        "category": trial["category"],
        "response": response,
        "correct": correct,
        # TODO 5: also save the reaction time
    })

# ---------------------------------------------------------------------------
# 6. SAVE — one CSV per participant, in a "data" folder next to this script
# ---------------------------------------------------------------------------
data_folder = Path(__file__).parent / "data"
data_folder.mkdir(exist_ok=True)
filename = data_folder / f"{info['participant']}_session{info['session']}_{data.getDateStr()}.csv"
pd.DataFrame(results).to_csv(filename, index=False)

# ---------------------------------------------------------------------------
# 7. GOODBYE
# ---------------------------------------------------------------------------
n_correct = sum(r["correct"] for r in results)
show_message(f"Done! You got {n_correct} of {len(results)} correct.\n\nPress SPACE to exit.")

win.close()
core.quit()
