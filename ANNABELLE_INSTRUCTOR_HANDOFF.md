# Annabelle Final Product Handoff: Instructor Version

## Goal

Give Annabelle two versions of the same project:

1. **A polished model version** she can see immediately as a finished public-facing product.
2. **A reproduction path** that lets her rebuild the same product inside her own GitHub and Hugging Face accounts.

This keeps the final session encouraging rather than overwhelming: she sees what her work can become, then follows a bounded checklist to make it her own.

---

## The three final products

### Product 1: Paper

**Working title:**

> From Audio-to-MIDI to Musician-Readable Notation: Testing the Limits of AI Music Transcription

**Instructor handoff version:**

Put `paper/ANNABELLE_PUBLISHABLE_PAPER_PLAN.md` in the showcase repo and link it from the website.

**Student-owned version:**

Annabelle converts the plan into a finished `PAPER.md` in her own `AI-research-level-2` repo. She should add:

- her own introduction;
- screenshots from her Spaces;
- a short table of test cases;
- a paragraph explaining what failed or was hard;
- a conclusion about why musician-readable notation is harder than audio-to-MIDI conversion.

---

### Product 2: Website

**Instructor handoff version:**

Deploy the `docs/` folder in your own GitHub account first.

Suggested repo name:

```text
annabelle-amt-showcase
```

Suggested GitHub Pages URL pattern:

```text
https://YOUR-GITHUB-USERNAME.github.io/annabelle-amt-showcase/
```

Current instructor demo:

```text
https://buildlittleworlds.github.io/annabelle-amt-showcase/
```

Current source repo:

```text
https://github.com/buildLittleWorlds/annabelle-amt-showcase
```

**Student-owned version:**

Annabelle copies the same `docs/` folder into her own repo and changes the text so it is written in her voice. She should update the links to her own GitHub repo and Hugging Face Spaces.

---

### Product 3: Hugging Face Space

**Instructor handoff version:**

Deploy `huggingface-space/` as an instructor-owned Hugging Face Space first.

Suggested Space name:

```text
annabelle-amt-musician-lab-demo
```

Suggested Space subtitle:

```text
A demo version of Annabelle's AI music transcription final project.
```

**Student-owned version:**

Annabelle creates her own Space or duplicates yours, then replaces the README with her own description and adds her own test audio/results.

---

## Recommended final-session flow

### First 10 minutes: Show the polished version

Open three tabs:

1. The GitHub Pages website.
2. The Hugging Face Space.
3. The paper plan or paper draft.

Say something like:

> This is not meant to erase your work or replace your authorship. It is a polished model built from the direction of your project. Your job is to decide what parts are accurate, revise it into your own voice, and own the final version.

### Next 15 minutes: Explain the portfolio logic

Frame the deliverable as a portfolio, not just an assignment:

- **The paper** proves she can explain the research problem.
- **The website** proves she can present the project publicly.
- **The Space** proves she can build an interactive AI prototype.

### Next 20–30 minutes: Make one live edit together

Do not try to rebuild everything live. Instead, make one visible edit in each product:

1. Change one sentence on the website.
2. Change one paragraph in the paper plan.
3. Change one sentence in the Space README.

Then commit/push one of those changes so she sees the deployment loop.

### Final 10 minutes: Give her the reproduction checklist

Hand her `ANNABELLE_STUDENT_REPRODUCTION_WALKTHROUGH.md` and ask for three concrete final actions:

1. Deploy the website from her GitHub repo.
2. Deploy or duplicate the Hugging Face Space.
3. Revise the paper plan into a finished `PAPER.md`.

---

## Best way to avoid overwhelming her

Do **not** present the handoff as “Here are 20 files.” Present it as:

> You already built the project idea. I made a polished model version so you can see where it can go. Now we are going to make your version of it.

Then give her this simple ownership checklist:

- Replace instructor wording with her own wording.
- Replace placeholder links with her own links.
- Add screenshots from her own Space.
- Add at least three test cases.
- Write a short reflection on what worked and what did not.

---

## Instructor deployment checklist

### GitHub Pages demo

1. Create a public GitHub repo named `annabelle-amt-showcase`.
2. Upload or push the full contents of this kit.
3. Confirm that `docs/index.html` exists.
4. Go to **Settings → Pages**.
5. Choose **Deploy from a branch**.
6. Select `main` and `/docs`.
7. Save.
8. Copy the published Pages link.

### Hugging Face Space demo

1. Create a new Hugging Face Space.
2. Choose **Gradio** as the SDK.
3. Use a clear name like `annabelle-amt-musician-lab-demo`.
4. Upload the files from `huggingface-space/`:
   - `app.py`
   - `requirements.txt`
   - `packages.txt`
   - `README.md`
5. Wait for the Space to build.
6. Test the upload tab with a short audio clip.
7. Copy the Space link.

Status note: the Hugging Face Space files are ready, but the instructor-owned demo Space has not been deployed from this machine because the local `hf` CLI is not logged in.

### Paper demo

1. Keep the paper plan in `paper/ANNABELLE_PUBLISHABLE_PAPER_PLAN.md`.
2. Link to it from the website.
3. Invite Annabelle to turn it into her own `PAPER.md`.

---

## Suggested handoff message to Annabelle

Subject: Final project upgrade path — paper, website, and app

Hi Annabelle,

For the final session, I put together a polished model version of your AI music transcription project. This is not meant to replace your work. It is meant to show what your project can look like when it is shaped into a professional final portfolio.

There are three parts:

1. A stronger paper plan about the difference between audio-to-MIDI transcription and musician-readable notation.
2. A public project website that explains your research question and prototype.
3. A more integrated Hugging Face app that transcribes music and gives a musician-facing report.

Your job is to make the final version yours: revise the language, update the links, add your own screenshots and test cases, and explain what you learned from building it.

We will use the model version first so you can see the destination, then we will walk through how to reproduce it in your own GitHub and Hugging Face accounts.
