# AGENTS.md — Codex guidance for Annabelle AMT final product

## Project purpose
This repository is a handoff bundle for Annabelle Li's final AI + Research Level 2 project. It turns her existing AI music transcription work into three more polished deliverables:

1. a publishable paper direction;
2. a GitHub Pages showcase site;
3. a more functional Hugging Face Gradio Space.

This is an instructor-prepared model/handoff package. Do not present it as if Annabelle personally authored every polished element. Help convert it into materials she can revise, own, and reproduce.

## Known public student context
- Student: Annabelle Li
- GitHub profile: annabelle-z-li
- Main coursework repo: annabelle-z-li/AI-research-level-2
- Hugging Face profile: annabelle-li
- Relevant Hugging Face Spaces: amt-report-card, music-to-sheet-music

## Repository layout
- `docs/` — static GitHub Pages website. Main entry: `docs/index.html`.
- `paper/ANNABELLE_PUBLISHABLE_PAPER_PLAN.md` — paper plan and revision architecture.
- `huggingface-space/` — Gradio Space files. Main app: `huggingface-space/app.py`.
- `ANNABELLE_INSTRUCTOR_HANDOFF.md` — instructor-facing deployment and handoff strategy.
- `ANNABELLE_STUDENT_REPRODUCTION_WALKTHROUGH.md` — student-facing reproduction steps.
- `CODEX_HANDOFF.md` — high-level source-of-truth brief for Codex tasks.
- `CODEX_FIRST_PROMPT.txt` — first prompt the instructor can paste into Codex.

## Build and verification commands
Static website:
- No build step is required.
- Verify `docs/index.html`, `docs/styles.css`, and `docs/script.js` exist.
- Optional local preview from repo root: `python3 -m http.server 8000 --directory docs`

Hugging Face Space:
- Verify syntax first: `python3 -m py_compile huggingface-space/app.py`
- Do not install heavy dependencies unless the user asks you to run the app locally.
- Do not hard-code API keys. Use Space secrets/environment variables only.

Repository sanity:
- Keep all handoff docs in Markdown.
- Keep paths simple so a student can understand the structure.
- Avoid adding unnecessary build tooling.

## Authorship, privacy, and classroom constraints
- Keep student information limited to public usernames and project facts already provided.
- Avoid private course details, grades, personal data, or instructor-only comments in public-facing files.
- Distinguish clearly between an instructor model/demo and Annabelle's student-owned final version.
- The student reproduction walkthrough should be simple enough for a beginner who has used GitHub and Hugging Face but may not be confident with terminal workflows.

## What “done” means
A successful Codex task should leave the repo with:
- a clean static website that can be published from `/docs` on GitHub Pages;
- a Hugging Face Space folder with the files needed for a Gradio Space;
- a paper plan that Annabelle can revise in her own voice;
- handoff documentation for both instructor deployment and student reproduction;
- no secrets, no broken links that can be avoided, and no unexplained placeholder text.

## Preferred working style
- Make concrete file changes rather than only giving advice.
- Explain the final diff in plain language.
- When making assumptions, state them briefly.
- Keep student-facing language encouraging and ownership-preserving.
