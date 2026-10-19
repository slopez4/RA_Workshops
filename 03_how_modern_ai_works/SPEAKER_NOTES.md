# Speaker Notes — How Modern AI Works

Notes for each of the 16 [slides](https://slopez4.github.io/RA_Workshops/03_how_modern_ai_works/slides.html).
Timing and the minute-by-minute script are in [`TEACHING_GUIDE.md`](TEACHING_GUIDE.md).

---

## 1 · How modern AI works

Welcome to Workshop 3. Workshop 1 was analysing data in Python; Workshop 2 was building an experiment in PsychoPy. Today is less hands-on: the tools many of you already use to help with that code. Today’s goal: by the end of the hour, everyone should be able to explain, in plain words, what happens when you type a question into a chatbot. No math background needed; we’ll use one small worked example and lots of pictures.

## 2 · Today’s question

Ask the room: who has used a chatbot this week? What do you think is happening inside? Collect a few guesses (it searches the internet, it has a database of answers, it thinks like a person). Keep them on the board; we’ll come back to them at the end and see which survive.

## 3 · AI is a family of nested ideas

“AI” is a moving target: chess programs were AI in the 1990s; now we barely call them that. Most of what people mean by AI today sits in the inner boxes: machine learning, and specifically deep learning. Chatbots like ChatGPT, Claude and Gemini are large language models, the innermost box. Everything else today zooms into that box.

## 4 · Machine learning flips programming around

This is the single most important idea of the lecture. For decades, programmers tried to write rules for things like recognizing faces or translating languages, and it mostly failed: the world has too many exceptions. Machine learning stops trying to write the rules and instead learns them from examples. The catch: the “rules” it learns are millions of numbers, not sentences a person can read.

## 5 · An artificial neuron is a tiny calculator

Walk through the numbers. Each input is multiplied by a weight that says how much it matters: barking matters a lot (0.9), having wings counts against “dog” (−1.0). Add them up: 1.5. Then squash the result into a range between 0 and 1 (here with the sigmoid function), giving 0.82, which we can read as “82% confident it’s a dog”. That’s the whole neuron. For a brain lab: this is loosely inspired by a biological neuron (inputs like dendrites, weights like synaptic strength, fire if the total is high enough), but it’s a cartoon of the real thing; we come back to that in the discussion. The power comes from connecting enormous numbers of them, where each layer feeds the next.

## 6 · Learning means nudging the weights downhill

Analogy: you’re on a foggy hillside and want to reach the valley floor. You can’t see the bottom, but you can feel which way the ground slopes under your feet, so you take a small step downhill, and repeat. That’s gradient descent. The “slope” is computed by an algorithm called backpropagation, which works out how much each weight contributed to the error. Real networks have billions of weights, so the “hillside” has billions of dimensions, but the idea is the same.

## 7 · First, text is chopped into tokens

Now we zoom into a language model, in four steps. Step one: tokenization. Common words get their own token; rarer words are split into reusable pieces. Each piece has an ID number in a fixed vocabulary, typically tens of thousands to a couple of hundred thousand entries. The exact split and IDs on this slide are made up for illustration; every model has its own tokenizer. Fun consequence: models can struggle with tasks like counting the letters in a word, because they never see individual letters.

## 8 · Each token becomes a point in “meaning space”

Each token ID is looked up in a giant table and turned into a long list of numbers, its embedding. You can think of that list as coordinates. During training, tokens that appear in similar contexts get pushed to similar places, so meaning becomes geometry. The classic finding from word2vec (2013): king minus man plus woman lands near queen. This 2D map is a simplified drawing, not real model data.

## 9 · The model’s one job: guess the next token

This is the core loop of every chatbot. The network takes all the tokens so far and outputs a probability for every token in its vocabulary. One is chosen (usually a likely one, with a little randomness so answers aren’t identical every time; that setting is called temperature), it’s appended, and the whole thing runs again. Ask students: if it only ever picks the single most likely word, what might go wrong? (Repetitive, bland text.) The percentages here are invented for illustration.

## 10 · Attention lets each word look at its context

Before 2017, language models read text one word at a time and struggled to connect words far apart. The transformer, introduced in the paper “Attention Is All You Need”, lets every token look at every other token and decide how relevant each one is. Here, a single word at the end (tired vs. wide) changes what “it” should attend to. Real models run many attention “heads” in parallel, across dozens of layers, so they track grammar, references, topic and tone at once. The highlighting is a simplified illustration of the idea.

## 11 · Pretraining repeats that guess at enormous scale

Pretraining is just the next-token game from step 3, played on a huge slice of the internet, books and code. Every wrong guess nudges the weights a little (the downhill walk from earlier). Doing this over trillions of tokens forces the model to absorb grammar, facts, styles of reasoning and much more, because all of those help predict the next word. Nobody programs in “facts”: they emerge as a side effect of getting good at prediction. Note how the pieces fit: billions of weights, trillions of examples.

## 12 · Three stages turn a text predictor into a chatbot

Try this framing: a pretrained model asked “What is the capital of France?” might just continue with “What is the capital of Germany?”, because lists of quiz questions are common online. Fine-tuning on example dialogues teaches the question-and-answer format. Stage 3 is often called RLHF, reinforcement learning from human feedback: people compare pairs of answers, and the model is trained to produce the kind they prefer. This is also where companies shape tone, safety behaviour and refusals.

## 13 · The same recipe now sees, hears and acts

Modern assistants are “multimodal”: one model handles text, images and audio by converting each into tokens in the same space. “Agents” go a step further: the model can output a special message like “search the web for X” or “run this Python code”. Software outside the model carries it out and pastes the result back in as more tokens. That’s how a chatbot can analyse a CSV like the one from Workshop 1: it writes and runs code, it doesn’t do the arithmetic in its head.

## 14 · Four ways it goes wrong

All four follow from what we’ve seen. Hallucination: the model is always producing the most plausible continuation, and a made-up reference can look just as plausible as a real one. Bias: it mirrors its training data. Cutoff: the weights are frozen when training ends. Lab-relevant example: never paste a citation, a statistic or a methods detail from a chatbot into anything without checking the original source. And remember privacy: don’t paste participant data into a public chatbot.

## 15 · Fluent isn’t the same as true

Pause here. Everything today comes down to this: these systems are extraordinarily good at producing text that sounds right, because that is exactly what they were trained to do. Sounding right and being right usually go together, which is why they’re so useful, but the model has no separate step that checks the truth. That’s your job.

## 16 · Let’s talk it through

Pick one or two depending on time. Q1: there’s no settled answer; push students to say what they mean by “understand”. Q2 links back to Workshops 1 and 2: run it on mock data, check the output CSV by hand for a few trials, read every line you don’t understand. Q3 is for a memory and brain lab: real neurons spike, use many neurotransmitters, rewire continuously and learn from few examples; artificial ones are simple weighted sums trained offline on enormous data. Finally, revisit the guesses from slide 2: which survived?
