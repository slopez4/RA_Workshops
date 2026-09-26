# Class Outline — 09/28

## Session overview

| | |
|---|---|
| **Topic** | Introduction to simple analysis code scripts · Christian's Reward + SFV presentation · Discussion: Motivational Shifts |
| **Audience** | Research assistants; no coding experience assumed |
| **Format** | Live code-along in Google Colab (browser only, nothing to install) |
| **Coding portion** | 35 min core + 5 min buffer |
| **Materials** | [Slides](https://slopez4.github.io/RA_Workshops/01_intro_python_analysis/slides.html) · [Student notebook](https://colab.research.google.com/github/slopez4/RA_Workshops/blob/main/01_intro_python_analysis/notebooks/workshop_student.ipynb) · [`analysis.py`](analysis.py) · [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) |

> We will go over what a Python script looks like and try to code one. Then
> Christian will present the Reward + SFV project, and we'll discuss ideas for
> other projects related to it.

## Learning goals

By the end of the coding portion, RAs will be able to:

1. **Read** a short analysis script and say what each section does (load → check → clean → analyze → plot).
2. **Use** four core ideas: variables, lists, `for` loops, `if` statements.
3. **Inspect** a data file: rows, columns, missing values, ranges, distributions.
4. **Justify** exclusions (too-fast/too-slow trials, a participant at chance) as rules set *before* seeing results.
5. **Summarize** per participant first, then across participants, and explain why.
6. **Connect** a data pattern to a scientific question — here, whether reward's effect on motivation shifts over time.

## Agenda

| Time | Part | What happens | Coding ideas | Data-thinking idea |
|---|---|---|---|---|
| 0:00–0:03 | **Setup** | Open Colab link, *Save a copy in Drive*, run first cell | Cells, Shift+Enter | — |
| 0:03–0:10 | **0. Python in 5 minutes** | Variables, lists, a loop that flags weird RTs | variables, `print`, lists, indexing from 0, `for`, `if/elif/else`, indentation | "Can a human respond in 101 ms?" |
| 0:10–0:15 | **1. Bring the data in** | Load the CSV from a URL, read the codebook | `import`, `pd.read_csv`, `.head()`, `.shape` | What is one row? Do the counts add up? |
| 0:15–0:22 | **2. Look before you analyze** | Summary stats, missing values, RT histogram, accuracy per person | `.describe()`, `.isna()`, `.hist()`, `groupby` | Impossible values; spotting a participant who guessed |
| 0:22–0:27 | **3. Clean the data** | Count bad trials, apply exclusion rules | True/False conditions, `&`, `~`, filtering | Rules, not names; decide *before* results; what happens to missing data |
| 0:27–0:33 | **4. Does reward change behavior?** | Condition means, per-person effects, spaghetti plot | `unstack`, new columns, plotting in a loop | Trial vs. participant averages; individual differences |
| 0:33–0:37 | **5. Does the effect change over time?** | Reward effect by half; motivation ratings | dictionaries, `.map`, `drop_duplicates` | Reward advantage halves; no-reward motivation drops → **motivational shifts** |
| 0:37–0:40 | **Wrap-up / buffer** | Show `analysis.py` as the "finished script"; 5 habits | Scripts run top-to-bottom | — |
| 0:40 → | **Christian: Reward + SFV** | Presentation | | |
| after | **Discussion: Motivational Shifts** | Use the Part 5 results as a starting point | | |

## Bridge into the discussion

Part 5 ends with three prompts that lead directly into the discussion after Christian's talk:

1. The reward advantage in reaction time roughly **halves** from the first to the second half of the session. What could explain that?
2. Motivation drops much more in **no-reward** blocks than in reward blocks. Does that change the explanation?
3. What would you add to a study design to tell these explanations apart?

## Where to cut if time runs short

- Skip the `elif` TODO in Part 0 (do it live yourself).
- In Part 2, skip the histogram and go straight to accuracy per participant.
- In Part 4, show the spaghetti plot but skip the `n_faster` TODO.
- Never cut Part 5 — it's the bridge to the discussion. Run it yourself if needed.

## After the session

- RAs keep their Colab copy in Google Drive.
- Solutions: [`notebooks/workshop_solutions.ipynb`](notebooks/workshop_solutions.ipynb).
- Optional homework: the ⭐ stretch exercise (repeat Part 5 for accuracy).
