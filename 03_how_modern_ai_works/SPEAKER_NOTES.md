# Speaker Notes — How Modern AI Works

Notes for each of the 33 [slides](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html).
Timing and the script are in [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md).
Students see a shorter, plain-language version of each note under the slide in reference view (press `R`).

The deck is one story in chronological order. Each chapter has an idea, a demo and a problem; the problem is the hook for the next chapter, and a “bridge” strip at the bottom of the chapter's last slide says it.

---

## Intro

### 1 · How modern AI works

Welcome to Workshop 3. Workshop 1 was analysing data in Python; Workshop 2 was building an experiment in PsychoPy. Today is less hands-on: the tools many of you already use to help with that code. We follow the story from 1936 to today, one idea at a time, and you can study the rest on your own during the week (press R for the reference view).

### 2 · Today’s question

Ask the room: who has used a chatbot this week? What do you think is happening inside? Collect a few guesses (it searches the internet, it has a database of answers, it thinks like a person). Keep them on the board; we’ll come back to them at the end and see which survive.

### 3 · The plan

Thirteen chapters, in order. Each introduces one idea, lets you try it, and ends with a problem that the next chapter solves. The timeline along the bottom of the slides shows where you are; every item in the list is a button that jumps to that chapter.

---

## Chapter 1 · 1936 · Rules and machines

### 4 · Everything starts with if/then (try it)

An if/then statement is the simplest decision a computer makes. They did this in Python in Workshop 1 (marking a trial correct or wrong). Ask for a prediction before each preset. Dog and parrot work. Cat: no rule covers it. Bat: furry plus wings, so the rules call it a bird, which is wrong. Robot dog: no fur, so the dog rule never fires. The point: the rules only work for the cases the programmer thought of, and the world never runs out of exceptions. Keep this problem in mind; it is what the whole story is about.

### 5 · 1936: the Turing machine

In 1936 Alan Turing asked what it means to compute something. His imaginary machine has a tape (memory), a head that reads and writes one cell at a time and moves left or right, and a table of rules: if I’m in this state and read this symbol, then write this, move this way, and switch to that state. Those are if/thens again. The big discovery: one machine with the right rules can imitate any other machine, which is the idea of software. Everything a laptop or phone does, including running a chatbot, rests on this idea.

### 6 · Run a Turing machine yourself (try it)

This machine adds 1 to a binary number. It walks right to the end of the number, then walks back left turning 1s into 0s (the carry) until it finds a 0 or a blank to turn into a 1. Press Step and ask which row will light up next. Ask for a prediction for 111 (answer 1000), then press Run. Other starts to try: 0 gives 1, and 1111 gives 10000. Point out there is no understanding of numbers anywhere in the machine, only a table of rules, and it still does arithmetic. Bridge: a person had to write every rule. What if we copied the brain?

---

## Chapter 2 · 1943 · The artificial neuron

### 7 · 1943: the first artificial neuron

Warren McCulloch and Walter Pitts proposed that a brain cell could be modelled as a tiny calculator. Walk down the four rows: dendrites receive signals (inputs); synapses are stronger or weaker (weights); the cell body adds up what arrives; the cell fires if the total is high enough (squash). Their version was strictly on or off; modern neurons give a smooth score between 0 and 1 (the sigmoid). It is a cartoon of a real neuron, and we come back to that in the discussion.

### 8 · Play with a neuron (try it)

The neuron, but the students control it. Switch inputs on and off and drag the weights; the sum and the squashed score update live. The defaults are the worked example: inputs 1, 1, 0, weights 0.6, 0.9, −1.0, sum 1.5, score 82%, “probably a dog”. The bias is a built-in nudge that makes the neuron fire more or less easily before it looks at any input. Task: make any barking animal score above 80%, furry or not (the Barks weight has to dominate). Then make the Wings weight positive and ask what the neuron now believes. Bridge: someone still has to choose every weight by hand. But first, what are we trying to build?

---

## Chapter 3 · 1950–56 · A goal and a name

### 9 · 1950–56: a goal and a name

In 1950 Turing proposed the imitation game (now the Turing test): a judge chats by text with a hidden person and a hidden machine; if the judge can’t tell which is which, the machine passes. In 1956 a summer workshop at Dartmouth College coined the term “artificial intelligence”. Now there is a goal (a machine that can converse, reason and learn) and a promising part (the neuron), but the weights are still chosen by hand. Bridge: a neuron that chooses its own weights.

---

## Chapter 4 · 1958 · Learning from examples

### 10 · 1958: the perceptron learns from examples

Frank Rosenblatt’s perceptron is a neuron that sets its own weights. This is the single most important idea of the session. Traditional programming: rules plus data give answers. Machine learning flips it: data plus answers give the rules. Recall the animal checker, where a person had to write every rule and it broke on cats and robot dogs. The catch: the “rules” it ends up with are lists of numbers (weights), not sentences a person can read.

### 11 · Learning means nudging weights downhill

Analogy: you’re on a foggy hillside and want to reach the valley floor. You can’t see the bottom, but you can feel which way the ground slopes under your feet, so you take a small step downhill, and repeat. That’s gradient descent: guess, measure the error, nudge every weight a little in the direction that shrinks it, repeat.

### 12 · Watch a neuron learn (try it)

A one-neuron model learns “is it a dog?” from five labelled examples (the examples are made up). All weights start at zero, so it says 50% for everything. Each round shows it all five examples and nudges the weights. After two rounds it already gets all five right; after ten it is confident. Watch Barks grow and Wings turn negative. Ask: why does Barks keep growing while Furry turns negative? (Both dogs bark, but cats and bats are furry and are not dogs, so “furry” ends up counting slightly against “dog”. That is an artefact of five tiny examples, and a good reminder that a model learns whatever patterns its data contains.) Nobody told it that barking means dog.

---

## Chapter 5 · 1966 · Rules fake a conversation

### 13 · 1966: rules can fake a conversation (try it)

Meanwhile other researchers kept writing rules. ELIZA (Joseph Weizenbaum, MIT) played a therapist using keyword rules and templates; the mini version here has five rules and a default. Click “Hello”, then “I am worried about my exam” (note it flips my to your: “Why are you worried about your exam?”), then the France question, which matches nothing and gets “Please, go on.” The list on the left lights up the rule that fired. People felt understood by ELIZA even though it understood nothing. Bridge: rules never cover everything people say.

---

## Chapter 6 · 1969 · What one neuron can’t do

### 14 · 1969: one neuron can’t do everything

XOR means “exactly one of the two inputs is on”. Plot the four cases: the two filled corners (answer 1) and two hollow corners (answer 0) cannot be separated by a single straight line, and a single neuron can only draw one straight line. Marvin Minsky and Seymour Papert’s book Perceptrons (1969) pointed out limits like this. Interest and funding in neural networks faded for years: the “AI winters”.

### 15 · Stuck on XOR, then unstuck (try it)

With one neuron there are three dials (two weights and a bias). Let the room try to get four out of four; it can’t be done, and three is the best possible. Then switch on “Add a hidden layer”: the weights are preset so that one hidden neuron detects OR, another detects AND, and the output says “OR but not AND”. Two layers solve XOR. That is why networks have layers. Bridge: two layers work, but how do you train the hidden weights?

---

## Chapter 7 · 1986 · Training many layers

### 16 · 1986: backpropagation trains many layers

In 1958 a neuron could learn its weights. With two layers, a hidden neuron never sees the right answer directly, so how should its weights change? Backpropagation answers that: the network makes a guess going forward, then the error is passed backwards through the layers, telling each weight how much it contributed to the mistake, so each can be nudged downhill. The method existed in earlier forms; a 1986 paper by David Rumelhart, Geoffrey Hinton and Ronald Williams made it widely known.

### 17 · Train a tiny network on XOR (try it)

A real 2-3-1 network trained by backpropagation on the four XOR cases. It starts with small arbitrary weights and mostly guesses. Press Train 10, then Train 100: within about a hundred rounds the error falls and all four cases are right. Nobody wrote the rule “exactly one input”. With other starting weights, or on bigger problems, training can be slow and uneven. Bridge: it works, but only on tiny problems; real ones need far more data and speed.

---

## Chapters 8–9 · 1997 and 2012 · Data, chips, deep learning

### 18 · 1997: rules peak, learning waits

IBM’s Deep Blue beat world chess champion Garry Kasparov using expert-written rules and brute-force search, not learning. Meanwhile neural networks were waiting for three ingredients: methods (backpropagation, already there), data (the internet and large labelled datasets such as ImageNet, 2009), and chips (graphics processors, built for video games but ideal for the maths of networks).

### 19 · 2012: deep learning takes off

AlexNet, a deep network with 8 learned layers and about 60 million weights, trained on GPUs, won an image-recognition contest by a wide margin. “Deep” just means many layers. Roughly speaking, early layers pick up edges, middle layers shapes, late layers objects, and nobody programmed those stages (this is a simplification). Mention AlphaGo (2016) if students know it: it beat a top Go player after learning from human games and from playing itself. Bridge: these networks read images; how do you feed one a sentence?

---

## Chapter 10 · 2013–17 · Teaching networks language

### 20 · 2013–17: teaching networks language

Networks work on numbers, so text must be turned into numbers and back. The recipe worked out in these years is still the core of every chatbot, in the order the data flows: tokens, embeddings, attention, prediction. Each card jumps to its slide.

### 21 · Step 1: text becomes tokens (try it)

Text is chopped into tokens (whole words, parts of words or punctuation), each with an ID from a fixed list. Common words get their own token; rarer words are split into reusable pieces. Type a made-up word and see how it is split. The vocabulary here is a tiny toy (about 54 pieces); real models have tens or hundreds of thousands. Fun consequence: models can struggle with tasks like counting the letters in a word, because they never see individual letters.

### 22 · Step 2: tokens get coordinates (try it)

Each token ID is looked up in a giant table and turned into a long list of numbers, its embedding: coordinates on a map of meaning. During training, tokens that appear in similar contexts get pushed to similar places, so meaning becomes geometry. Click “king”: its nearest neighbours are man and queen. The classic finding from word2vec (2013): king minus man plus woman lands near queen. The 2D map is hand-made for illustration, not real model data.

### 23 · Step 3: attention reads the context (try it)

Before 2017, language models read text one word at a time and struggled to connect words far apart. The transformer (“Attention Is All You Need”) lets every token look at every other token and decide how relevant each one is. Toggle tired / wide: the word at the end changes which noun “it” attends to. Real models run many attention “heads” in parallel, across dozens of layers, so they track grammar, references, topic and tone at once. The numbers here are a hand-made illustration.

### 24 · Step 4: predict the next token (try it)

The core loop of every chatbot. The network takes all the tokens so far and outputs a probability for every token in its vocabulary. One is chosen, appended, and the whole thing runs again. Be the model: before clicking, have the room shout the next word, then click bars to build a sentence. The randomness slider is the temperature: at the minimum it nearly always takes the top word (repetitive), at the maximum it takes stranger words. The model here is a tiny made-up one that only looks at the last word; real models look at the whole text through attention. Note the sentences are fluent whether or not they are sensible. Bridge: this works on toy examples; what happens at enormous scale?

---

## Chapters 11–12 · 2020 and 2022 · Scale and assistants

### 25 · 2020: the same recipe, at enormous scale

The ladder: our dog neuron has 4 numbers (3 weights and a bias), the XOR network 13, AlexNet about 60 million, GPT-3 175 billion (each step right is 10 times more). Llama 3 was trained on 15 trillion tokens; training takes thousands of specialised chips for weeks or months. Pretraining is just the next-token game from slide 24 played on a huge slice of the internet, books and code. Nobody programs in “facts”: they emerge as a side effect of getting good at prediction. Bridge: a pretrained model only continues text.

### 26 · 2022: from text predictor to assistant (try it)

Click through the three tabs for the same question. A pretrained model asked “What is the capital of France?” might just continue with more quiz questions, because lists of quiz questions are common online. Fine-tuning on example dialogues teaches the question-and-answer format. The third stage is often called RLHF, reinforcement learning from human feedback: people compare pairs of answers, and the model is trained toward the kind they prefer. This is also where companies shape tone, safety behaviour and refusals. The replies are illustrative.

### 27 · Now it sees, hears and acts

Modern assistants are “multimodal”: one model handles text, images and audio by converting each into tokens. “Agents” go a step further: the model can output a special message like “search the web for X” or “run this Python code”. Software outside the model carries it out and pastes the result back in as more tokens. That’s how a chatbot can analyse a CSV like the one from Workshop 1: it writes and runs code, it doesn’t do the arithmetic in its head. Bridge: it is fluent and capable, but is it right?

---

## Chapter 13 · Today · Limits

### 28 · Four ways it goes wrong

All four follow from what we’ve seen. Hallucination: the model is always producing the most plausible continuation, and a made-up reference can look just as plausible as a real one (compare the generator on slide 24). Bias: it mirrors its training data. Cutoff: the weights are frozen when training ends. Lab-relevant example: never paste a citation, a statistic or a methods detail from a chatbot into anything without checking the original source. And remember privacy: don’t paste participant data into a public chatbot.

### 29 · Fluent isn’t the same as true

Pause here. Everything today comes down to this: these systems are extraordinarily good at producing text that sounds right, because that is exactly what they were trained to do. Sounding right and being right usually go together, which is why they’re so useful, but the model has no separate step that checks the truth. That’s your job.

---

## Wrap-up

### 30 · The whole story in one slide

Click through the timeline, one line per chapter, and ask what problem each solved. Rules (1936), the neuron (1943), the goal (1950), learning (1958), the limit of one neuron (1969), layers and backpropagation (1986), data and chips (1997–2012), language (2013–17), scale (2020), assistants (2022), and the one big weakness. Each item is a button that jumps back to that chapter.

### 31 · Let’s talk it through

Pick one or two depending on time. Q1: there’s no settled answer; push students to say what they mean by “understand”. Q2 links back to Workshops 1 and 2: run it on mock data, check the output CSV by hand for a few trials, read every line you don’t understand. Q3 is for a memory and brain lab: real neurons spike, use many neurotransmitters, rewire continuously and learn from few examples; artificial ones are simple weighted sums trained offline on enormous data. Finally, revisit the guesses from slide 2: which survived?

### 32 · Practice this week

Four short activities for the week; ask for at least two. Break the rule bot (slide 13), predict then run the Turing machine (slide 6), get unstuck on XOR (slides 15 and 17), and check a chatbot’s references. Invite students to bring surprising results to the next lab meeting.

### 33 · Key words

A glossary of fourteen terms for reference. Each is explained in the chapter where it first appears.
