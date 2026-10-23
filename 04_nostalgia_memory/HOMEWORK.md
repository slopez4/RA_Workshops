# Homework for Workshop 4

Open the interactive **[workbook](workbook.html)** (or [on GitHub Pages](https://slopez4.github.io/RA_Workshops/04_nostalgia_memory/workbook.html)). Everything saves in your own browser; use **Export my work** to keep a copy. This page is the same plan as a checklist. Budget **3–4 hours**, spread across lab hours.

| ✓ | Module | Time | What you do | What you bring |
|---|---|---|---|---|
| ☐ | 1 · Read like a scientist | 60–90 min | Pick 3 papers from the menu (at least one smell or music paper and one on design or ecological validity). Fill the extraction form in your own words. | One thing that surprised you |
| ☐ | 2a · Event reflection task on yourself | 15 min | Do the nostalgic and ordinary rounds (separate occasions, ≥ 1 h apart). | A sentence on what the control condition does |
| ☐ | 2b · Seven-day cue diary | 5 min per entry | Log 5–10 nostalgic episodes: sense, unprompted or sought, age in the memory, ratings. | The CSV (download from the workbook) |
| ☐ | 3 · Spot the confound | 15 min | Eight design vignettes with feedback. | Your score and the one you got wrong |
| ☐ | 4 · Evidence map and search | 30–45 min | Pick an empty or sparse cell, search, fill the search log. | Your search log and verdict |
| ☐ | 5 · Power sandbox | 20 min | Size a study at g ≈ 0.39; then an interaction. | The N you would aim for |
| ☐ | 6 · Build your study | 45–60 min | Start from a seed (or your own), fill the brief, export it. | **The one-page brief** (the main deliverable) |
| ☐ | 7 · Quiz | 10 min | Retrieval practice on the key findings. | — |
| ☐ | 8 · Resources | 5 min | Import `references.bib` into Zotero. | — |

## If you want to analyse your cue diary in Python (Workshop 1 skills)

I could not run Python on the machine used to prepare this workshop, so **treat this as a starter and test it in Colab**:

```python
import pandas as pd

d = pd.read_csv("cue_diary.csv")
d = d[d["demo"].astype(str).str.lower() == "false"]       # drop demo entries

print(d.groupby("sense")["age"].agg(["count", "median"]))  # age in memory by sense
print(d["access"].value_counts(normalize=True))            # unprompted vs sought
d["bittersweet"] = d[["pos", "neg"]].min(axis=1)           # high on both = mixed emotion
print(d.groupby("sense")[["nost", "viv", "pos", "neg", "bittersweet"]].mean().round(2))
```

Questions to ask of your own data: do smell entries come from earlier ages than music entries? Are unprompted entries more vivid? Is the most nostalgic entry also the most bittersweet? With 5–10 entries you cannot conclude anything: the exercise is to see what a real dataset would need.

## Rules of thumb

- **Open the paper** before you quote a number from the slides or the review (summaries were written from abstracts).
- The practice questionnaires in Module 2 are **not validated instruments**.
- Your diary and writing may contain personal memories. Don't share exports unless you want to.
