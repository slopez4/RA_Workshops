# Workshop 3 — How Modern AI Works

**Session:** 10/19 · **Length:** 40–60 min live, plus self-study during the week · **Nothing to install**

**📊 Slides / study guide:** [open the slides](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html). Press `R` to switch between slide view and **reference view**: every slide on one scrolling page with a plain-language explanation under it. Press `F` for fullscreen. Slides tagged **TRY IT** are interactive.

A talk-and-discussion session, no coding this time. We open up the tools many of you already
use to help with the Python from [Workshop 1](../01_intro_python_analysis/) and the PsychoPy
script from [Workshop 2](../02_psychopy_experiment/): **what actually happens between typing a
question into a chatbot and getting an answer back?**

No background is assumed. We start from the basics (if/then rules, Turing machines, a short
history), build up to the artificial neuron and how networks learn, and then follow a chatbot
step by step. The deck doubles as a self-study guide: you can work through it on your own
during the week.

---

## The path through the deck

| Part | Slides | What you'll learn |
|---|---|---|
| 1 · Foundations | 1–9 | If/then rules and why hand-written rules break; a rule-based chatbot (ELIZA); what a Turing machine is; a short history from 1936 to 2022 |
| 2 · Neural networks | 10–16 | AI ⊃ machine learning ⊃ deep learning ⊃ LLMs; learning rules from examples; the artificial neuron; networks of neurons; training as walking downhill on the error |
| 3 · Inside a chatbot | 17–23 | Tokens → embeddings (“meaning space”) → next-token prediction → attention; pretraining at scale; fine-tuning and feedback; images, audio and tools |
| 4 · Using it well | 24–28 | Hallucination, bias, knowledge cutoff, no fact check; “fluent isn’t the same as true”; discussion; practice for the week; key words |

### The interactive (TRY IT) slides

| Slide | What you can do |
|---|---|
| 4 · If/then | Try five animals against a few hand-written rules, and see where the rules fail |
| 5 · Rule-based chatbot | Talk to a tiny ELIZA-style bot and try to break it |
| 7 · Turing machine | Step through a machine that adds 1 to a binary number, rule by rule |
| 13 · Neuron playground | Switch inputs on and off and move the weights; watch the sum and the score |
| 16 · Watch a neuron learn | Train a one-neuron model on five examples and watch the weights change |

## What's in this folder

| File | What it is |
|---|---|
| [`slides.html`](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html) | 28 slides + reference view with plain-language notes + interactive demos (opens in any browser) |
| [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md) | What to say on each slide |
| [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md) | Session plan: goals, timing, agenda (full and short versions) |
| [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) | How to run the session, demos, discussion prompts, likely questions |

## What you'll be able to do afterward

- Explain what an **if/then rule** is, and why rules alone can't cover the real world
- Describe a **Turing machine** (tape, head, rules) and why it matters for every computer
- Place the main milestones from **1936 to 2022** and tell the “rules” thread from the “learning” thread
- Explain the difference between **traditional programming** and **machine learning**
- Describe what an **artificial neuron** computes, what a **network** is, and what **training** changes (the weights)
- Walk through how a chatbot writes a reply: **tokens → embeddings → attention → next-token prediction**, one token at a time
- Say what **pretraining**, **fine-tuning** and **feedback from people** each add
- Name four ways these models fail, and why each follows from how they're built

## Using AI in the lab: ground rules

- **Check everything.** Treat an AI answer as a draft, not a source. Verify citations, statistics and methods details against the original.
- **Test AI-written code** the way we did in Workshops 1–2: run it on mock data and check a few rows of the output by hand.
- **Never paste participant data** (or anything identifiable) into a public chatbot.

## Keep practicing

The **Practice this week** slide (27) has four short activities: break the rule bot, predict the
Turing machine, train the neuron and explain why the weights move, and check a chatbot's
references. The **Key words** slide (28) is a glossary.
