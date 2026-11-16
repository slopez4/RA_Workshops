# Teaching guide — Workshop 4: Nostalgia, Memory and the Senses

How to run the session, the discussion stops and the pitch block; what to prepare; what to be careful about.

## 1. Preparation checklist

- [ ] Open [`slides.html`](slides.html) and [`workbook.html`](workbook.html) in a browser (any modern browser; nothing to install). Press `F` for fullscreen.
- [ ] Press **R** once to look at the reference view; every slide has a plain-language note and sources.
- [ ] Skim [`LITERATURE_REVIEW.md`](LITERATURE_REVIEW.md), sections 0 and 1, so you can say what is verified and what is not.
- [ ] Decide whether RAs will have done the workbook before the session (best: at least Modules 1 and 6 done) or after.
- [ ] If you run the live tally on a shared screen, each RA adds a dot from their own device only if the slide is open on their device; otherwise add dots yourself as they call them out.

## 2. How the deck is organised

| Part | Slides | Palette | What it is for |
|---|---|---|---|
| Intro | 1–3 | Pastel stripes | Welcome, live tally, map |
| 1 · What nostalgia is | 4–7 | 1970s (mustard, olive, rust, teal) | Definition, anatomy, regulatory model, reality check |
| 2 · The memory lens | 8–11 | 1980s playground (red, yellow, blue, green) | Cue → memory, reminiscence bump, feeling vs accuracy |
| 3 · The senses | 12–19 | 1990s pastel + the five-sense icons | Smell, music, food, temperature, vision; brain; aging |
| 4 · Methods and your ideas | 20–25 | "Now": indigo with pastel accents | Methods, evidence map, seeds, pitches, homework |

Each slide uses one palette only. The ruler at the top right shows the era; in Part 3 the sense bar lights up the senses on that slide.

## 3. The interactive slides

| Slide | What to do |
|---|---|
| 2 · Your cue | Everyone picks a cue and the age in their memory; the chart stacks dots by decade of age, colored by cue. Revisit on slides 9 and 14. Add demo data if the room is small (it is labelled as made up). Data are kept in the browser only. |
| 21 · Evidence map | Click cells to list studies. Dense cells: smell and music × emotion/content. Empty cells are prompts for a literature search, not proof of a gap. |
| 22 · Seeds | Click a card for hook, design, measures, pitfalls and starter reading. |

## 4. The three discussion stops

**Discuss A (slide 7): lab vs daily life.** Aim for 2–3 points: control condition, demand characteristics, generalisation from "recall on request" to everyday nostalgia. Don't resolve it: the point is to notice that the headline effect size depends on the paradigm.

**Discuss B (slide 10): richer vs rosier.** Steer toward measurement: blind-coded episodic details (Autobiographical Interview), word-count control, external records. If they propose "ask people if it's accurate", ask what a confident-but-wrong memory would look like.

**Discuss C (slide 17): a fair comparison across senses.** Ask them to name the three things they would hold constant (familiarity, relevance, labels/order are the usual answers) and the one thing they would give up.

## 5. Running the pitch block (10–15 min)

1. Each RA gets **60 seconds**: question; cue and control; measure; gap and risk.
2. Group gives **one strength and one concern** (30 s total).
3. Keep a visible timer; interrupt kindly.
4. Capture each pitch in a shared doc (title, question, one concern).
5. Optional: vote for one or two to take forward as a pilot.

**Common issues to watch for:** the control is missing; "nostalgia" is measured only with a single self-report rating; a conclusion about all ages from a student sample; comparing senses with different cues per sense; a claim about accuracy from richness of detail; no power thinking (see Module 5).

## 6. Things to be honest about

- The literature search was non-systematic and done in October 2026. "No study found" means "not found in these searches".
- Findings were written from abstracts. Where only a summary was seen, the text says so (for example, the 2026 meta-analysis numbers and the EEG study's design).
- The practice items in Module 2 are my own wording, not a validated scale.
- A few claims from secondary sources were left out because I could not verify them (see section 0 of the literature review).
- The strips on slide 9 are a visual summary of ranges from different studies, not data from one experiment.

## 7. Technical notes

- The deck and workbook are static HTML plus [`evidence_data.js`](evidence_data.js); they need the `.js` file next to them. Opened from a local folder they work; hosted on GitHub Pages they work too.
- Workbook progress and diary entries are stored in the browser's local storage (this browser, this device). Clearing site data deletes them. Use the export buttons to keep copies.
- Fonts load from Google Fonts; offline, the pages fall back to system fonts.
- On a phone, the deck opens in reference view automatically.

## 8. If you want to extend

- Add studies to `STUDIES` in `evidence_data.js` (tag each with a sense and outcomes) and the evidence map updates in both the slides and the workbook.
- Add a seed to `SEEDS` and it appears in the slides and in the workbook's study builder.
- Add questions to `QUIZ` or vignettes to `VIGNETTES`.
