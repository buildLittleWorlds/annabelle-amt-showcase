# Codex handoff brief — Annabelle final product bundle

## Why this bundle exists
The instructor is entering the final session of an AI + Research Level 2 course. Annabelle already has public work on GitHub and Hugging Face around AI music transcription, but the instructor wants to help her bridge from a working class project to a more impressive, professional-looking final portfolio.

This bundle should become a source-of-truth repository that Codex can operate on directly, instead of requiring the instructor to paste long ChatGPT conversations and code snippets into each new Codex session.

## Public context from the course tracker
- Annabelle's GitHub profile: `annabelle-z-li`
- Annabelle's main coursework repo: `AI-research-level-2`
- Annabelle's Hugging Face profile: `annabelle-li`
- Public-facing project direction: AI music transcription, musician-readable notation, AMT evaluation/reporting
- Relevant Hugging Face Spaces: `music-to-sheet-music` and `amt-report-card`

## Deliverables in this repository

### 1. Publishable paper plan
File: `paper/ANNABELLE_PUBLISHABLE_PAPER_PLAN.md`

Purpose: Help Annabelle reframe her project from “I made a music transcription app” into a stronger research narrative about the gap between audio-to-MIDI transcription and musician-readable notation.

Desired student-owned outcome: Annabelle revises this into `PAPER.md` in her own repo, adding her own examples, screenshots, test cases, and conclusions.

### 2. GitHub Pages website
Files:
- `docs/index.html`
- `docs/styles.css`
- `docs/script.js`

Purpose: Provide a polished static showcase site that can be deployed first under the instructor's GitHub account, then copied or adapted into Annabelle's own repo.

Deployment target: GitHub Pages from the `/docs` folder.

Desired student-owned outcome: Annabelle updates language, links, screenshots, and examples so the page becomes her final project site.

### 3. Hugging Face Space app
Files:
- `huggingface-space/app.py`
- `huggingface-space/requirements.txt`
- `huggingface-space/packages.txt`
- `huggingface-space/README.md`

Purpose: Provide a more integrated Gradio Space prototype that combines music transcription with a musician-facing quality report.

Desired student-owned outcome: Annabelle duplicates or recreates the Space, revises the README, runs a few test cases, and links it from the website and paper.

## Recommended Codex workflow

### Phase 1 — instructor showcase repo
Create or update a GitHub repo under the instructor's account, for example:

`annabelle-amt-showcase`

Tasks:
1. Copy this bundle into the repo.
2. Make sure `/docs` is ready for GitHub Pages.
3. Replace generic placeholder links with instructor-owned demo links where available.
4. Keep clear language that this is an instructor-prepared model/demo based on Annabelle's project direction.
5. Verify `docs/index.html` loads locally if possible.

### Phase 2 — student reproduction package
Tasks:
1. Keep `ANNABELLE_STUDENT_REPRODUCTION_WALKTHROUGH.md` concise and usable.
2. Add a final checklist Annabelle can complete.
3. Make sure all instructions can be followed without needing the original ChatGPT conversation.
4. Use plain language and avoid advanced Git unless there is an easier browser-based alternative.

### Phase 3 — student-owned repo adaptation
When the instructor is ready to help Annabelle directly, use Codex on Annabelle's repo or on a fork/copy:

`annabelle-z-li/AI-research-level-2`

Tasks:
1. Add `/docs` with the website.
2. Update links to Annabelle's own GitHub and Hugging Face pages.
3. Add or revise `PAPER.md` based on the paper plan.
4. Link the website, paper, GitHub repo, and Hugging Face Space together.
5. Keep Annabelle's voice and examples central.

## Suggested final public framing
Use language like this:

> This project explores the difference between AI transcription and musician-readable notation. The goal is not simply to convert audio into MIDI, but to evaluate whether the output is useful for a musician trying to understand, revise, or perform the result.

Avoid language like this:

> This app solves AI music transcription.

## Safety and integrity notes
- Do not invent test results. Leave blanks or placeholders where Annabelle needs to add her own outcomes.
- Do not include private student records or grading comments.
- Do not hide instructor assistance. The correct framing is: instructor-provided model, student-revised final product.
- Do not put API keys in files.

## Minimal verification checklist
Before saying the bundle is ready:

- [ ] `docs/index.html` exists and references `styles.css` and `script.js` correctly.
- [ ] `huggingface-space/app.py` passes Python syntax checking.
- [ ] `huggingface-space/README.md` explains the Space clearly.
- [ ] `paper/ANNABELLE_PUBLISHABLE_PAPER_PLAN.md` is still present.
- [ ] `ANNABELLE_STUDENT_REPRODUCTION_WALKTHROUGH.md` gives student-owned steps.
- [ ] Public-facing language distinguishes model/demo from student-authored work.
