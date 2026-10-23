# Teaching Guide — How Modern AI Works

For whoever is running the session: prep, a script chapter by chapter, prompts for each interactive slide, and likely questions.
Speaker notes for every slide are in [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md). The slides also have a plain-language explanation under each slide in reference view (press `R`), which is what students use when studying on their own.

---

## 1. Before the session

### One week before
- [ ] Make sure GitHub Pages is on, so the [slides link](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html) works.
- [ ] Optional: download `slides.html` from the repo as a backup in case of Wi-Fi trouble (it opens in any browser; only the fonts fall back offline).
- [ ] Decide full (≈ 80 min) or core (≈ 45 min) version (see [`CLASS_OUTLINE.md`](CLASS_OUTLINE.md)). For the core version, send the link a few days ahead and ask students to read the skipped chapters in reference view.

### Day before
- [ ] Click through all 33 slides once with `SPEAKER_NOTES.md` open, and try each TRY IT slide (4, 6, 8, 12, 13, 15, 17, 21, 22, 23, 24, 26).
- [ ] If you'll do the live chatbot demos (section 4), try each one in the chatbot you'll use. Results vary between models and over time, so check what yours does now.

### 10 minutes before
- [ ] Open the slides and press `F` for fullscreen. Have a whiteboard or a blank slide ready for the guesses from slide 2.
- [ ] Optional: a chatbot open in a second browser tab, zoomed in so it's readable on the projector.

---

## 2. How to teach it

- **Follow the timeline.** The deck is one story: each chapter adds an idea, has a demo, and ends with a problem that the next chapter solves. The bar along the bottom shows where you are, and the bridge strip at the end of each chapter says “The problem … Next …”. Read it out loud, and ask the room to guess the fix before you click.
- **Predict, then click.** On every TRY IT slide, ask the room what will happen *before* you click (“What will the rules say for a cat?”). Predicting is what makes the idea stick.
- **Ask, don't tell.** Most slides have a natural question (in the notes). Give the room 10–15 seconds before answering.
- **No math required.** The only arithmetic is the neuron (0.6 + 0.9 + 0 = 1.5). If someone asks how the “squash” works, it's the sigmoid function; that's as deep as it needs to go.
- **Keyboard:** arrow keys move between slides. On the interactive slides, click the buttons with the mouse; typing in a text box won't change slides. `R` toggles reference view, and the timeline buttons jump to a chapter.
- **Two ideas matter more than any detail:** (1) a chatbot writes its answer *one token at a time by predicting what comes next*; (2) because of that, *fluent isn't the same as true*. Come back to both often.
- Some figures are illustrative: the word map (slide 22), the attention numbers (23), the next-word probabilities and the tiny generator (24), the three-stage replies (26), the network drawings and the five training examples (12, 16). The slides say so; mention it if anyone asks.

---

## 3. Script (full version, about 80 min)

### 0:00–0:04 · Intro (slides 1–3)
- “Workshop 1 was analysing data; Workshop 2 was building an experiment. Many of you already use chatbots to help with that code. Today we follow the story of how they were built, from 1936.”
- Slide 2: “What do you think happens in the middle box?” Write 3–4 guesses on the board (it searches the internet, it has a database of answers, it thinks like a person…). Don't correct them yet.
- Slide 3: thirteen chapters, each fixing the last one's problem. Show the timeline along the bottom, and mention reference view (`R`) for studying later.

### 0:04–0:12 · Chapter 1 · 1936: rules and machines (slides 4–6)
- **Slide 4 (animals).** Read the three rules. Ask before each click: Dog? Parrot? Then **Cat**: “No rule for cats.” Then **Bat**: “Wings make it a bird.” Then **Robot dog**: “No fur.” Point: every case needs a rule written by a person. Tie to Workshop 1: “You already wrote if/then when you marked a trial correct or wrong.”
- **Slide 5 (Turing machine).** Three parts: tape, head, rules. “The rules are just if/thens again.” One machine plus the right rules can imitate any other machine: that is the idea of software.
- **Slide 6 (run it).** Press Step 3–4 times and ask which row will light up next. Then ask for a prediction for **111** (answer: 1000) and press Run. If time: 0 → 1, 1111 → 10000.
- Bridge: “A person has to write every rule, in advance. What if we copied the brain?”

### 0:12–0:20 · Chapters 2–3 · 1943 and 1950: the neuron, the goal (slides 7–9)
- **Slide 7.** Walk down the four rows: dendrites ≈ inputs, synapses ≈ weights, cell body ≈ add up, firing ≈ squash. “It's a cartoon of a real neuron; we'll come back to how much of a cartoon.”
- **Slide 8 (playground).** Let a student drive. Task: “Make the neuron call any barking animal a dog, furry or not.” Then make the wings weight positive and ask what the neuron now believes. Bridge: “But *we* are choosing the weights.”
- **Slide 9.** The imitation game and the Dartmouth workshop: now there is a goal (conversation) and a part (the neuron), but the weights are still set by hand.

### 0:20–0:28 · Chapter 4 · 1958: learning from examples (slides 10–12)
- **Slide 10.** Rules + data → answers, versus data + answers → rules. “Remember the animal checker? Now the machine finds the rules.” The perceptron: a neuron that sets its own weights.
- **Slide 11.** Foggy hillside: you can't see the valley, but you can feel the slope under your feet, so you step downhill and repeat. The technical name is gradient descent.
- **Slide 12 (train it).** Ask: “All weights start at zero. What will the neuron say?” (50% for everything.) Press **Train 1 round** twice and read the weights out loud: Barks goes up, Wings goes down. Press **Train 10**. “Nobody told it barking means dog.”

### 0:28–0:32 · Chapter 5 · 1966: ELIZA (slide 13)
- Click “Hello”, then “I am worried about my exam” (note it turns *my* into *your*), then the capital-of-France question. The list on the left lights up the rule that fired; the last one is the “I have no idea” default. Invite a student to break it. “ELIZA did this in 1966, and people still felt understood.” Bridge: “Rules never cover everything people say.”

### 0:32–0:42 · Chapters 6–7 · 1969 and 1986: layers and backpropagation (slides 14–17)
- **Slide 14.** XOR means “exactly one”. Look at the four corners: no single straight line separates the filled from the hollow ones. Minsky and Papert pointed this out in 1969, and interest faded (the AI winters).
- **Slide 15 (XOR).** Let the room try to get 4/4 with the three dials: it can't be done (3/4 is the best). Then click **Add a hidden layer**: “one neuron spots OR, one spots AND, the output says OR-but-not-AND. Two layers solve it.” Bridge: “but how do you train the hidden weights?”
- **Slide 16.** Backpropagation: guess forwards, share the blame backwards, nudge each weight downhill (1986).
- **Slide 17 (train it).** Press **Train 10** a couple of times, then **Train 100**. Ask when all four cases go right (about 100 rounds). “Nobody wrote the rule *exactly one*.”

### 0:42–0:47 · Chapters 8–9 · 1997 and 2012: data, chips and deep learning (slides 18–19)
- Slide 18: Deep Blue won with rules and brute force. Learning was waiting for **data, chips and methods**.
- Slide 19: in 2012 they arrived together (AlexNet). “Deep” = many layers: early layers pick up edges, later ones shapes, then objects. Mention AlphaGo (2016) aloud if students know it.
- Bridge: “These read images. How do we feed one a sentence?”

### 0:47–0:59 · Chapter 10 · 2013–17: teaching networks language (slides 20–24)
- Slide 20: four steps in the order the data flows. Click a card to jump to it.
- **Slide 21 (tokens).** Type a made-up word and see how it splits. “The model never sees letters, only numbers.” Fun consequence: models have historically struggled to count letters in a word.
- **Slide 22 (embeddings).** Click “king”: nearest are man and queen. “Meaning becomes geometry”: king → queen is the same step as man → woman.
- **Slide 23 (attention).** Toggle tired / wide and watch “it” change which word it attends to. The transformer is from 2017 (“Attention Is All You Need”).
- **Slide 24 (next token), be the model.** Before clicking, read “The students opened their…” and have the room shout the next word. Click bars to build a sentence. Then set the randomness slider to the minimum and press Pick for me repeatedly: it repeats itself. Maximum: stranger choices. “Fluent, but nothing here checks truth.”

### 0:59–1:08 · Chapters 11–12 · 2020 and 2022: scale and assistants (slides 25–27)
- Slide 25: the ladder from 4 weights to 175 billion. “The next-token game, played over trillions of tokens. Facts and grammar emerge because they help predict the next word.”
- **Slide 26 (stages).** Click through the three tabs for the same question: a raw model may continue with more quiz questions; fine-tuning teaches it to answer; feedback makes it more helpful and honest.
- Slide 27: tools are how a chatbot can analyse a CSV like Workshop 1's: it writes and runs code rather than doing the arithmetic in its head.

### 1:08–1:13 · Chapter 13 · today: limits (slides 28–29)
- Slide 28: tie each failure back to the mechanism (plausible ≠ true; it mirrors its data; the weights freeze when training ends). Link back to the generator on slide 24.
- State the lab ground rules (also in the README): check citations and statistics against the original source, test AI-written code on mock data, **never paste participant data into a public chatbot**.
- Slide 29: pause. Let it land.

### 1:13–1:20 · Recap and discussion (slides 30–33)
- Slide 30: click through the timeline, one line per chapter, and ask what problem each one solved.
- Slide 31: pairs for 2 minutes on one question, then 2–3 pairs share. **Q2 (checking AI-written code)** is the most practical: run it on mock data, check a few output rows by hand, read every line you don't understand, compare with the Workshop 1–2 scripts. **Q3 (neuron analogy)**: real neurons spike, use many neurotransmitters, keep rewiring and learn from few examples; artificial ones are simple weighted sums trained offline on huge data.
- Close by revisiting the board: which guesses from slide 2 survived? (“It searches the internet” is only true when it's given a search tool; “it has a database of answers” is not how it works.)
- Point to slide 32 (four activities for the week), slide 33 (key words), and reference view (`R`).

---

## 4. Optional live chatbot demos

Try these the day before; what a model does changes between versions. If a demo “fails” (the model gets it right), that's a good discussion point too: newer models and tools fix some of these.

| Demo | Prompt idea | What it shows |
|---|---|---|
| Next-token feel | Ask for the same short story opening three times | Same prompt, different text: it samples from probabilities (slide 24) |
| Letters vs tokens | Ask how many times a letter appears in a long or unusual word | It sees tokens, not letters (slide 21) |
| Hallucinated citation | Ask for references on a very narrow topic, then search for one | Fluent isn't the same as true (slides 28–29) |
| Tool use | In a chatbot that can run code, ask it to compute a mean from a small table you paste in | It writes and runs code instead of doing arithmetic in its head (slide 27) |

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
| Why did neural networks take until about 2012 to take off? | Three things came together: a practical training method (backpropagation, 1986), much more data, and much faster chips (GPUs). |
| Does ELIZA “understand”? | No. It matches keywords and fills in templates. It's a good example of how little it takes to feel understood. |
| Why does the XOR network sometimes need many rounds? | Training is a downhill walk; with these starting weights it takes about a hundred rounds, but with other starting points or bigger problems it can be slow and uneven. |
