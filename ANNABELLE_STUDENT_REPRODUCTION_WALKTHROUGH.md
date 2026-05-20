# Annabelle Student Walkthrough: Rebuilding the Final Products Yourself

## What you are making

You are turning your AI music transcription work into a three-part final portfolio:

1. **A paper** explaining the research problem.
2. **A website** that presents the project publicly.
3. **A Hugging Face app** that demonstrates the tool.

The goal is not just to show that you experimented with AI tools. The goal is to show that you understand a real problem:

> AI can sometimes turn audio into notes, but making notation that musicians can actually read and trust is much harder.

---

# Part 1: Put the website in your GitHub repo

## Step 1: Open your GitHub repo

Go to your coursework repository:

```text
annabelle-z-li/AI-research-level-2
```

## Step 2: Add the website files

Copy the full `docs/` folder into your repo.

The folder should contain:

```text
docs/index.html
docs/styles.css
docs/script.js
```

## Step 3: Edit the website so it is yours

Open `docs/index.html` and change:

- the opening description;
- any placeholder links;
- any wording that does not sound like you;
- the GitHub link;
- the Hugging Face links;
- the paper link.

You do not need to rewrite everything at once. Start by changing the first paragraph and the links.

## Step 4: Commit and push

Use GitHub’s web editor, GitHub Desktop, or the command line. A good commit message would be:

```text
Add final project website
```

## Step 5: Turn on GitHub Pages

In your repo:

1. Go to **Settings**.
2. Click **Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Choose branch: `main`.
5. Choose folder: `/docs`.
6. Click **Save**.

After it finishes, GitHub will give you a public website link.

---

# Part 2: Build your own Hugging Face Space

## Step 1: Create a new Space

Go to Hugging Face and create a new Space.

Suggested name:

```text
amt-musician-lab
```

Suggested SDK:

```text
Gradio
```

Suggested visibility:

```text
Public
```

## Step 2: Upload the app files

Upload these files from the `huggingface-space/` folder:

```text
app.py
requirements.txt
packages.txt
README.md
```

## Step 3: Wait for the Space to build

The first build may take a while because the app installs audio and music transcription tools.

If it fails, open the build logs and look for the first error message. The most common problems are:

- missing package;
- package version conflict;
- audio conversion dependency problem;
- Space sleeping or needing a restart.

## Step 4: Test the app with a simple audio file

Start with a short, simple melody or scale.

Good first tests:

- a C major scale;
- a short single-note melody;
- “Twinkle Twinkle Little Star” played on one instrument.

Avoid starting with a full complex recording. A complicated piece may fail or produce messy notation, and that failure should be part of the research discussion rather than the first test.

## Step 5: Save evidence

Take screenshots of:

- the upload screen;
- the output files;
- the chart or report;
- any error or limitation you discover.

These screenshots can go into your website and paper.

---

# Part 3: Turn the paper plan into your final paper

## Step 1: Open the paper plan

Use:

```text
paper/ANNABELLE_PUBLISHABLE_PAPER_PLAN.md
```

## Step 2: Create your own final paper file

In your GitHub repo, create or revise:

```text
PAPER.md
```

## Step 3: Use this structure

```markdown
# From Audio-to-MIDI to Musician-Readable Notation

## 1. What I wanted to build

## 2. The rudimentary baseline

## 3. The constraint I hit

## 4. What I tried first

## 5. The move that worked

## 6. What the final prototype does

## 7. What I learned

## 8. What I would improve next
```

## Step 4: Add a test table

Use a table like this:

```markdown
| Test input | What I expected | What happened | What I learned |
|---|---|---|---|
| C major scale | Clean notes and simple rhythm |  |  |
| Simple melody | Mostly correct pitch sequence |  |  |
| More complex music | More errors in rhythm/notation |  |  |
```

## Step 5: Add your main claim

A strong main claim could be:

> My project showed me that AI music transcription is not only a technical problem of detecting pitches. It is also a communication problem: the output has to be readable and useful for musicians.

Revise this into your own words.

---

# Final checklist

Before you are finished, make sure you have:

- [ ] A live GitHub Pages website.
- [ ] A working or mostly working Hugging Face Space.
- [ ] A revised `PAPER.md` in your GitHub repo.
- [ ] At least three test cases.
- [ ] Screenshots or examples from your own app.
- [ ] Links between the website, GitHub repo, paper, and Space.
- [ ] A short explanation of what failed or still needs work.

---

# What to say in your final presentation

Use this structure:

1. **The problem:** AI can generate musical note data, but readable sheet music is harder.
2. **The experiment:** I tested audio-to-MIDI and notation tools on simple and more complex music.
3. **The prototype:** I built a Space that transcribes audio and gives a report.
4. **The finding:** Simple monophonic music works better than complex music, and evaluation is necessary.
5. **The next step:** Improve the report card and test more examples with real musicians.

