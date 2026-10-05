# Teaching Guide — Your First PsychoPy Experiment

For whoever is running the session: prep, a minute-by-minute script, TODO answers, and troubleshooting.

---

## 1. Before the session

### One week before
- [ ] Install **PsychoPy 2026.1 Standalone** on every lab computer RAs will use.
- [ ] On **each** computer: open PsychoPy, switch to Coder, and run `animals_plants_starter.py` once. This catches keyboard permissions (Mac), first-launch prompts, and a missing Coder view before class.
- [ ] Make sure GitHub Pages is on, so the [slides link](https://slopez4.github.io/RA_Workshops/02_psychopy_experiment/slides.html) works.

### Day before
- [ ] Run both `animals_plants_starter.py` and `animals_plants.py` on the machine you'll present from.
- [ ] Optional: put the workshop folder on each lab computer's Desktop so RAs can skip the ZIP download (slide 3).
- [ ] If a computer misbehaves, pair that RA with a neighbour (pairing is fine for this workshop).

### 10 minutes before
- [ ] Open the slides (press `F` for fullscreen) and PsychoPy Coder with `animals_plants_starter.py`.
- [ ] Increase Coder's font size (**View → Zoom in**, or Preferences → Coder → font size) so code is readable on the projector.
- [ ] Keep `animals_plants.py` open in a second Coder tab as your cheat sheet.

---

## 2. How to teach it

- **Live-code in the starter file** while RAs type the same thing in theirs. Don't paste from the solution; typing slowly is the point.
- **Run after every TODO.** The starter is built so it always runs, and each TODO makes a visible change. Seeing the change is what makes it stick.
- For each TODO, give **60–90 seconds**, then type the answer on screen. The answers are behind the *TODO* toggles on the slides, so RAs can check themselves.
- The PsychoPy window covers your code when it runs. Tell RAs to look at the slides or your screen *after* they've played the trials.
- **Two ideas matter more than any syntax:** (1) *draw → flip* controls when things appear, and RTs are timed from the flip; (2) *one row per trial, with everything you need to analyse it later.* Come back to both often.

---

## 3. Minute-by-minute script

### 0:00–0:03 · Setup check (slides 1–3)
- "Thumbs up if you've already run the starter and seen two trials."
- Anyone stuck → pair them with a neighbour now; sort out that computer after class.

### 0:03–0:07 · Big picture (slides 4–5)
- **Builder vs Coder:** "Builder writes a Python script like ours behind the scenes. Today we write it ourselves so Builder stops being a black box."
- **Anatomy of a trial:** point at the three screens. "Every experiment you'll run in this lab is a version of this: something to look at, something to respond to, maybe feedback, repeated in some order."

### 0:07–0:14 · Walk through the script (slides 6–10)
- Scroll the starter top to bottom, naming the 7 sections. Point out the parallel with Workshop 1: **settings at the top**.
- **Dialog:** "That pop-up box is this one line. The participant ID ends up in the file name and on every row."
- **Window:** `units="height"` makes sizes a fraction of screen height; `fullscr=False` while developing.
- **draw → flip (slide 9), the key concept.** Whiteboard analogy: draw on a hidden whiteboard, then flip it around to face the room. Ask the 🤔 question.
  *Answer:* draw without flip shows nothing. Flipping everything at once gives one exact onset time, which RTs are measured from.
- **Functions (slide 10):** "`def` = teach Python a new command. We use it for instructions *and* the goodbye screen."

### 0:14–0:19 · TODO 1 & 2 (slides 7, 11)
- **TODO 1:** add 3 animals + 3 plants. Any words work; the solution uses eagle, salmon, frog / fern, cactus, tulip. Watch for missing commas and quotes.
- **TODO 2:** `random.shuffle(trials)`.
- **Run it.** RAs should now get 8 trials but **blank screens** where the word should be (TODO 3 isn't done). Say: "That's what *draw without text* looks like. Let's fix it."
- 🤔 *Why randomize?* Fixed orders confound the stimulus with its position: practice, fatigue, rhythm. Randomizing spreads those effects evenly. Because order differs per person, we save the word on every row.

### 0:19–0:27 · TODO 3 & 4 (slides 12–13)
- **TODO 3:**
  ```python
  word.text = trial["word"]
  word.draw()
  ```
  Then explain the next three given lines: `callOnFlip(kb.clock.reset)` starts the RT clock *at the moment the word appears*, not when the code ran; `clearEvents()` throws away keys pressed during fixation.
- **Run it.** Words appear, but **every answer says "Wrong."** Ask why → `correct = 0`.
- **TODO 4:** `correct = int(response == trial["category"])`. `==` gives True/False; `int()` makes 1/0, the same `correct` column as Workshop 1.
- Walk through the `if / elif / else`: timeout → `None`; escape → `break` (leaves the loop, still saves what we have); otherwise score it.

### 0:27–0:32 · TODO 5, run, open the data (slides 14–15)
- **TODO 5:** add `"rt_s": rt,` to the dictionary.
- **Run it for real.** Then open `data/` next to the script and open the CSV (Excel, Numbers, or Coder itself).
- 🤔 *Empty response and RT on a row?* A timeout: they didn't press within 3 s.
  🤔 *Why is your neighbour's order different?* The shuffle.
  🤔 *Crash on trial 7?* Everything is lost, because we save only at the end. Real experiments save after every trial; PsychoPy's `ExperimentHandler` (which Builder uses) does this automatically.

### 0:32–0:40 · Make it yours & wrap-up (slides 17–20)
- Let RAs pick one extension. Quick answers:
  - Arrow keys: `KEYS = {"left": "animal", "right": "plant"}` **and** update the instruction text.
  - Yellow word: `visual.TextStim(win, text="", height=0.1, color="yellow")`.
  - Each word twice: `trials = STIMULI * 2` (instead of `STIMULI.copy()`), then shuffle.
  - Break screen: inside the loop, at the top: `if trial_number == 5: show_message("Take a break. Press SPACE.")`.
  - Images: add `"image": "dog.png"` to each stimulus, create `pic = visual.ImageStim(win, size=0.4)`, then `pic.image = trial["image"]; pic.draw()`.
- Point to **slide 17** (install PsychoPy on your own computer) for anyone who wants to keep practicing, and remind RAs to save their script before leaving the lab computer.
- Wrap-up: "You've built what Builder builds. The CSV you just made is exactly the kind of file we analysed in Workshop 1."

---

## 4. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Keys do nothing (Mac) | macOS hasn't granted keyboard access | *System Settings → Privacy & Security* → enable PsychoPy under **Input Monitoring** and **Accessibility**, then **restart PsychoPy** |
| macOS says the app can't be opened | Gatekeeper | *Privacy & Security → Open Anyway* |
| Window frozen / stuck on a screen | Waiting for a key it isn't getting, or it lost focus | Click the PsychoPy window, press `Esc` (during a trial) or `Space` (on a text screen); otherwise the red **Stop** button in Coder |
| `ModuleNotFoundError: No module named 'psychopy'` | Script run from VS Code / system Python | Run from PsychoPy Coder (it has its own Python) |
| Blank screen instead of the word | TODO 3 not done, or `draw()` after `flip()` | `word.text = …`, `word.draw()` must come **before** `win.flip()` |
| Every answer "Wrong" | TODO 4 not done | `correct = int(response == trial["category"])` |
| `SyntaxError` in the stimulus list | Missing comma or quote | Each line: `{"word": "x", "category": "y"},` |
| `IndentationError` | Loop body not lined up | Everything inside the `for` loop is indented 4 spaces |
| `KeyError: 'rt_s'` or missing column | Typo in a dictionary key | Keys must match exactly, including quotes |
| Can't find the CSV | Looking in Downloads | It's in `data/` **next to the script** |
| Window on the wrong monitor / too big | Multi-monitor setup | Change `size=(1000, 700)`; add `screen=0` or `screen=1` to `visual.Window` |
| Text looks tiny or huge | Different units | Keep `units="height"`; text `height` is a fraction of screen height |

---

## 5. Why not run it online?

PsychoPy experiments *can* run in a browser via **Pavlovia** (PsychoPy's online platform), but only by
building in **Builder** and exporting to JavaScript (PsychoJS). A Python Coder script like this one
won't run online as-is. For learning to write the script, the lab computers (or a local install at home) are the simplest route.
