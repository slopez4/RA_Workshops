# Teaching Guide — How Modern AI Works

For whoever is running the session: prep, a minute-by-minute script, the interactive slides, and likely questions.
Speaker notes for every slide are in [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md). The slides also have a plain-language explanation under each slide in reference view (press `R`), which is what students use when studying on their own.

---

## 1. Before the session

### One week before
- [ ] Make sure GitHub Pages is on, so the [slides link](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html) works.
- [ ] Optional: download `slides.html` from the repo as a backup in case of Wi-Fi trouble (it opens in any browser; only the fonts fall back offline).
- [ ] Decide full or short version (see [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md)). For the short version, send the link a few days ahead and ask students to work through slides 4–9, 13 and 16 first.

### Day before
- [ ] Click through all 28 slides once with `SPEAKER_NOTES.md` open, including every TRY IT slide (4, 5, 7, 13, 16).
- [ ] If you'll do the live chatbot demos (section 4), try each one in the chatbot you'll use. Results vary between models and over time, so check what yours does now.

### 10 minutes before
- [ ] Open the slides and press `F` for fullscreen. Have a whiteboard or a blank slide ready for the guesses from slide 2.
- [ ] Optional: a chatbot open in a second browser tab, zoomed in so it's readable on the projector.

---

## 2. How to teach it

- **One idea per slide, build up.** Rules → Turing machine → history → neuron → network → training → tokens → embeddings → prediction → attention → assistant. Recap the chain out loud at the start of each part.
- **Predict, then click.** On every TRY IT slide, ask the room what will happen *before* you click (“What will the rules say for a cat?”). Predicting is what makes the idea stick.
- **Ask, don't tell.** Most slides have a natural question (in the notes). Give the room 10–15 seconds before answering.
- **No math required.** The only arithmetic is the neuron (0.6 + 0.9 + 0 = 1.5). If someone asks how the “squash” works, it's the sigmoid function; that's as deep as it needs to go.
- **Keyboard:** arrow keys move between slides. On the interactive slides, click the buttons with the mouse; typing in a text box won't change slides. `R` toggles reference view.
- **Two ideas matter more than any detail:** (1) a chatbot writes its answer *one token at a time by predicting what comes next*; (2) because of that, *fluent isn't the same as true*. Come back to both often.
- Some figures are illustrative: the token split and IDs (slide 17), the word map (18), the probabilities (19), the attention highlighting (20), the network drawing (14) and the five training examples (16). The slides say so; mention it if anyone asks.

---

## 3. Minute-by-minute script (full version, about 60 min)

### 0:00–0:04 · Hook and map (slides 1–3)
- “Workshop 1 was analysing data; Workshop 2 was building an experiment. Many of you already use chatbots to help with that code. Today we look inside, starting from the very beginning.”
- Slide 2: “What do you think happens in the middle box?” Write 3–4 guesses on the board (it searches the internet, it has a database of answers, it thinks like a person…). Don't correct them yet.
- Slide 3: four parts, each building on the last. Mention that every slide has a plain-language version in reference view (`R`) for studying later.

### 0:04–0:12 · If/then, a rule bot, a Turing machine (slides 4–7)
- **Slide 4 (animals).** Read the three rules. Ask before each click: Dog? Parrot? Then **Cat**: “No rule for cats.” Then **Bat**: “Wings make it a bird.” Then **Robot dog**: “No fur.” Point: every case needs a rule written by a person.
- Tie to Workshop 1: “You already wrote if/then when you marked a trial correct or wrong.”
- **Slide 5 (rule bot).** Click “Hello”, then “I am worried about my exam” (note it turns *my* into *your*), then the capital-of-France question. The list on the left lights up the rule that fired; the last one is the “I have no idea” default. Invite a student to type something to break it. “ELIZA did this in 1966, and people still felt understood.”
- **Slide 6 (Turing machine).** Three parts: tape, head, rules. “The rules are just if/thens again.” One machine plus the right rules can imitate any other machine: that is the idea of software.
- **Slide 7 (run it).** Press Step 3–4 times and ask which row will light up next. Then ask for a prediction for **111** (answer: 1000) and press Run. If time: 0 → 1, 1111 → 10000.

### 0:12–0:16 · History (slides 8–9)
- Point out the two threads using the tags: **Rules** (Turing, ELIZA, Deep Blue) and **Brain-inspired** (McCulloch–Pitts, perceptron, backpropagation, deep learning, transformer).
- “Learning won because of three things: a practical training method, lots of data, and fast chips (GPUs).” Mention AlphaGo (2016) aloud if students know it; it isn't on the slide.

### 0:16–0:22 · The big picture and the neuron (slides 10–12)
- Slide 10: point from the outside in. “Chess programs used to count as AI. Today, when people say AI they almost always mean the inner boxes.”
- Slide 11 is the key shift: **rules + data → answers** vs **data + answers → rules**. “Remember the dog detector: we wrote every rule and it broke on cats. Now the computer finds the rules.”
- Slide 12: walk the numbers left to right. 🤔 *Ask:* “Why is the weight on ‘has wings’ negative?” (Wings count *against* dog.)
- Brain-lab hook: inputs ≈ dendrites, weights ≈ synaptic strength, output ≈ firing. “It's a cartoon of a real neuron; we'll come back to how much of a cartoon.”

### 0:22–0:30 · Networks and training (slides 13–16)
- **Slide 13 (playground).** Let a student drive. Task: “Make the neuron call any barking animal a dog, furry or not.” Then make the wings weight positive and ask what the neuron now believes.
- **Slide 14.** “One neuron is one calculation. Wire many together in layers and you get a network. Every line is a weight: 20 here, billions in a chatbot.”
- **Slide 15.** Foggy hillside analogy. You can't see the valley, but you can feel the slope under your feet. The technical names are gradient descent and backpropagation; students don't need more than the names.
- **Slide 16 (train it).** Ask: “All weights start at zero. What will the neuron say?” (50% for everything.) Press **Train 1 round** twice and read the weights out loud: Barks goes up, Wings goes down. Press **Train 10**. “Nobody told it barking means dog.”

### 0:30–0:42 · Inside a language model (slides 17–20)
- Slide 17: “The model never sees letters, only numbers.” Fun consequence: models have historically struggled to count letters in a word.
- Slide 18: “Meaning becomes geometry.” King → queen is the same step as man → woman.
- Slide 19, **Be the model:** before the bars finish, read “The students opened their…” and have the room shout the next word. Then show the bars: “You just did what the model does, and you also produced a spread of answers, not one.” 🤔 *Ask:* what goes wrong if it always picks the single top word? (Repetitive, bland text; that's why there's a little randomness, called temperature.)
- Slide 20: read both sentences. “One word at the end changes what ‘it’ means. Attention is how the model tracks that.” The transformer is from 2017 (“Attention Is All You Need”).

### 0:42–0:48 · Becoming an assistant (slides 21–23)
- Slide 21: “The next-token game from slide 19, played over trillions of tokens. Facts and grammar emerge because they help predict the next word.”
- Slide 22: the “capital of France” example: a raw pretrained model might just continue with another quiz question.
- Slide 23: tools are how a chatbot can analyse a CSV like Workshop 1's: it writes and runs code rather than doing the arithmetic in its head.

### 0:48–0:53 · Limits (slides 24–25)
- Slide 24: tie each failure back to the mechanism (plausible ≠ true; it mirrors its data; the weights freeze when training ends).
- State the lab ground rules (also in the README): check citations and statistics against the original source, test AI-written code on mock data, **never paste participant data into a public chatbot**.
- Slide 25: pause. Let it land.

### 0:53–1:00 · Discussion and wrap-up (slides 26–28)
- Pairs for 2 minutes on one question, then 2–3 pairs share.
- **Q2 (checking AI-written code)** is the most practical. Good answers: run it on mock data, check a few output rows by hand, read every line you don't understand, compare with the Workshop 1–2 scripts.
- **Q3 (neuron analogy)**: real neurons spike, use many neurotransmitters, keep rewiring and learn from few examples; artificial ones are simple weighted sums trained offline on huge data.
- Close by revisiting the board: which guesses from slide 2 survived? (“It searches the internet” is only true when it's given a search tool; “it has a database of answers” is not how it works.)
- Point to slide 27 (four activities for the week) and slide 28 (key words), and to reference view (`R`).

---

## 4. Optional live chatbot demos

Try these the day before; what a model does changes between versions. If a demo “fails” (the model gets it right), that's a good discussion point too: newer models and tools fix some of these.

| Demo | Prompt idea | What it shows |
|---|---|---|
| Next-token feel | Ask for the same short story opening three times | Same prompt, different text: it samples from probabilities (slide 19) |
| Letters vs tokens | Ask how many times a letter appears in a long or unusual word | It sees tokens, not letters (slide 17) |
| Hallucinated citation | Ask for references on a very narrow topic, then search for one | Fluent isn't the same as true (slides 24–25) |
| Tool use | In a chatbot that can run code, ask it to compute a mean from a small table you paste in | It writes and runs code instead of doing arithmetic in its head (slide 23) |

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
| Is a neural network just lots of if/then statements? | Not quite. Rules are written by a person and are all-or-nothing; a neuron weighs evidence smoothly and its weights are learned from data. Both are simple operations repeated at scale. |
| Is a Turing machine used for anything today? | Mostly as a thought experiment that defines what “computable” means. Real computers are far faster and more convenient, but they can compute the same things. |
| Why did neural networks take until about 2012 to take off? | Three things came together: a practical training method (backpropagation), much more data, and much faster chips (GPUs). |
| Does ELIZA “understand”? | No. It matches keywords and fills in templates. It's a good example of how little it takes to feel understood. |
