# Class Outline — 10/19 · Workshop 3: How Modern AI Works

## Session overview

| | |
|---|---|
| **Topic** | How modern AI works: from if/then rules and Turing machines, through artificial neurons and networks, to a chatbot, and where it goes wrong |
| **Audience** | Undergraduate research assistants; no math or coding background needed. Workshops 1–2 are referenced but not required |
| **Format** | Short talk with questions to the room, five interactive “Try it” slides, closing discussion. The deck is also a self-study guide for the rest of the week |
| **Length** | Full version ≈ 60 min. Short version ≈ 40 min + 5 min buffer, with Part 1 and the neuron try-its assigned as pre-work (see below) |
| **Setup** | Projector and the slides. Optional: a chatbot open in a browser tab for the demos |
| **Materials** | [Slides](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html) · [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md) · [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) |

## Learning goals

By the end, RAs will be able to:

1. **Explain** what an if/then rule is, and why hand-written rules can't cover the real world.
2. **Describe** a Turing machine (tape, head, rules) and place the main milestones of AI from 1936 to 2022.
3. **Place** large language models inside AI → machine learning → deep learning.
4. **Contrast** writing rules by hand with learning them from labeled examples.
5. **Describe** what an artificial neuron computes, what a network is, and what training changes (the weights).
6. **Explain** how a chatbot writes a reply: tokens → embeddings → attention → predict the next token, repeat.
7. **Name** the three stages that turn a text predictor into an assistant (pretraining, fine-tuning, feedback).
8. **Identify** four failure modes (hallucination, bias, knowledge cutoff, no fact check) and apply the lab's ground rules for using AI.

## Agenda: full version (≈ 60 min)

| Time | Slides | What happens | Interaction |
|---|---|---|---|
| 0:00–0:04 | 1–3 | Welcome; link to Workshops 1–2; “what happens inside the middle box?”; the map of the four parts | Collect guesses, write them on the board |
| 0:04–0:12 | 4–7 | If/then rules; a rule-based chatbot; the Turing machine | **Try it** ×3: animals, break the bot, step the machine |
| 0:12–0:16 | 8–9 | Short history: two threads (rules vs. brain-inspired learning) | — |
| 0:16–0:22 | 10–12 | AI ⊃ ML ⊃ deep learning ⊃ LLMs; ML flips programming; the neuron | Ask: which input should get a negative weight? |
| 0:22–0:30 | 13–16 | Play with a neuron; from one neuron to a network; training as walking downhill | **Try it** ×2: neuron playground, watch a neuron learn |
| 0:30–0:42 | 17–20 | Tokens, embeddings, next-token prediction, attention | **Be the model** game on slide 19 |
| 0:42–0:48 | 21–23 | Pretraining at scale; three stages to an assistant; images, audio, tools | Optional live demo |
| 0:48–0:53 | 24–25 | Four ways it goes wrong; “fluent isn't the same as true” | — |
| 0:53–1:00 | 26–28 | Discussion (pick 1–2 questions); revisit the guesses from slide 2; point to practice (27) and key words (28) | Pairs, then share |

## Agenda: short version (≈ 40 min)

Assign **slides 4–9** (Part 1) and the **try-its on slides 13 and 16** as pre-work (about 20 minutes on their own), and start the live session from the big picture.

| Time | Slides | What happens |
|---|---|---|
| 0:00–0:03 | 1–3 | Hook and map; ask what they remember from the pre-work (if/then, Turing machine, the two threads) |
| 0:03–0:08 | 10–12 | The nested family; ML flips programming; the neuron |
| 0:08–0:12 | 14–15 | Network and training (they already played with both) |
| 0:12–0:22 | 17–20 | Tokens, embeddings, prediction (**be the model**), attention |
| 0:22–0:27 | 21–23 | Scale, three stages, beyond text |
| 0:27–0:32 | 24–25 | Limits and the takeaway |
| 0:32–0:40 | 26 | Discussion; revisit the board |

## Where to cut if time runs short

- Skip slide 5 (rule bot) and slide 9 (second half of the history): say the main point in one sentence each.
- Merge slides 10 and 11: say the definitions aloud and go straight to “data + answers → rules”.
- Skip slide 23 (beyond text) and mention tools in one sentence on slide 22.
- Use just one discussion question (Q2, checking AI-written code, is the most lab-relevant).
- **Don't cut** slide 19 (next-token prediction) or slides 24–25 (limits and the takeaway). Those are the two ideas RAs should leave with.

## After the session

- Share the slides link with RAs. In reference view (`R`) every slide has a plain-language explanation, so it works as a study guide and handout.
- During the week, RAs do at least two of the four activities on slide 27.
- Optional homework: ask a chatbot for three references on a topic the lab works on, then check whether each one exists and says what the chatbot claimed. Bring the results to the next lab meeting.
