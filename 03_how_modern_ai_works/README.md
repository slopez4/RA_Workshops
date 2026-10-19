# Workshop 3 — How Modern AI Works

**Session:** 10/19 · **Length:** 35–40 min · **Nothing to install**

**📊 Slides:** [open the deck](https://claude.ai/artifact/RNDm7HXKjdeMNRFmJKjj49) — speaker notes are on every slide.

A talk-and-discussion session, no coding this time. We open up the tools many of you already
use to help with the Python from [Workshop 1](../01_intro_python_analysis/) and the PsychoPy
script from [Workshop 2](../02_psychopy_experiment/): **what actually happens between typing a
question into a chatbot and getting an answer back?** We build it up one idea at a time, from a
single artificial neuron to a full chatbot, then talk about where it goes wrong and how to use
it responsibly in the lab.

---

## The path through the session

| Part | Slides | Idea |
|---|---|---|
| The big picture | 1–4 | AI ⊃ machine learning ⊃ deep learning ⊃ LLMs; learning rules from examples instead of writing them |
| The machinery | 5–6 | An artificial neuron is a weighted sum + squash; training nudges the weights downhill on the error |
| Inside a language model | 7–10 | Tokens → embeddings (“meaning space”) → next-token prediction → attention |
| Becoming an assistant | 11–13 | Pretraining at scale, fine-tuning and feedback, then images, audio and tools |
| Limits & discussion | 14–16 | Hallucination, bias, knowledge cutoff, no fact check; “fluent isn’t the same as true” |

## What's in this folder

| File | What it is |
|---|---|
| [Slides](https://claude.ai/artifact/RNDm7HXKjdeMNRFmJKjj49) | 16 slides with speaker notes (downloadable as PDF or PowerPoint from the deck) |
| [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md) | Session plan: goals, timing, agenda |
| [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) | How to run the session, live demos, discussion prompts, likely questions |

## What you'll be able to do afterward

- Explain the difference between **traditional programming** and **machine learning**
- Describe what an **artificial neuron** computes and what **training** changes
- Walk through how a chatbot writes a reply: **tokens → embeddings → attention → next-token prediction**, one token at a time
- Say what **pretraining**, **fine-tuning** and **feedback from people** each add
- Name four ways these models fail, and why each follows from how they're built

## Using AI in the lab: ground rules

- **Check everything.** Treat an AI answer as a draft, not a source. Verify citations, statistics and methods details against the original.
- **Test AI-written code** the way we did in Workshops 1–2: run it on mock data and check a few rows of the output by hand.
- **Never paste participant data** (or anything identifiable) into a public chatbot.
