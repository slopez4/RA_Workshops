# Speaker Notes — How Modern AI Works

Notes for each of the 28 [slides](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html).
Timing and the minute-by-minute script are in [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md).
Students see a shorter, plain-language version of each note under the slide in reference view (press `R`).

---

## Part 1 · Foundations

### 1 · How modern AI works

Welcome to Workshop 3. Workshop 1 was analysing data in Python; Workshop 2 was building an experiment in PsychoPy. Today is less hands-on: the tools many of you already use to help with that code. Today’s goal: by the end, everyone should be able to explain, in plain words, what happens when you type a question into a chatbot. No background needed; we start from the very beginning, and you can study the rest on your own during the week (press R for the reference view).

### 2 · Today’s question

Ask the room: who has used a chatbot this week? What do you think is happening inside? Collect a few guesses (it searches the internet, it has a database of answers, it thinks like a person). Keep them on the board; we’ll come back to them at the end and see which survive.

### 3 · Your map for the week

Four parts, each building on the last. Part 1 is the older ideas (rules, the first computers, a short history). Part 2 is the building block of modern AI, the artificial neuron. Part 3 is how those neurons read and write text. Part 4 is using it wisely. Mention the TRY IT tag: those slides are interactive, and the reference view has a plain-language explanation under every slide.

### 4 · If/then: the simplest machine that decides (try it)

An if/then statement is the simplest decision a computer makes. They did this in Python in Workshop 1 (marking a trial correct or wrong). Ask for a prediction before each preset. Dog and parrot work. Cat: no rule covers it. Bat: furry plus wings, so the rules call it a bird, which is wrong. Robot dog: no fur, so the dog rule never fires. The point: the rules only work for the cases the programmer thought of, and the world never runs out of exceptions. Set up the next slide: could we write enough rules to hold a conversation?

### 5 · Rules can fake a conversation, for a while (try it)

ELIZA (Joseph Weizenbaum, MIT, 1966) played a therapist using keyword rules and templates; the mini version here has five rules and a default. Click “Hello”, then “I am worried about my exam” (note it flips my to your: “Why are you worried about your exam?”), then the France question, which matches nothing and gets “Please, go on.” The list on the left lights up the rule that fired. People felt understood by ELIZA even though it understood nothing. Hand-written rules cannot cover everything people might say; modern chatbots work differently, and the rest of the session shows how.

### 6 · A Turing machine: a tape, a head, and rules

In 1936 Alan Turing asked what it means to compute something. His imaginary machine has a tape (memory), a head that reads and writes one cell at a time and moves left or right, and a table of rules: if I’m in this state and read this symbol, then write this, move this way, and switch to that state. Those are if/thens again. The big discovery: one machine with the right rules can imitate any other machine, which is the idea of software. Everything a laptop or phone does, including running a chatbot, rests on this idea.

### 7 · Run a Turing machine yourself (try it)

This machine adds 1 to a binary number. It walks right to the end of the number, then walks back left turning 1s into 0s (the carry) until it finds a 0 or a blank to turn into a 1. Press Step and ask which row will light up next. Ask for a prediction for 111 (answer 1000), then press Run. Other starts to try: 0 gives 1, and 1111 gives 10000. Point out there is no understanding of numbers anywhere in the machine, only a table of rules, and it still does arithmetic.

### 8 · A short history, part 1: the ideas (1936–1966)

Two threads, labelled on each card. Rules: Turing’s machine (1936), ELIZA (1966). Brain-inspired: McCulloch and Pitts’ artificial neuron (1943), Rosenblatt’s perceptron (1958), a neuron that learns its weights from examples. Idea cards: the imitation game (Turing, 1950, now called the Turing test) and the 1956 Dartmouth summer workshop where the term “artificial intelligence” was coined. The field is only about 70 years old.

### 9 · A short history, part 2: scale (1969–today)

In 1969 Minsky and Papert pointed out what a single neuron cannot do, and interest in neural networks faded through the “AI winters”. Backpropagation (1986) gave a practical way to train several layers. Deep Blue (1997) beat Kasparov at chess using hand-written rules and brute-force search, not learning. In 2012 AlexNet, a deep network trained on graphics chips, won an image-recognition contest by a wide margin and the field changed direction. 2017: the transformer. 2022: ChatGPT. Why then? A practical training method, far more data, far faster chips. Mention AlphaGo (2016) if students know it: it beat a top Go player after learning from human games and from playing itself.

---

## Part 2 · Neural networks

### 10 · AI is a family of nested ideas

“AI” is a moving target: chess programs were AI in the 1990s; now we barely call them that. Most of what people mean by AI today sits in the inner boxes: machine learning, and specifically deep learning. Chatbots like ChatGPT, Claude and Gemini are large language models, the innermost box. Everything else today zooms into that box.

### 11 · Machine learning flips programming around

This is the single most important idea of the lecture. For decades, programmers tried to write rules for things like recognizing faces or translating languages, and it mostly failed: the world has too many exceptions (recall the dog detector). Machine learning stops trying to write the rules and instead learns them from examples. The catch: the “rules” it learns are millions of numbers, not sentences a person can read.

### 12 · An artificial neuron is a tiny calculator

Walk through the numbers. Each input is multiplied by a weight that says how much it matters: barking matters a lot (0.9), having wings counts against “dog” (−1.0). Add them up: 1.5. Then squash the result into a range between 0 and 1 (the sigmoid function), giving 0.82, which we can read as “82% confident it’s a dog”. That’s the whole neuron. For a brain lab: this is loosely inspired by a biological neuron (inputs like dendrites, weights like synaptic strength, fire if the total is high enough), but it’s a cartoon of the real thing; we come back to that in the discussion.

### 13 · Play with a neuron (try it)

The neuron from slide 12, but the students control it. Switch inputs on and off and drag the weights; the sum and the squashed score update live. The bias is a built-in nudge that makes the neuron fire more or less easily before it looks at any input. Task: make any barking animal score above 80%, furry or not (the Barks weight has to dominate). Then make the Wings weight positive and ask what the neuron now believes. Nobody sets these by hand in real models; the next slides show how they are found.

### 14 · From one neuron to a network

One neuron combines its inputs in one simple way. Wire many together in layers, each feeding the next, and the network can build complex ideas out of simple ones (in image networks, early layers pick up edges, later layers combine them into shapes and objects). “Deep” means many layers. Every line in the drawing is a weight: this toy has 20; large language models have billions. The drawing is an illustration, not a real model.

### 15 · Learning means nudging the weights downhill

Analogy: you’re on a foggy hillside and want to reach the valley floor. You can’t see the bottom, but you can feel which way the ground slopes under your feet, so you take a small step downhill, and repeat. That’s gradient descent. The “slope” is computed by an algorithm called backpropagation, which works out how much each weight contributed to the error. Real networks have billions of weights, so the “hillside” has billions of dimensions, but the idea is the same.

### 16 · Watch a neuron learn (try it)

A one-neuron model learns “is it a dog?” from five labelled examples (the examples are made up). All weights start at zero, so it says 50% for everything. Each round shows it all five examples and nudges the weights. After two rounds it already gets all five right; after ten it is confident. Watch Barks grow and Wings turn negative. Ask: why does Barks keep growing while Furry turns negative? (Both dogs bark, but cats and bats are furry and are not dogs, so “furry” ends up counting slightly against “dog”. That is an artefact of five tiny examples, and a good reminder that a model learns whatever patterns its data contains.) Nobody told it that barking means dog.

---

## Part 3 · Inside a chatbot

### 17 · First, text is chopped into tokens

Now we zoom into a language model, in four steps. Step one: tokenization. Common words get their own token; rarer words are split into reusable pieces. Each piece has an ID number in a fixed vocabulary, typically tens of thousands to a couple of hundred thousand entries. The exact split and IDs on this slide are made up for illustration; every model has its own tokenizer. Fun consequence: models can struggle with tasks like counting the letters in a word, because they never see individual letters.

### 18 · Each token becomes a point in “meaning space”

Each token ID is looked up in a giant table and turned into a long list of numbers, its embedding. You can think of that list as coordinates. During training, tokens that appear in similar contexts get pushed to similar places, so meaning becomes geometry. The classic finding from word2vec (2013): king minus man plus woman lands near queen. This 2D map is a simplified drawing, not real model data.

### 19 · The model’s one job: guess the next token

This is the core loop of every chatbot. The network takes all the tokens so far and outputs a probability for every token in its vocabulary. One is chosen (usually a likely one, with a little randomness so answers aren’t identical every time; that setting is called temperature), it’s appended, and the whole thing runs again. Be the model: before the bars grow, have the room shout the next word. Ask: if it only ever picks the single most likely word, what might go wrong? (Repetitive, bland text.) The percentages here are invented for illustration.

### 20 · Attention lets each word look at its context

Before 2017, language models read text one word at a time and struggled to connect words far apart. The transformer, introduced in the paper “Attention Is All You Need”, lets every token look at every other token and decide how relevant each one is. Here, a single word at the end (tired vs. wide) changes what “it” should attend to. Real models run many attention “heads” in parallel, across dozens of layers, so they track grammar, references, topic and tone at once. The highlighting is a simplified illustration of the idea.

### 21 · Pretraining repeats that guess at enormous scale

Pretraining is just the next-token game from slide 19, played on a huge slice of the internet, books and code. Every wrong guess nudges the weights a little (the downhill walk from slide 15). Doing this over trillions of tokens forces the model to absorb grammar, facts, styles of reasoning and much more, because all of those help predict the next word. Nobody programs in “facts”: they emerge as a side effect of getting good at prediction. Note how the pieces fit: billions of weights, trillions of examples.

### 22 · Three stages turn a text predictor into a chatbot

Try this framing: a pretrained model asked “What is the capital of France?” might just continue with “What is the capital of Germany?”, because lists of quiz questions are common online. Fine-tuning on example dialogues teaches the question-and-answer format. Stage 3 is often called RLHF, reinforcement learning from human feedback: people compare pairs of answers, and the model is trained to produce the kind they prefer. This is also where companies shape tone, safety behaviour and refusals.

### 23 · The same recipe now sees, hears and acts

Modern assistants are “multimodal”: one model handles text, images and audio by converting each into tokens. “Agents” go a step further: the model can output a special message like “search the web for X” or “run this Python code”. Software outside the model carries it out and pastes the result back in as more tokens. That’s how a chatbot can analyse a CSV like the one from Workshop 1: it writes and runs code, it doesn’t do the arithmetic in its head.

---

## Part 4 · Using it well

### 24 · Four ways it goes wrong

All four follow from what we’ve seen. Hallucination: the model is always producing the most plausible continuation, and a made-up reference can look just as plausible as a real one. Bias: it mirrors its training data. Cutoff: the weights are frozen when training ends. Lab-relevant example: never paste a citation, a statistic or a methods detail from a chatbot into anything without checking the original source. And remember privacy: don’t paste participant data into a public chatbot.

### 25 · Fluent isn’t the same as true

Pause here. Everything today comes down to this: these systems are extraordinarily good at producing text that sounds right, because that is exactly what they were trained to do. Sounding right and being right usually go together, which is why they’re so useful, but the model has no separate step that checks the truth. That’s your job.

### 26 · Let’s talk it through

Pick one or two depending on time. Q1: there’s no settled answer; push students to say what they mean by “understand”. Q2 links back to Workshops 1 and 2: run it on mock data, check the output CSV by hand for a few trials, read every line you don’t understand. Q3 is for a memory and brain lab: real neurons spike, use many neurotransmitters, rewire continuously and learn from few examples; artificial ones are simple weighted sums trained offline on enormous data. Finally, revisit the guesses from slide 2: which survived?

### 27 · Practice this week

Four short activities for the week; ask for at least two. Break the rule bot (slide 5), predict then run the Turing machine (slide 7), train the neuron and explain why the weights move (slide 16), and check a chatbot’s references. Invite students to bring surprising results to the next lab meeting.

### 28 · Key words

A glossary of twelve terms for reference. Each is explained on the slide where it first appears.
