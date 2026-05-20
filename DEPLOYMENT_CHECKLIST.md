# Deployment checklist for Annabelle showcase handoff

## Instructor-owned finished demo

### GitHub Pages showcase
- [ ] Create a public GitHub repo, e.g. `annabelle-amt-showcase`.
- [ ] Copy this bundle into the repo.
- [ ] Confirm the repo has `docs/index.html`.
- [ ] Commit and push.
- [ ] In GitHub: Settings -> Pages -> Deploy from a branch -> `main` -> `/docs`.
- [ ] Open the published Pages URL.
- [ ] Confirm the site labels itself as an instructor-prepared model/demo, not as Annabelle's already-finished work.
- [ ] If an instructor-owned Hugging Face demo Space exists, update the website app link to that Space.

### Hugging Face demo Space
- [ ] Create a new Gradio Space under the instructor account.
- [ ] Upload the contents of `huggingface-space/`.
- [ ] Confirm `app.py`, `requirements.txt`, `packages.txt`, and `README.md` are at the Space root.
- [ ] Add any optional API key as a Space secret, not in the code.
- [ ] Test with a short/simple audio input.
- [ ] Copy the Space URL into the website if desired.

## Student-owned reproduction

### Annabelle's GitHub repo
- [ ] Copy or adapt `/docs` into `annabelle-z-li/AI-research-level-2`.
- [ ] Update website links to Annabelle's own GitHub and Hugging Face pages.
- [ ] Add at least one screenshot or concrete example from her own project.
- [ ] Enable GitHub Pages from `/docs`.

### Annabelle's Hugging Face Space
- [ ] Duplicate the instructor demo Space or create a new Gradio Space.
- [ ] Revise the README in Annabelle's own voice.
- [ ] Run at least three test inputs: scale, simple melody, more complex music.
- [ ] Save results/screenshots for the paper and website.

### Annabelle's paper
- [ ] Revise or create `PAPER.md`.
- [ ] Use the stronger frame: AI transcription vs musician-readable notation.
- [ ] Add her own test-result table.
- [ ] Add screenshots or concrete outputs.
- [ ] Explain limitations honestly.

## Instructor demo language to keep

Use language like "instructor-prepared model showcase" or "demo version based on Annabelle's public coursework." Avoid language that implies Annabelle personally completed every polished page, app feature, or paper paragraph before she has revised it herself.
