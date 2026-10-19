# Class Outline — 10/19 · Workshop 3: How Modern AI Works

## Session overview

| | |
|---|---|
| **Topic** | How modern AI works: from a single artificial neuron to a chatbot, and where it goes wrong |
| **Audience** | Research assistants; no math or coding background needed. Workshops 1–2 are referenced but not required |
| **Format** | Short talk with questions to the room, one optional live demo, closing discussion |
| **Length** | 35 min core + 5 min buffer |
| **Setup** | Projector and the slides. Optional: a chatbot open in a browser tab for the demos |
| **Materials** | [Slides](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html) · [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md) · [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md) |

## Learning goals

By the end, RAs will be able to:

1. **Place** large language models inside AI → machine learning → deep learning.
2. **Contrast** writing rules by hand with learning them from labeled examples.
3. **Describe** what an artificial neuron computes and what training changes (the weights).
4. **Explain** how a chatbot writes a reply: tokens → embeddings → attention → predict the next token, repeat.
5. **Name** the three stages that turn a text predictor into an assistant (pretraining, fine-tuning, feedback).
6. **Identify** four failure modes (hallucination, bias, knowledge cutoff, no fact check) and apply the lab's ground rules for using AI.

## Agenda

| Time | Slides | What happens | Interaction |
|---|---|---|---|
| 0:00–0:04 | 1–2 | Welcome; link to Workshops 1–2; “what happens inside the middle box?” | Collect guesses, write them on the board |
| 0:04–0:09 | 3–4 | The nested family of AI; ML flips programming around (spam filter) | — |
| 0:09–0:15 | 5–6 | One neuron, worked example (“is it a dog?”); training as walking downhill | Ask: which input should get a negative weight? |
| 0:15–0:26 | 7–10 | Tokens, embeddings, next-token prediction, attention | **Be the model** game on slide 9 |
| 0:26–0:32 | 11–13 | Pretraining at scale; three stages to an assistant; images, audio, tools | Optional live demo |
| 0:32–0:36 | 14–15 | Four ways it goes wrong; “fluent isn’t the same as true” | — |
| 0:36–0:40 | 16 | Discussion (pick 1–2 questions); revisit the guesses from slide 2 | Pairs, then share |

## Where to cut if time runs short

- Merge slides 3 and 4: say the definitions aloud and go straight to “data + answers → rules”.
- Skip slide 13 (beyond text) and mention tools in one sentence on slide 12.
- Use just one discussion question (Q2, checking AI-written code, is the most lab-relevant).
- **Don't cut** slide 9 (next-token prediction) or slides 14–15 (limits and the takeaway). Those are the two ideas RAs should leave with.

## After the session

- Share the slides link with RAs.
- Optional homework: ask a chatbot for three references on a topic the lab works on, then check whether each one exists and says what the chatbot claimed. Bring the results to the next lab meeting.
