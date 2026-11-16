"""
svf_vwm_mini.py — a small, complete version of the SFV reward x VWM experiment.

One session, in this order:
    instructions -> practice -> two blocks (Duration, Dose; order counterbalanced)
    -> memory tests for the videos -> goodbye
Inside a block, for each condition:  reward video(s) -> ratings -> memory-task trials

The memory task is CHANGE DETECTION: colored squares flash up, disappear, then come
back. The participant says whether anything changed (D = different) or not (S = same).

This is the TEACHING version. The real study's code lives in the project folder
(experiment_scripts/: study_config.py, run_session.py, ...). Anything marked
PROVISIONAL is a decision the lab has not settled yet: search for that word.

Run it: open this file in PsychoPy Coder and press the green Run button (Ctrl+R).
Quit early: press Escape at any time.
"""

import random
from pathlib import Path

import pandas as pd
from PIL import Image
from psychopy import core, data, event, gui, visual
from psychopy.hardware import keyboard

# ---------------------------------------------------------------------------
# 1. SETTINGS — change the experiment here, not further down
# ---------------------------------------------------------------------------
DEV_MODE = True                    # True while building/testing. False for real participants.

# --- the memory task (change detection) ---
SET_SIZE = 4                       # PROVISIONAL: squares per array. 3 is probably too easy for
                                   # change detection (everyone near 100%). Pilot to decide.
COLORS = {                         # name -> (R, G, B), each 0-255
    "red":     (220, 40, 40),
    "green":   (40, 170, 70),
    "blue":    (50, 90, 220),
    "yellow":  (240, 210, 40),
    "magenta": (200, 60, 190),
    "cyan":    (40, 190, 200),
    "orange":  (240, 130, 30),
}
SLOTS = [(-0.25, 0.25), (0, 0.25), (0.25, 0.25),      # places a square may appear
         (-0.25, 0),               (0.25, 0),         # (3x3 grid without the center,
         (-0.25, -0.25), (0, -0.25), (0.25, -0.25)]   #  which is where the + goes)
SQUARE_SIZE = 0.1                  # fraction of screen height
BACKGROUND = (128, 128, 128)       # mid-grey
FIXATION_TIME = 0.6                # seconds (a little random jitter is added)
ENCODING_TIME = 0.25               # PROVISIONAL: design doc says 250 ms, the lab's old MATLAB task used 100 ms
RETENTION_TIME = 1.0               # PROVISIONAL: design doc says 1000 ms, the old MATLAB task used 900 ms
MAX_RESPONSE_TIME = 3.0            # seconds before a trial times out
KEYS = {"s": "same", "d": "different"}
N_PRACTICE = 6
TRIALS_PER_CONDITION = 16          # design doc says ~15; 16 splits evenly into change / no-change

# --- the reward videos ---
GENRE = "nature"                   # PROVISIONAL: the real study assigns this from the calibration ratings
VIDEO_ROOT = Path(__file__).parent / "videos"     # videos/<genre>/<bucket>/clip_000.mp4
CONDITIONS = {                     # a condition = which folders to play clips from, and the nominal seconds
    "duration": {
        "control": [],
        "5s":      [("duration_5s", 5)],
        "45s":     [("duration_45s", 45)],
        "120s":    [("duration_120s", 120)],
    },
    "dose": {
        "control": [],
        "1x45s":   [("dose_45s_single", 45)],
        "3x15s":   [("dose_15s_fragment", 15)] * 3,   # PROVISIONAL: 3 different clips (as here) or one clip 3 times?
    },
}
RATING_PROMPTS = {                 # PROVISIONAL: which ratings, and how often? (satisfaction? only some blocks?)
    "wanting": "How much do you want to keep watching more like this?",
    "liking":  "How enjoyable was that?",
}
CLIP_CAP_S = None                  # None = play whole clips. A number = stop each clip after that many seconds.

# --- the memory tests for the videos ---
STILL_ROOT = Path(__file__).parent / "stills"     # made by make_stills.py

if DEV_MODE:                       # shortcuts so a test run takes minutes, not an hour
    TRIALS_PER_CONDITION = 4
    CLIP_CAP_S = 6

# ---------------------------------------------------------------------------
# 2. WHO IS THIS? — a pop-up box for the participant ID
# ---------------------------------------------------------------------------
info = {"participant": ""}
dialog = gui.DlgFromDict(info, title="SFV x VWM")
if not dialog.OK or not info["participant"]:
    core.quit()

START_TIME = data.getDateStr()
DATA_FOLDER = Path(__file__).parent / "data"
DATA_FOLDER.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 3. SET UP — the window, the things we'll draw, the keyboard, and our data lists
# ---------------------------------------------------------------------------
win = visual.Window(size=(1000, 700), color=BACKGROUND, colorSpace="rgb255",
                    units="height", fullscr=not DEV_MODE)
win.mouseVisible = False

fixation = visual.TextStim(win, text="+", height=0.08, color="black")
message = visual.TextStim(win, text="", height=0.04, wrapWidth=1.2, color="black")
caption = visual.TextStim(win, text="", pos=(0, 0.44), height=0.035, wrapWidth=1.3, color="black")
squares = [visual.Rect(win, width=SQUARE_SIZE, height=SQUARE_SIZE, lineColor=None, colorSpace="rgb255")
           for _ in range(SET_SIZE)]

kb = keyboard.Keyboard()

trial_rows = []        # one dictionary per memory-task trial
reward_rows = []       # one per reward delivery
memory_rows = []       # one per memory-test answer
shown_in = {}          # each video file they watched -> the (block, condition) it was shown in


def save_data():
    """Write everything collected so far. Called after every trial, so a crash loses almost nothing."""
    for name, rows in [("trials", trial_rows), ("rewards", reward_rows), ("memory", memory_rows)]:
        if rows:
            filename = DATA_FOLDER / f"{info['participant']}_{START_TIME}_{name}.csv"
            pd.DataFrame(rows).to_csv(filename, index=False)


def quit_experiment():
    save_data()
    win.close()
    core.quit()


def show_message(text):
    """Show a screen of text and wait for the space bar."""
    message.text = text
    message.draw()
    win.flip()
    keys = kb.waitKeys(keyList=["space", "escape"], waitRelease=False)
    if keys[0].name == "escape":
        quit_experiment()


def show_for(text, seconds):
    """Show a screen of text for a fixed time."""
    message.text = text
    message.draw()
    win.flip()
    core.wait(seconds)


def fit_in_box(width, height, box_width, box_height):
    """Biggest size that fits inside the box without stretching the picture."""
    scale = min(box_width / width, box_height / height)
    return (width * scale, height * scale)


# ---------------------------------------------------------------------------
# 4. THE MEMORY TASK — one change-detection trial
# ---------------------------------------------------------------------------
def make_trial(is_change):
    """Decide everything about one trial before showing anything."""
    slots = random.sample(SLOTS, SET_SIZE)             # which places are used
    sample_colors = random.sample(list(COLORS), SET_SIZE)   # which colors (all different)
    test_colors = sample_colors.copy()
    changed_item = None
    if is_change:
        changed_item = random.randrange(SET_SIZE)      # which square will change
        spare = [name for name in COLORS if name not in sample_colors]
        test_colors[changed_item] = random.choice(spare)
    return {"slots": slots, "sample_colors": sample_colors, "test_colors": test_colors,
            "is_change": is_change, "changed_item": changed_item}


def balanced_trial_list(n):
    """n True/False flags, half 'change' and half 'no change', in random order."""
    flags = [True] * (n // 2) + [False] * (n - n // 2)
    random.shuffle(flags)
    return flags


def draw_array(slots, color_names):
    for square, slot, name in zip(squares, slots, color_names):
        square.pos = slot
        square.fillColor = COLORS[name]
        square.draw()


def run_trial(trial, feedback=False):
    # fixation, with a little random jitter so the start can't be predicted
    fixation.draw()
    win.flip()
    core.wait(FIXATION_TIME + random.uniform(0, 0.1))

    # the sample array
    draw_array(trial["slots"], trial["sample_colors"])
    fixation.draw()
    win.flip()
    core.wait(ENCODING_TIME)

    # the blank delay: the participant has to HOLD the colors in memory
    fixation.draw()
    win.flip()
    core.wait(RETENTION_TIME)

    # the test array, and start the RT clock at the exact moment it appears
    draw_array(trial["slots"], trial["test_colors"])
    fixation.draw()
    win.callOnFlip(kb.clock.reset)
    kb.clearEvents()
    win.flip()
    keys = kb.waitKeys(maxWait=MAX_RESPONSE_TIME, keyList=list(KEYS) + ["escape"], waitRelease=False)

    if keys is None:                                   # nothing pressed in time
        response, rt, correct = None, None, 0
    elif keys[0].name == "escape":
        quit_experiment()
    else:
        response = KEYS[keys[0].name]                  # "s" -> "same", "d" -> "different"
        rt = keys[0].rt
        truth = "different" if trial["is_change"] else "same"
        correct = int(response == truth)

    if feedback:
        show_for("Too slow!" if response is None else ("Correct!" if correct else "Wrong"), 0.5)
    return {"response": response, "correct": correct, "rt_s": rt}


def run_practice():
    for is_change in balanced_trial_list(N_PRACTICE):
        run_trial(make_trial(is_change), feedback=True)    # practice is not saved


def run_trials(block, condition):
    for number, is_change in enumerate(balanced_trial_list(TRIALS_PER_CONDITION), start=1):
        trial = make_trial(is_change)
        result = run_trial(trial)
        trial_rows.append({
            "participant": info["participant"],
            "block": block,
            "condition": condition,
            "trial": number,
            "overall_trial": len(trial_rows) + 1,
            "is_change": int(is_change),
            "changed_item": trial["changed_item"],
            "sample_colors": "-".join(trial["sample_colors"]),
            "test_colors": "-".join(trial["test_colors"]),
            "response": result["response"],
            "correct": result["correct"],
            "rt_s": result["rt_s"],
        })
        save_data()


# ---------------------------------------------------------------------------
# 5. THE REWARD — find the clips, play them, ask for ratings
# ---------------------------------------------------------------------------
def find_clips(bucket):
    return sorted((VIDEO_ROOT / GENRE / bucket).glob("*.mp4"))


def choose_clips(plan):
    """plan = [(bucket, seconds), ...]  ->  [(clip file or None, seconds), ...]"""
    used = []
    picks = []
    for bucket, seconds in plan:
        options = [clip for clip in find_clips(bucket) if clip not in used]   # never repeat a clip
        clip = random.choice(options) if options else None    # None = no file on this computer
        used.append(clip)
        picks.append((clip, seconds))
    return picks


def play_clip(clip, seconds):
    """Play one video (or a stand-in screen if the file is missing). Returns (file_s, played_s)."""
    if clip is None:
        message.text = f"[a {seconds} s reward video would play here]"
        message.draw()
        win.flip()
        timer = core.Clock()
        limit = min(seconds, CLIP_CAP_S) if CLIP_CAP_S else seconds
        while timer.getTime() < limit:
            if kb.getKeys(["escape"], waitRelease=False):
                quit_experiment()
            core.wait(0.01)
        return None, round(timer.getTime(), 2)

    message.text = "Get ready..."                       # long videos take a few seconds to load
    message.draw()
    win.flip()
    movie = visual.MovieStim(win, str(clip), units="height")
    movie.size = fit_in_box(*movie.frameSize, win.size[0] / win.size[1], 1)
    timer = None
    while not movie.isFinished:
        movie.draw()
        win.flip()
        if timer is None:
            timer = core.Clock()                       # start timing when the first frame is on screen
        if kb.getKeys(["escape"], waitRelease=False):
            quit_experiment()
        if CLIP_CAP_S and timer.getTime() > CLIP_CAP_S:
            break
    played = timer.getTime()                           # measure before any clean-up
    if not movie.isFinished:                           # we cut it short (DEV cap): silence it
        movie.pause()                                  # (stop() can take seconds on long clips)
    return round(movie.duration, 2), round(played, 2)


def ask_rating(prompt):
    message.text = f"{prompt}\n\n1 = not at all          7 = extremely"
    message.draw()
    win.flip()
    keys = kb.waitKeys(keyList=["1", "2", "3", "4", "5", "6", "7", "escape"], waitRelease=False)
    if keys[0].name == "escape":
        quit_experiment()
    return int(keys[0].name)


def deliver_reward(block, condition):
    plan = CONDITIONS[block][condition]
    row = {"participant": info["participant"], "block": block, "condition": condition, "genre": GENRE,
           "clips": "", "nominal_s": 0, "file_s": 0, "played_s": 0, "wanting": None, "liking": None}
    if plan:                                           # an empty plan = the no-video control
        picks = choose_clips(plan)
        file_total, played_total = 0, 0
        for clip, seconds in picks:
            file_s, played_s = play_clip(clip, seconds)
            file_total += file_s or 0
            played_total += played_s
            if clip is not None:
                shown_in[clip] = (block, condition)
        row["clips"] = ";".join(f"{clip.parent.name}/{clip.name}" if clip else "PLACEHOLDER" for clip, _ in picks)
        row["nominal_s"] = sum(seconds for _, seconds in picks)
        row["file_s"] = round(file_total, 2)
        row["played_s"] = round(played_total, 2)
        for name, prompt in RATING_PROMPTS.items():
            row[name] = ask_rating(prompt)
    reward_rows.append(row)
    save_data()


# ---------------------------------------------------------------------------
# 6. BLOCKS — put it together: reward first, then the memory trials it should affect
# ---------------------------------------------------------------------------
def block_order_for(participant):
    """Even-numbered participants do Duration first, odd-numbered do Dose first."""
    digits = "".join(ch for ch in participant if ch.isdigit())     # "P007" -> "007"
    number = int(digits) if digits else 0
    return ["duration", "dose"] if number % 2 == 0 else ["dose", "duration"]


def run_block(block):
    conditions = list(CONDITIONS[block])
    random.shuffle(conditions)                         # random condition order for each participant
    for condition in conditions:
        deliver_reward(block, condition)
        show_for("Memory task starting...\n\nKeep your eyes on the +", 2)
        run_trials(block, condition)


# ---------------------------------------------------------------------------
# 7. MEMORY TESTS FOR THE VIDEOS — free recall, pick the images, one-by-one
# ---------------------------------------------------------------------------
def still_path(clip, tag):
    return STILL_ROOT / clip.parent.parent.name / clip.parent.name / f"{clip.stem}_{tag}.jpg"


def pick_foils(shown):
    """For each clip they watched, a clip from the same folder that they did NOT watch."""
    foils = []
    for clip in shown:
        options = [c for c in find_clips(clip.parent.name) if c not in shown and c not in foils]
        foils.append(random.choice(options))
    return foils


def build_test_items(shown, foils, tag):
    items = [{"image": still_path(clip, tag), "is_old": True, "shown_in": shown_in[clip]} for clip in shown]
    items += [{"image": still_path(clip, tag), "is_old": False, "shown_in": (None, None)} for clip in foils]
    return items


def make_image(path, box_width, box_height, pos=(0, 0)):
    width, height = Image.open(path).size
    return visual.ImageStim(win, image=str(path), pos=pos,
                            size=fit_in_box(width, height, box_width, box_height))


def log_memory(test, item=None, answer=None, correct=None, rt_s=None, notes=None):
    memory_rows.append({
        "participant": info["participant"],
        "test": test,
        "image": f"{item['image'].parent.name}/{item['image'].name}" if item else None,
        "is_old": int(item["is_old"]) if item else None,
        "block": item["shown_in"][0] if item else None,        # which block/condition the video was in
        "condition": item["shown_in"][1] if item else None,    # (empty for pictures from unseen videos)
        "answer": answer,
        "correct": correct,
        "rt_s": rt_s,
        "notes": notes,
    })


def free_recall():
    show_message("Memory questions\n\nPlease tell the experimenter everything you remember "
                 "about the videos you watched. Take as long as you like.\n\n"
                 "(Experimenter: press SPACE when they are finished.)")
    summary = {"notes": ""}
    gui.DlgFromDict(summary, title="Experimenter: type a quick summary of what they recalled")
    log_memory("free_recall", notes=summary["notes"])
    save_data()


def image_selection(items):
    random.shuffle(items)
    stims = []
    for i, item in enumerate(items):
        pos = ((i % 5 - 2) * 0.28, 0.21 - (i // 5) * 0.27)    # 5 per row
        stims.append(make_image(item["image"], 0.24, 0.24, pos))
    frame = visual.Rect(win, lineColor="yellow", lineWidth=5, fillColor=None)
    caption.text = "Click every picture you remember seeing in the videos.   Press SPACE when you are done."
    mouse = event.Mouse(win=win)
    win.mouseVisible = True
    chosen = set()
    was_down = False
    while True:
        is_down = mouse.getPressed()[0]
        if is_down and not was_down:                   # a fresh click, not a held button
            for i, stim in enumerate(stims):
                if stim.contains(mouse):
                    if i in chosen:
                        chosen.remove(i)
                    else:
                        chosen.add(i)
        was_down = is_down
        caption.draw()
        for i, stim in enumerate(stims):
            stim.draw()
            if i in chosen:
                frame.pos, frame.size = stim.pos, stim.size + 0.02
                frame.draw()
        win.flip()
        keys = kb.getKeys(["space", "escape"], waitRelease=False)
        if keys and keys[0].name == "escape":
            quit_experiment()
        if keys:
            break
    win.mouseVisible = False
    for i, item in enumerate(items):
        picked = int(i in chosen)
        log_memory("selection", item, picked, int(picked == item["is_old"]))
    save_data()


def recognition(items):
    random.shuffle(items)
    caption.text = "Did you see this picture in one of the videos?        Y = yes        N = no"
    for item in items:
        picture = make_image(item["image"], 1.2, 0.8)
        picture.draw()
        caption.draw()
        win.callOnFlip(kb.clock.reset)
        kb.clearEvents()
        win.flip()
        keys = kb.waitKeys(keyList=["y", "n", "escape"], waitRelease=False)
        if keys[0].name == "escape":
            quit_experiment()
        said_old = keys[0].name == "y"
        log_memory("recognition", item, int(said_old), int(said_old == item["is_old"]), keys[0].rt)
    save_data()


def run_memory_tests():
    if not shown_in:
        show_message("No real video files were played, so there is nothing to test.\n\nPress SPACE.")
        return
    shown = list(shown_in)
    foils = pick_foils(shown)
    selection_items = build_test_items(shown, foils, "a")
    recognition_items = build_test_items(shown, foils, "b")   # other moments from the same clips
    missing = [item["image"] for item in selection_items + recognition_items if not item["image"].exists()]
    if missing:
        show_message(f"{len(missing)} still image(s) are missing.\n\nRun make_stills.py first.\n\nPress SPACE.")
        return
    free_recall()                                      # first: nothing to jog their memory yet
    image_selection(selection_items)
    recognition(recognition_items)


# ---------------------------------------------------------------------------
# 8. THE SESSION
# ---------------------------------------------------------------------------
show_message(
    "Welcome!\n\n"
    "You will do a memory task, and watch some short videos between parts of it.\n\n"
    "In the memory task, some colored squares flash up, disappear, and then come back.\n"
    "Press  D  if ANY square changed color.\n"
    "Press  S  if they are all the SAME.\n\n"
    "Press SPACE to practice."
)
run_practice()
show_message("Practice is over.\n\nWatch the videos as you normally would. Sound is on.\n\nPress SPACE to begin.")

for number, block in enumerate(block_order_for(info["participant"])):
    if number > 0:
        show_message("Short break.\n\nPress SPACE when you are ready to continue.")
    run_block(block)

run_memory_tests()

# ---------------------------------------------------------------------------
# 9. GOODBYE
# ---------------------------------------------------------------------------
save_data()
show_message("Thank you! You are finished.\n\nPlease let the experimenter know.")
win.close()
core.quit()
