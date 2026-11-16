# Workshop 4 — Build the SFV × VWM Experiment

**Length:** a few sessions (each Part is one sitting) · **PsychoPy is already installed on the lab computers**

**📊 Slides / reference guide:** open [`slides.html`](slides.html) in a browser (double-click it, or once pushed to GitHub: `https://slopez4.github.io/RA_Workshops/04_svf_vwm_experiment/slides.html`). Press `R` to switch between slide view and a scrollable reference page.

You'll build, from a blank file, the experiment the lab is testing:

1. a **change-detection memory task** (colored squares: did one change?),
2. **reward videos** before each set of trials (a no-video control, 5 / 45 / 120 s clips, and 1 × 45 s vs 3 × 15 s clips),
3. **ratings** after each video (wanting, liking), and
4. **memory tests for the videos** at the end (free recall, pick the pictures, one-by-one recognition).

Everything gets saved to three CSV files per participant: trials, rewards, memory.

## Files

| File | What it is |
|---|---|
| `slides.html` | The workshop. 5 Parts with a checkpoint at the end of each, plus a cheat sheet, common problems and glossary. |
| `svf_vwm_mini.py` | The **finished** script. The slides build this file up piece by piece, and the code on the slides is the same code. Use it to check your own work. |
| `make_stills.py` | Run once before sessions with memory tests. Saves two screenshots from every video (needs [ffmpeg](https://ffmpeg.org/)). |

## Before you start

- **Videos are not in this repo** (too large). Put them in `videos/<genre>/<folder>/clip_000.mp4`, e.g. `videos/nature/duration_5s/clip_001.mp4`. The folders are `duration_5s`, `duration_45s`, `duration_120s`, `dose_45s_single`, `dose_15s_fragment`. Ask the lab for the video library.
- **No videos yet?** Everything still runs. Each video becomes a "[a 45 s reward video would play here]" screen. The memory tests for the videos are skipped.
- Run the scripts from PsychoPy Coder (**View → Coder**, open the file, press the green Run button), which uses PsychoPy's own Python.
- `DEV_MODE = True` (the default) runs a short test version: 4 trials per condition, videos cut at 6 s. **Set it to `False` for real participants.**

## Python you already know

The slides assume only the basics from w3schools: variables, lists, dictionaries, `for`/`while`, `if`, functions, and f-strings. Part 0 has a map of which concept appears where; the one new idea (objects, like `win.flip()`) is explained before it's needed.

## Provisional parts

The study is still being tested. Anything the lab hasn't decided is a **setting** at the top of `svf_vwm_mini.py` and tagged `PROVISIONAL` (search for that word), and has a yellow **Provisional** box on its slide. Currently:

- set size (4), timings (250 ms encoding, 1000 ms retention)
- video genre (`GENRE`) and whether 3 × 15 s means 3 different clips or one clip three times
- which ratings to ask, and how often
- whether to show feedback in the real trials (we only show it in practice)
- reward **before** the trials (as here) or trials before the reward
- the memory tests: how many pictures, order, and whether to add a test on video titles

## Updating the deck when the script changes

1. Edit `svf_vwm_mini.py` and run a test session.
2. Search `slides.html` for the changed lines and update them. Each code block on a slide is an excerpt of the script, so copy and paste (remember `<` is `&lt;`, `>` is `&gt;`, `&` is `&amp;` inside the HTML).
3. Code blocks that are *only* illustrative carry `data-nocheck`. Everything else should match the script line for line (ignoring comments).
4. Example CSV rows on the checkpoint slides come from a simulated test run. Regenerate them if the columns change.
5. Open the slides and click through the affected Part.

Data you generate lands in `data/` (ignored by Git), as do `videos/` and `stills/`.
