# Class Outline — 10/05 · Workshop 2: Your First PsychoPy Experiment

## Session overview

| | |
|---|---|
| **Topic** | Writing a simple PsychoPy experiment script: "We use a simple demo to present 8 randomized trials of animals and plants" |
| **Audience** | Research assistants; Workshop 1 helpful but not required |
| **Format** | Live code-along in PsychoPy Coder on the lab computers |
| **Length** | 35 min core + 5 min buffer |
| **Setup** | PsychoPy 2026.1 pre-installed on the lab computers by the instructor. Install steps for RAs' own computers are on slide 17 and in the [README](README.md), for later |
| **Materials** | [Slides](https://slopez4.github.io/RA_Workshops/02_psychopy_experiment/slides.html) · [`animals_plants_starter.py`](animals_plants_starter.py) · [`animals_plants.py`](animals_plants.py) · [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) |

## Learning goals

By the end, RAs will be able to:

1. **Describe** an experiment as a script that shows things, waits for responses, and writes a file, and say how Builder relates to Coder.
2. **Read** the seven sections of the script (settings → dialog → setup → instructions → trial loop → save → goodbye).
3. **Explain** draw → flip and why reaction times are timed from the flip.
4. **Randomize** trial order and say why it matters.
5. **Collect** a keypress with a timeout, score it against the stimulus's correct answer, and save it.
6. **Open** the output CSV and connect it to the Workshop 1 analysis.

## Agenda

| Time | Slides | What happens | Hands-on |
|---|---|---|---|
| 0:00–0:03 | 1–3 | Everyone has PsychoPy open, starter loaded, 2 trials run | Run the starter |
| 0:03–0:07 | 4–5 | Builder vs Coder; anatomy of a trial (fixation → word → feedback, × 8, random) | — |
| 0:07–0:14 | 6–10 | Walk through the script: settings, dialog, window, **draw → flip**, `show_message` function | — |
| 0:14–0:19 | 7, 11 | Stimuli list and randomization | **TODO 1** (add 6 stimuli), **TODO 2** (shuffle) → run |
| 0:19–0:27 | 12–13 | One trial: show the word, start the clock on the flip, collect and score the key | **TODO 3** (draw word), **TODO 4** (score) → run |
| 0:27–0:32 | 14–15 | Save one row per trial; open the CSV; compare orders with a neighbour | **TODO 5** (save RT) → run, open CSV |
| 0:32–0:37 | 16, 20 | "Make it yours" extensions; wrap-up | Pick one extension |
| 0:37–0:40 | 17–19 | Buffer / questions; point to install-at-home steps, cheat sheet & common problems | — |

## Where to cut if time runs short

- Skip slide 10 (functions); just say "`show_message` shows text and waits for space."
- Do TODO 1 yourself (paste the 6 stimuli) and let RAs copy.
- Skip the extensions; assign them as homework.
- **Don't cut** draw → flip (slide 9) or running + opening the CSV (slide 15). Those are the two takeaways.

## After the session

- RAs save their completed `animals_plants_starter.py` (email it to themselves or copy it to a USB stick; lab computers may be shared).
- To keep practicing at home, they install PsychoPy using slide 17 / the README.
- Reference: the slides' reference view (`R`), especially the cheat sheet and common problems.
- Optional homework: one "Make it yours" extension, then rebuild the same experiment in **Builder**.
