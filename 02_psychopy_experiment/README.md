# Workshop 2 — Your First PsychoPy Experiment

**Session:** 10/05 · **Length:** 30–40 min · **PsychoPy is already installed on the lab computers**

**📊 Slides / reference guide:** [open the slides](https://slopez4.github.io/RA_Workshops/02_psychopy_experiment/slides.html) — keep it open while you work (press `R` to switch between slide view and a scrollable reference page).

We'll write a short PsychoPy experiment from a starter script: **8 trials of animal and
plant words in random order.** Participants press **A** for an animal or **P** for a plant,
and the script records their answer, accuracy, and reaction time to a CSV file. That's
the same kind of file you analysed in [Workshop 1](../01_intro_python_analysis/).

---

## For later: install PsychoPy on your own computer (~10 min)

You don't need this for the session; the lab computers are set up. To practice at home, install
PsychoPy yourself. It runs on your computer, not in a browser, because it controls screen and keyboard timing directly.

1. Download the **Standalone** installer from [psychopy.org/download](https://www.psychopy.org/download.html).
   Use the same version as the lab computers (**2026.1**).
2. **Windows:** run the `.exe`, accept the defaults.
   **Mac:** open the `.dmg` and drag PsychoPy into *Applications*. If macOS blocks it:
   *System Settings → Privacy & Security → Open Anyway*.
3. Open PsychoPy → **View → Coder**.
4. **Mac only:** *System Settings → Privacy & Security* → allow PsychoPy under
   **Input Monitoring** and **Accessibility**, or it won't detect keypresses.

## Get the files and test

In class, do this on the lab computer. At home, do it after installing.

1. On [the repo page](https://github.com/slopez4/RA_Workshops), click **Code → Download ZIP** and unzip it.
2. Open PsychoPy → **View → Coder**, then **File → Open** → `02_psychopy_experiment/animals_plants_starter.py`.
3. Click the green **Run** button. Enter any ID, click OK, and press A or P on the 2 trials.

If a window appears and responds to your keys, you're ready.

---

## What's in this folder

| File | What it is |
|---|---|
| [`animals_plants_starter.py`](animals_plants_starter.py) | The script we complete together. It has 5 TODOs and runs at every step |
| [`animals_plants.py`](animals_plants.py) | The finished experiment, to compare with yours |
| [`slides.html`](https://slopez4.github.io/RA_Workshops/02_psychopy_experiment/slides.html) | Slides for class + reference page (install steps, cheat sheet, common problems) |
| [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md) | Session plan: goals, timing, agenda |
| [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) | How to run the session, TODO answers, troubleshooting |

Data files are written to a `data/` folder next to the script, one CSV per run:

| participant | session | trial | word | category | response | correct | rt_s |
|---|---|---|---|---|---|---|---|
| RA01 | 1 | 1 | eagle | animal | animal | 1 | 0.593 |
| RA01 | 1 | 2 | tulip | plant | plant | 1 | 0.469 |
| RA01 | 1 | 3 | salmon | animal | | 0 | |

## What you'll be able to do afterward

- Explain the difference between PsychoPy **Builder** and **Coder**
- Set up a window, text stimuli, and a keyboard
- Use **draw → flip** to control exactly when things appear
- Randomize trial order and loop through trials
- Collect a keypress with a timeout, score it, and time it from stimulus onset
- Save one row per trial to a CSV

## Keep practicing

Try the "Make it yours" slide: different keys, repeated trials, a break screen, or
pictures instead of words (`visual.ImageStim`). Then open PsychoPy **Builder** and
you'll recognise the same pieces as routines, loops and a conditions file.
