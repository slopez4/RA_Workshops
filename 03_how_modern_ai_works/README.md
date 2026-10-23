# Workshop 3 — How Modern AI Works

**Session:** 10/19 · **Length:** 45–80 min live, plus self-study during the week · **Nothing to install**

**📊 Slides / study guide:** [open the slides](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html). The deck tells **one story in order, from 1936 to today**: a timeline along the bottom shows where you are. Press `R` to switch between slide view and **reference view**: every slide on one scrolling page with a plain-language explanation under it. Press `F` for fullscreen. Slides tagged **TRY IT** are interactive.

A talk-and-discussion session, no coding this time. We open up the tools many of you already
use to help with the Python from [Workshop 1](../01_intro_python_analysis/) and the PsychoPy
script from [Workshop 2](../02_psychopy_experiment/): **what actually happens between typing a
question into a chatbot and getting an answer back?**

No background is assumed. We follow the history in order. **Each chapter adds one idea, lets you
try it, and ends with a problem that the next chapter solves.** By the end, you will have built up
from if/then rules to a chatbot, step by step. The deck doubles as a self-study guide for the week.

---

## The story, chapter by chapter

| # | Year | Idea | Try it | Slides |
|---|---|---|---|---|
| 1 | 1936 | **If/then rules** and the **Turing machine** | Test hand-written rules; step a Turing machine | 4–6 |
| 2 | 1943 | The **artificial neuron**: weigh, add up, squash | Play with a neuron | 7–8 |
| 3 | 1950 | The goal (the Turing test) and the name (“AI”, 1956) | — | 9 |
| 4 | 1958 | The **perceptron**: learning weights from examples; training as walking downhill | Watch a neuron learn | 10–12 |
| 5 | 1966 | **ELIZA**: rules can fake a conversation | Talk to a rule-based bot | 13 |
| 6 | 1969 | One neuron can't do **XOR**; the AI winters | Stuck on XOR, then add a hidden layer | 14–15 |
| 7 | 1986 | **Backpropagation** trains many layers | Train a tiny network on XOR | 16–17 |
| 8 | 1997 | Rules peak (Deep Blue); learning waits for data and chips | — | 18 |
| 9 | 2012 | **Deep learning** takes off (AlexNet) | — | 19 |
| 10 | 2013–17 | Teaching networks language: **tokens → embeddings → attention → prediction** | Tokenizer, meaning map, attention, next-word generator | 20–24 |
| 11 | 2020 | The same recipe at enormous **scale** | — | 25 |
| 12 | 2022 | From text predictor to **assistant** (fine-tuning, feedback); seeing, hearing, acting | Compare the three training stages | 26–27 |
| 13 | Today | **Limits**: hallucination, bias, cutoff, no fact check | — | 28–29 |
| — | Recap | The whole story in one slide; discussion; practice; key words | — | 30–33 |

## What's in this folder

| File | What it is |
|---|---|
| [`slides.html`](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html) | 33 slides + reference view with plain-language notes + 12 interactive demos (opens in any browser) |
| [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md) | What to say on each slide |
| [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md) | Session plan: goals, timing, agenda (full and core versions) |
| [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) | How to run the session, prompts for each demo, likely questions |

## What you'll be able to do afterward

- Explain what an **if/then rule** is, why rules alone can't cover the real world, and what a **Turing machine** is
- Tell the story of AI from **1936 to 2022**, and say what problem each step solved
- Describe what an **artificial neuron** computes, what a **network** is, and why networks need **layers**
- Explain what **training** does (nudging weights downhill, with **backpropagation** through the layers)
- Walk through how a chatbot writes a reply: **tokens → embeddings → attention → next-token prediction**, one token at a time
- Say what **pretraining**, **fine-tuning** and **feedback from people** each add
- Name four ways these models fail, and why each follows from how they're built

## Using AI in the lab: ground rules

- **Check everything.** Treat an AI answer as a draft, not a source. Verify citations, statistics and methods details against the original.
- **Test AI-written code** the way we did in Workshops 1–2: run it on mock data and check a few rows of the output by hand.
- **Never paste participant data** (or anything identifiable) into a public chatbot.

## Keep practicing

The **Practice this week** slide (32) has four short activities: break the rule bot, predict the
Turing machine, get unstuck on XOR, and check a chatbot's references. The **Key words** slide (33)
is a glossary, and the **Recap** slide (30) links back to every chapter.
