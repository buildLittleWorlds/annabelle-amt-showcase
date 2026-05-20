# Annabelle Li — Publishable Paper Plan

## Working title

**When the Map Loses the City: Testing Whether CPU-Friendly AI Music Transcription Produces Music a Performer Can Actually Use**

Alternative titles:

- **From Audio to Score Is Not One Problem: A Musician-Centered Evaluation of Lightweight Automatic Music Transcription**
- **Pitch Detection Is Not Musical Representation: Failure Modes in a Free-Tier AI Sheet-Music Pipeline**
- **Can a Free AI Transcription Tool Make Readable Sheet Music? A Student Research Case Study**

## One-sentence claim

Annabelle's paper should argue that lightweight, CPU-deployable automatic music transcription can sometimes recover pitch contour, but it often fails at the higher-level musical decisions — meter, rhythm, voicing, clef, dynamics, and notation readability — that determine whether a score is usable by real musicians.

## Why this can become publishable

The strongest version of this paper is not a claim that Annabelle invented a better AMT model. The contribution is a clear, musician-centered evaluation of what a currently accessible AMT pipeline actually produces when deployed on free student-accessible infrastructure.

That makes the project publishable as a student research brief because it combines:

1. a real deployed tool,
2. a clear research question,
3. reproducible test inputs,
4. visible output artifacts,
5. a failure taxonomy,
6. and a usable next-stage evaluator: the AMT Report Card.

## Core research question

> How do the architectural and computational constraints of lightweight AI music transcription systems affect their ability to produce notation that is musically readable and practically useful for performers?

## Sharper sub-questions

1. Which dimensions fail first: pitch, rhythm, timing, dynamics, meter, clef, or readability?
2. Does failure increase as musical texture moves from a scale, to a familiar melody, to a polyphonic piece?
3. Is the main gap a transcription problem, a MIDI-to-notation problem, or a performer-usability problem?
4. What can a free-tier student-built tool evaluate reliably, even when it cannot solve full transcription?

## Proposed paper structure

### 1. Abstract

One paragraph. State the problem, method, main finding, and contribution.

Model sentence:

> This paper evaluates a student-built automatic music transcription pipeline deployed on Hugging Face Spaces. The pipeline uses Basic Pitch to convert audio to MIDI, music21 to convert MIDI into symbolic notation, and LilyPond to render sheet music. Three test cases — a C major scale, *Twinkle Twinkle Little Star*, and Bach's Minuet in G — show that pitch contour may survive in the simplest case, but rhythm, meter, voicing, dynamics, and score readability degrade quickly. The paper argues that the central limitation is not only model accuracy but the gap between pitch-event detection and performer-readable musical representation.

### 2. Introduction: the promise and the gap

Open with Annabelle's motivation as a musician: transcription is difficult, time-consuming, and potentially made more accessible by AI. Then introduce the problem: existing tools often return output that looks like sheet music but does not behave like usable notation.

The introduction should end with the claim that the paper evaluates transcription from the musician's side, not only from the model's side.

### 3. Background: AMT is a chain, not a single task

Explain that automatic music transcription involves multiple subtasks: pitch detection, onset/offset detection, rhythm extraction, meter inference, instrument separation, dynamics, and notation rendering. Annabelle should make this the conceptual center of the paper.

Key distinction:

- **MIDI-level success**: the system detected note events.
- **Score-level success**: the system produced readable notation.
- **Performer-level success**: a musician could actually practice or perform from it.

### 4. System built

Describe her pipeline in a clean architecture diagram:

```text
Audio input
   ↓
Basic Pitch — audio to MIDI note events
   ↓
music21 — quantization and MusicXML conversion
   ↓
LilyPond — engraved sheet music / SVG viewer
   ↓
AMT Report Card — comparison against reference MIDI + musician review
```

She should frame the free Hugging Face CPU tier as a meaningful research constraint rather than an embarrassment. The constraint is part of the research question: what happens when an ambitious music-AI tool has to run on infrastructure a student can actually access?

### 5. Methods

Use three test cases, but make the method more formal.

| Test | Why it matters | Expected output |
|---|---|---|
| C major scale | simplest monophonic baseline | eight clear quarter notes in ascending order |
| Twinkle Twinkle | familiar melody with repeated notes and simple rhythm | short readable melody, no chord clusters |
| Minuet in G | polyphonic / repertoire stress test | recognizable meter, two-voice structure, bass/treble separation |

Add a short protocol:

1. Record or upload audio.
2. Run it through the same deployed pipeline.
3. Save MIDI, MusicXML, and rendered score.
4. Compare against a known reference MIDI.
5. Score pitch, timing, rhythm, and dynamics with the AMT Report Card.
6. Add a musician-centered readability judgment.

### 6. Results

This should be a results section, not just a narrative.

Recommended results table:

| Dimension | C major scale | Twinkle Twinkle | Minuet in G | Pattern |
|---|---|---|---|---|
| Pitch contour | partly survives | buried by false notes | mostly lost | degrades with texture |
| Rhythm | wrong | wrong | wrong | fails across all tests |
| Meter | mostly correct | unstable | wrong | no reliable meter inference |
| Voicing | not relevant | false chord clusters | false dense chords | overtones become notes |
| Dynamics | absent | absent | absent | not represented |
| Performer readability | barely usable | unusable | unusable | score-like output is not score usability |

Then include the three output figures she already has.

### 7. Discussion

This is the most important section. The discussion should make the larger argument:

- Basic Pitch can detect sound events, but notation requires musical interpretation.
- MIDI is not sheet music; MIDI lacks meter, phrasing, key, voice-leading, and notational intention unless those are inferred later.
- A readable score is a compressed performer-facing abstraction, not a literal dump of every frequency peak.
- The free-tier CPU constraint forces a tradeoff between accessibility and transcription sophistication.
- For beginning musicians, a bad transcription may be worse than no transcription because it hides errors inside professional-looking notation.

### 8. Limitations

Annabelle should be direct and confident:

- only three test pieces,
- one main model,
- one deployment tier,
- limited repeated trials,
- reference MIDI quality matters,
- tests are mostly Western tonal music.

Then emphasize that the paper is valuable because it turns those limitations into a next-stage test platform.

### 9. Future work / next build

The next research artifact is the improved **AMT Musician Lab**:

- compare audio to reference MIDI,
- quantify note-event recall and precision,
- show timing and duration errors,
- detect likely false-positive/overtone clusters,
- produce a musician-facing usability review,
- save artifacts for reproducibility.

Next experiments:

1. instrument comparison: voice vs. piano vs. guitar;
2. texture comparison: monophonic vs. chordal vs. two-voice;
3. model comparison: Basic Pitch vs. heavier AMT system;
4. usability comparison: score output judged by musicians, not only by metrics.

## What Annabelle should revise in `PAPER.md`

### Keep

- the title metaphor, “When the Map Loses the City”;
- the personal musician perspective;
- the three test cases;
- the argument that the output is not performer-ready;
- the tension between accessibility and accuracy.

### Strengthen

- turn “what happened” into a methods/results structure;
- add a table of measured outcomes from AMT Report Card;
- distinguish pitch detection, MIDI transcription, and notation rendering;
- explain CPU/free-tier deployment as a research constraint;
- make the conclusion more direct: the tool does not fail randomly; it fails at the exact places where notation becomes musical interpretation.

### Cut or compress

- long debugging detail unless it supports the accessibility argument;
- repeated phrases about “wrong pitches/wrong rhythms”; consolidate into the failure taxonomy;
- unsupported claims about all AMT models; keep the claims specific to her pipeline and supported literature.

## Publishable final deliverables

1. **Paper:** revised `PAPER.md` with figures, method table, results table, and references.
2. **Website:** GitHub Pages showcase explaining the project, showing screenshots, and linking to the app and paper.
3. **App:** improved Hugging Face Space that lets a user run a transcription, compare it with a reference MIDI, and download outputs.
4. **Portfolio framing:** Annabelle should describe herself as studying “music AI, automatic transcription, and musician-centered evaluation.”
