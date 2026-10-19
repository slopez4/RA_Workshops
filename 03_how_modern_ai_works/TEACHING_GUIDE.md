# Teaching Guide — How Modern AI Works

For whoever is running the session: prep, a minute-by-minute script, live demos, and likely questions.
Speaker notes for every slide are in [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md).

---

## 1. Before the session

### One week before
- [ ] Make sure GitHub Pages is on, so the [slides link](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html) works.
- [ ] Optional: download `slides.html` from the repo as a backup in case of Wi-Fi trouble (it opens in any browser).

### Day before
- [ ] Click through all 16 slides once with `SPEAKER_NOTES.md` open.
- [ ] If you'll do the live demos (section 3), try each one in the chatbot you'll use. Results vary between models and over time, so check what yours does now.

### 10 minutes before
- [ ] Open the slides and press `F` for fullscreen. Have a whiteboard or a blank slide ready for the guesses from slide 2.
- [ ] Optional: a chatbot open in a second browser tab, zoomed in so it's readable on the projector.

---

## 2. How to teach it

- **One idea per slide, build up.** Each step adds one piece: neuron → training → tokens → embeddings → prediction → attention → assistant. Recap the chain out loud before moving to the next part.
- **Ask, don't tell.** Most slides have a natural question (in the notes). Give the room 10–15 seconds before answering.
- **No math required.** The only arithmetic is on slide 5 (0.6 + 0.9 + 0 = 1.5). If someone asks how the “squash” works, it's the sigmoid function; that's as deep as it needs to go.
- **Two ideas matter more than any detail:** (1) a chatbot writes its answer *one token at a time by predicting what comes next*; (2) because of that, *fluent isn't the same as true*. Come back to both often.
- Some figures are illustrative (the token split and IDs on slide 7, the probabilities on slide 9, the word map on slide 8, the attention highlighting on slide 10). The slides say so; mention it if anyone asks.

---

## 3. Minute-by-minute script

### 0:00–0:04 · Hook (slides 1–2)
- “Workshop 1 was analysing data; Workshop 2 was building an experiment. Many of you already use chatbots to help with that code. Today we look inside.”
- Slide 2: “What do you think happens in the middle box?” Write 3–4 guesses on the board (it searches the internet, it has a database of answers, it thinks like a person…). Don't correct them yet.

### 0:04–0:09 · The big picture (slides 3–4)
- Slide 3: point from the outside in. “Chess programs used to count as AI. Today, when people say AI they almost always mean the inner boxes.”
- Slide 4 is the key shift: **rules + data → answers** vs **data + answers → rules**. Spam filter example. “The catch: the rules it learns are millions of numbers, not sentences you can read.”

### 0:09–0:15 · The machinery (slides 5–6)
- Slide 5: walk the numbers left to right. 🤔 *Ask:* “Why is the weight on ‘has wings’ negative?” (Wings count *against* dog.)
- Brain-lab hook: inputs ≈ dendrites, weights ≈ synaptic strength, output ≈ firing. “It's a cartoon of a real neuron; we'll come back to how much of a cartoon.”
- Slide 6: foggy hillside analogy. You can't see the valley, but you can feel the slope under your feet. The technical names are gradient descent and backpropagation; RAs don't need more than the names.

### 0:15–0:26 · Inside a language model (slides 7–10)
- Slide 7: “The model never sees letters, only numbers.” Fun consequence: models have historically struggled to count letters in a word.
- Slide 8: “Meaning becomes geometry.” King → queen is the same step as man → woman.
- Slide 9, **Be the model:** before revealing the bars, read “The students opened their…” and have the room shout the next word. Then show the bars: “You just did what the model does, and you also produced a spread of answers, not one.” 🤔 *Ask:* what goes wrong if it always picks the single top word? (Repetitive, bland text; that's why there's a little randomness, called temperature.)
- Slide 10: read both sentences. “One word at the end changes what ‘it’ means. Attention is how the model tracks that.” The transformer is from 2017 (“Attention Is All You Need”).

### 0:26–0:32 · Becoming an assistant (slides 11–13)
- Slide 11: “The next-token game from slide 9, played over trillions of tokens. Facts and grammar emerge because they help predict the next word.”
- Slide 12: the “capital of France” example from the notes: a raw pretrained model might just continue with another quiz question.
- Slide 13: tools are how a chatbot can analyse a CSV like Workshop 1's: it writes and runs code rather than doing the arithmetic in its head.

### 0:32–0:36 · Limits (slides 14–15)
- Slide 14: tie each failure back to the mechanism (plausible ≠ true; it mirrors its data; the weights freeze when training ends).
- State the lab ground rules (also in the README): check citations and statistics against the original source, test AI-written code on mock data, **never paste participant data into a public chatbot**.
- Slide 15: pause. Let it land.

### 0:36–0:40 · Discussion (slide 16)
- Pairs for 2 minutes on one question, then 2–3 pairs share.
- **Q2 (checking AI-written code)** is the most practical. Good answers: run it on mock data, check a few output rows by hand, read every line you don't understand, compare with the Workshop 1–2 scripts.
- **Q3 (neuron analogy)**: real neurons spike, use many neurotransmitters, keep rewiring and learn from few examples; artificial ones are simple weighted sums trained offline on huge data.
- Close by revisiting the board: which guesses from slide 2 survived? (“It searches the internet” is only true when it's given a search tool; “it has a database of answers” is not how it works.)

---

## 4. Optional live demos

Try these the day before; what a model does changes between versions. If a demo “fails” (the model gets it right), that's a good discussion point too: newer models and tools fix some of these.

| Demo | Prompt idea | What it shows |
|---|---|---|
| Next-token feel | Ask for the same short story opening three times | Same prompt, different text: it samples from probabilities (slide 9) |
| Letters vs tokens | Ask how many times a letter appears in a long or unusual word | It sees tokens, not letters (slide 7) |
| Hallucinated citation | Ask for references on a very narrow topic, then search for one | Fluent isn't the same as true (slides 14–15) |
| Tool use | In a chatbot that can run code, ask it to compute a mean from a small table you paste in | It writes and runs code instead of doing arithmetic in its head (slide 13) |

Use only made-up data in demos, never real participant data.

---

## 5. Likely questions

| Question | Short answer |
|---|---|
| Does it search the internet? | Only if it's connected to a search tool. Otherwise everything comes from patterns stored in its weights during training. |
| Does it remember our conversation? | Within one conversation, yes: the earlier text is fed back in as tokens every time. Across conversations, only if the app has a separate memory feature. |
| Does it learn from what I type? | Not as you chat; the weights are fixed. Some companies may use conversations to train future models, depending on settings and policies. |
| Is it conscious or does it understand? | Open question, no consensus. Good for discussion Q1. What we can say: it was trained to predict text, and it does that extraordinarily well. |
| How is this like the brain? | Loosely inspired by neurons and learning by adjusting connection strengths, but very different in mechanism, energy use and how much data it needs (discussion Q3). |
| Why does it sound so confident when it's wrong? | Confident-sounding text is what most of its training text looks like. Nothing in next-token prediction measures truth. |
