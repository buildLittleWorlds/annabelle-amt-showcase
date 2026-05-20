# Deployed Demo Links

## Instructor-owned showcase

- GitHub repository: <https://github.com/buildLittleWorlds/annabelle-amt-showcase>
- GitHub Pages site: <https://buildlittleworlds.github.io/annabelle-amt-showcase/>
- Source folder for GitHub Pages: `docs/`

This site is an instructor-prepared model showcase based on Annabelle's public coursework. It should be shown as a destination model, not as Annabelle's already-finished student-authored submission.

## Hugging Face Space

The Gradio Space files are ready in `huggingface-space/`, but the instructor-owned Hugging Face demo is not deployed from this machine because `hf auth whoami` reports that the local CLI is not logged in.

Recommended Space name:

```text
annabelle-amt-musician-lab-demo
```

After logging in, upload these files to the Space root:

```text
huggingface-space/app.py
huggingface-space/requirements.txt
huggingface-space/packages.txt
huggingface-space/README.md
```
