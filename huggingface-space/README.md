---
title: AMT Musician Lab
emoji: 🎼
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 4.36.1
app_file: app.py
pinned: false
python_version: '3.10'
---

# AMT Musician Lab

A more functional version of Annabelle's music-transcription project.

## What it does

1. Upload an audio recording.
2. Run Basic Pitch to create a MIDI transcription.
3. Convert the MIDI into MusicXML and, if LilyPond is available, an inline SVG score viewer.
4. Optionally upload a reference MIDI file.
5. Score the transcription across note recall, precision, timing, duration, pitch coverage, and dynamics.
6. Produce a musician-centered usability review.
7. Download MIDI, MusicXML, note-events CSV, and a JSON summary.

## Why this is different from the original Space

The original app mostly asked: “Can I turn audio into sheet music?”

This version asks a stronger research question: “When the tool turns audio into sheet music, what musical information survives, what fails, and would a performer actually be able to use the output?”

## Recommended use

Use short, clean recordings first:

- C major scale
- Twinkle Twinkle Little Star
- a short two-voice piano excerpt
- solo voice or solo instrument

For the Report Card mode, upload a matching reference MIDI file.

## Optional secret

Add `GROQ_API_KEY` in Space settings to enable the LLM-generated musician review. Without it, the app generates a rule-based review.
