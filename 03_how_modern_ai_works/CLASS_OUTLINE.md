# Class Outline — 10/19 · Workshop 3: How Modern AI Works

## Session overview

| | |
|---|---|
| **Topic** | How modern AI works: from if/then rules and Turing machines, through artificial neurons and networks, to a chatbot, and where it goes wrong |
| **Topic** | How modern AI works, told as one story in order: if/then rules and Turing machines (1936), the artificial neuron (1943), learning from examples (1958), layers and backpropagation (1969–86), deep learning (2012), language models and the transformer (2013–17), scale and assistants (2020–22), and where they go wrong |
| **Audience** | Undergraduate research assistants; no math or coding background needed. Workshops 1–2 are referenced but not required |
| **Format** | Short talk with questions to the room, five interactive “Try it” slides, closing discussion. The deck is also a self-study guide for the rest of the week |
| **Length** | Full version ≈ 60 min. Short version ≈ 40 min + 5 min buffer, with Part 1 and the neuron try-its assigned as pre-work (see below) |
| **Format** | Short talk following the timeline, twelve interactive “Try it” slides, closing discussion. The deck is also a self-study guide for the rest of the week |
| **Length** | Full version ≈ 80 min (e.g. a double session). Core version ≈ 45 min, with the other chapters assigned as reading. Self-study ≈ 90 min over the week |
| **Setup** | Projector and the slides. Optional: a chatbot open in a browser tab for the demos |
| **Materials** | [Slides](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html) · [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md) · [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) |

## The idea that makes it easy to follow

Every chapter has the same shape: **an idea → a demo → a problem**, and the problem is what the next chapter fixes. A bridge strip at the bottom of each chapter's last slide says it out loud (“The problem … Next ▶ …”), and the timeline along the bottom of the slides shows where you are. If RAs get lost, ask them: *what problem did the last chapter leave?*

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
1. **Explain** what an if/then rule is, why hand-written rules can't cover the real world, and what a Turing machine is.
2. **Place** the main milestones of AI from 1936 to 2022 and say what problem each solved.
3. **Describe** what an artificial neuron computes, what a network is, and why networks need layers (the XOR story).
4. **Contrast** writing rules by hand with learning them from examples, and explain training as nudging weights downhill.
5. **Explain** how a chatbot writes a reply: tokens → embeddings → attention → predict the next token, repeat.
6. **Name** the three stages that turn a text predictor into an assistant (pretraining, fine-tuning, feedback).
7. **Identify** four failure modes (hallucination, bias, knowledge cutoff, no fact check) and apply the lab's ground rules for using AI.

## Agenda: full version (≈ 80 min)

| Time | Chapter | Slides | What happens | Try it |
|---|---|---|---|---|
| 0:00–0:04 | Intro | 1–3 | Welcome; guesses on the board; the plan and the timeline | — |
| 0:04–0:12 | 1 · 1936 | 4–6 | If/then; the Turing machine | Animals; step the machine |
| 0:12–0:18 | 2 · 1943 | 7–8 | Copy the brain: the artificial neuron | Neuron playground |
| 0:18–0:20 | 3 · 1950 | 9 | The goal (Turing test) and the name (AI) | — |
| 0:20–0:28 | 4 · 1958 | 10–12 | Learning from examples; downhill training | Watch a neuron learn |
| 0:28–0:32 | 5 · 1966 | 13 | ELIZA: rules fake a conversation | Break the rule bot |
| 0:32–0:37 | 6 · 1969 | 14–15 | One neuron can't do XOR; a hidden layer can | Stuck, then unstuck |
| 0:37–0:42 | 7 · 1986 | 16–17 | Backpropagation | Train a network on XOR |
| 0:42–0:47 | 8–9 · 1997, 2012 | 18–19 | Rules peak; data, chips and deep learning | — |
| 0:47–0:59 | 10 · 2013–17 | 20–24 | Language in four steps: tokens, embeddings, attention, prediction | Four mini demos (**be the model** on 24) |
| 0:59–1:02 | 11 · 2020 | 25 | Scale: from 4 weights to 175 billion | — |
| 1:02–1:08 | 12 · 2022 | 26–27 | Pretraining → fine-tuning → feedback; seeing, hearing, acting | Compare the three stages |
| 1:08–1:13 | 13 · Today | 28–29 | Four ways it goes wrong; “fluent isn't the same as true” | — |
| 1:13–1:20 | Wrap-up | 30–33 | Recap (click through the timeline), discussion, point to practice and key words | Pairs, then share |

## Agenda: core version (≈ 45 min)

Assign **slides 5, 7, 9, 11, 13, 14, 18–20, 25, 27, 30, 32 and 33** as reading, plus a few minutes with the TRY IT slides, and run the following live.

| Time | Slides | What happens |
|---|---|---|
| 0:00–0:03 | 1–3 | Hook and map; ask what they remember from the pre-work (if/then, Turing machine, the two threads) |
| 0:03–0:08 | 10–12 | The nested family; ML flips programming; the neuron |
| 0:08–0:12 | 14–15 | Network and training (they already played with both) |
| 0:12–0:22 | 17–20 | Tokens, embeddings, prediction (**be the model**), attention |
| 0:22–0:27 | 21–23 | Scale, three stages, beyond text |
| 0:27–0:32 | 24–25 | Limits and the takeaway |
| 0:32–0:40 | 26 | Discussion; revisit the board |
| 0:00–0:03 | 1–3 | Hook, guesses on the board, the plan |
| 0:03–0:07 | 4, 6 | If/then (animals); step the Turing machine |
| 0:07–0:10 | 8 | Neuron playground |
| 0:10–0:16 | 10, 12 | Learning from examples; watch a neuron learn |
| 0:16–0:19 | 15 | XOR: stuck, then unstuck |
| 0:19–0:23 | 16–17 | Backpropagation and the XOR network |
| 0:23–0:35 | 21–24 | Tokens, embeddings, attention, next-token prediction (**be the model**) |
| 0:35–0:38 | 26 | Three stages of training |
| 0:38–0:42 | 28–29 | Limits and the takeaway |
| 0:42–0:45 | 31 | Discussion (one question), revisit the board |

## Where to cut if time runs short

- Skip slide 5 (rule bot) and slide 9 (second half of the history): say the main point in one sentence each.
- Merge slides 10 and 11: say the definitions aloud and go straight to “data + answers → rules”.
- Skip slide 23 (beyond text) and mention tools in one sentence on slide 22.
- Cut slides 5, 9, 18 and 19 first: say each in one sentence.
- Skip slide 13 (ELIZA) if you've shown slide 4 (it makes the same point about rules).
- Skip slide 27 (beyond text) and mention tools in one sentence on slide 26.
- Use just one discussion question (Q2, checking AI-written code, is the most lab-relevant).
- **Don't cut** slide 19 (next-token prediction) or slides 24–25 (limits and the takeaway). Those are the two ideas RAs should leave with.
- **Don't cut** slide 24 (next-token prediction), slide 15 (XOR, the reason for layers) or slides 28–29 (limits and the takeaway). Those are the ideas RAs should leave with.

## After the session

- Share the slides link with RAs. In reference view (`R`) every slide has a plain-language explanation, so it works as a study guide and handout.
- During the week, RAs do at least two of the four activities on slide 27.
- Share the slides link with RAs. In reference view (`R`) every slide has a plain-language explanation, so it works as a study guide and handout. The Recap slide (30) links back to every chapter.
- During the week, RAs do at least two of the four activities on slide 32.
- Optional homework: ask a chatbot for three references on a topic the lab works on, then check whether each one exists and says what the chatbot claimed. Bring the results to the next lab meeting.
