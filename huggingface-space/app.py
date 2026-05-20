import csv
import json
import math
import os
import shutil
import subprocess
import tempfile
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional

import gradio as gr
import music21
import numpy as np
import pretty_midi
import requests

# Gradio 4.36 sometimes crashes while generating API schema for complex outputs.
try:
    import gradio_client.utils as _gcu
    _orig_schema_to_type = _gcu._json_schema_to_python_type

    def _safe_schema_to_type(schema, defs=None):
        try:
            return _orig_schema_to_type(schema, defs)
        except TypeError:
            return "Any"

    _gcu._json_schema_to_python_type = _safe_schema_to_type
except Exception:
    pass

try:
    from basic_pitch.inference import predict
    import basic_pitch as _basic_pitch
except Exception:
    predict = None
    _basic_pitch = None


@dataclass
class NoteEvent:
    pitch: int
    start: float
    end: float
    velocity: int
    instrument: str = "Unknown"
    program: int = 0
    is_drum: bool = False

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)


@dataclass
class Match:
    ref_index: int
    hyp_index: int
    pitch_error: int
    onset_error: float
    duration_error: float


GRADE_COLORS = {
    "A": "#4ade80",
    "B": "#a3e635",
    "C": "#facc15",
    "D": "#fb923c",
    "F": "#f87171",
    "N/A": "#9ca3af",
}


def letter_grade(score: Optional[float]) -> str:
    if score is None:
        return "N/A"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def clamp_score(value: float) -> int:
    return int(round(max(0, min(100, value))))


def model_path() -> str:
    if _basic_pitch is None:
        raise RuntimeError("basic_pitch could not be imported. Check requirements.txt and Python 3.10.")
    bp_dir = Path(_basic_pitch.__file__).parent
    onnx_path = bp_dir / "saved_models" / "icassp_2022" / "nmp.onnx"
    if onnx_path.exists():
        return str(onnx_path)
    return str(bp_dir / "saved_models" / "icassp_2022")


def status_box(message: str, tone: str = "info") -> str:
    colors = {
        "info": "#a78bfa",
        "good": "#4ade80",
        "warn": "#facc15",
        "bad": "#f87171",
    }
    color = colors.get(tone, colors["info"])
    return f"""
    <div class='status-box'>
      <p style='color:{color};margin:0'>{message}</p>
    </div>
    """


def extract_notes(midi_path: str) -> list[NoteEvent]:
    midi = pretty_midi.PrettyMIDI(midi_path)
    events: list[NoteEvent] = []
    for inst in midi.instruments:
        name = inst.name or pretty_midi.program_to_instrument_name(inst.program)
        for n in inst.notes:
            events.append(
                NoteEvent(
                    pitch=int(n.pitch),
                    start=float(n.start),
                    end=float(n.end),
                    velocity=int(n.velocity),
                    instrument=name,
                    program=int(inst.program),
                    is_drum=bool(inst.is_drum),
                )
            )
    events.sort(key=lambda n: (n.start, n.pitch, n.end))
    return events


def write_note_csv(notes: list[NoteEvent], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["pitch", "pitch_name", "start", "end", "duration", "velocity", "instrument"],
        )
        writer.writeheader()
        for note in notes:
            writer.writerow(
                {
                    "pitch": note.pitch,
                    "pitch_name": pretty_midi.note_number_to_name(note.pitch),
                    "start": round(note.start, 4),
                    "end": round(note.end, 4),
                    "duration": round(note.duration, 4),
                    "velocity": note.velocity,
                    "instrument": note.instrument,
                }
            )


def estimate_tempo(audio_path: str) -> Optional[float]:
    try:
        import librosa

        y, sr = librosa.load(audio_path, sr=None, mono=True, duration=120)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        if isinstance(tempo, np.ndarray):
            tempo = tempo.item()
        tempo = float(tempo)
        if math.isfinite(tempo) and tempo > 0:
            return tempo
    except Exception:
        return None
    return None


def run_basic_pitch(audio_path: str, out_dir: str) -> tuple[str, list[NoteEvent]]:
    if predict is None:
        raise RuntimeError("Basic Pitch is unavailable. Check requirements.txt and rebuild the Space.")
    _, midi_data, _ = predict(audio_path, model_path())
    midi_path = os.path.join(out_dir, "transcription.mid")
    midi_data.write(midi_path)
    return midi_path, extract_notes(midi_path)


def midi_to_musicxml(midi_path: str, out_dir: str, tempo_bpm: Optional[float]) -> tuple[str, Optional[Any]]:
    score = music21.converter.parse(midi_path)
    try:
        score = score.quantize(quarterLengthDivisors=(4, 3))
    except Exception:
        pass
    if tempo_bpm:
        try:
            first_part = score.parts[0] if score.parts else score
            first_part.insert(0, music21.tempo.MetronomeMark(number=round(tempo_bpm)))
        except Exception:
            pass
    xml_path = os.path.join(out_dir, "transcription.musicxml")
    score.write("musicxml", fp=xml_path)
    return xml_path, score


def render_lilypond_svg(score: Any, out_dir: str) -> str:
    lilypond = shutil.which("lilypond")
    if not lilypond:
        return ""
    try:
        ly_path = os.path.join(out_dir, "score.ly")
        score.write("lilypond", fp=ly_path)
        subprocess.run(
            [lilypond, "--svg", "-o", os.path.join(out_dir, "score_render"), ly_path],
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        svg_paths = sorted(
            os.path.join(out_dir, name)
            for name in os.listdir(out_dir)
            if name.startswith("score_render") and name.endswith(".svg")
        )
        pages = []
        for path in svg_paths[:4]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                pages.append(f"<div class='score-page'>{f.read()}</div>")
        return "".join(pages)
    except Exception:
        return ""


def greedy_match_notes(
    ref: list[NoteEvent],
    hyp: list[NoteEvent],
    onset_tolerance: float,
    pitch_tolerance: int,
) -> list[Match]:
    used_hyp: set[int] = set()
    matches: list[Match] = []

    for ri, rn in enumerate(ref):
        candidates = []
        for hi, hn in enumerate(hyp):
            if hi in used_hyp:
                continue
            pitch_error = abs(rn.pitch - hn.pitch)
            onset_error = abs(rn.start - hn.start)
            if pitch_error <= pitch_tolerance and onset_error <= onset_tolerance:
                duration_error = abs(rn.duration - hn.duration)
                distance = onset_error + (0.05 * pitch_error) + (0.1 * duration_error)
                candidates.append((distance, hi, pitch_error, onset_error, duration_error))
        if candidates:
            _, hi, pitch_error, onset_error, duration_error = min(candidates, key=lambda x: x[0])
            used_hyp.add(hi)
            matches.append(Match(ri, hi, pitch_error, onset_error, duration_error))

    return matches


def pitch_coverage(ref: list[NoteEvent], hyp: list[NoteEvent], pitch_tolerance: int) -> int:
    if not ref:
        return 0
    hyp_pitches = [n.pitch for n in hyp]
    covered = sum(1 for rn in ref if any(abs(rn.pitch - hp) <= pitch_tolerance for hp in hyp_pitches))
    return clamp_score(100 * covered / len(ref))


def dynamics_score(ref: list[NoteEvent], hyp: list[NoteEvent], pitch_tolerance: int) -> tuple[Optional[int], str]:
    soft_ref = [n for n in ref if n.velocity < 50]
    if not soft_ref:
        return None, "No soft notes in the reference MIDI, so dynamics cannot be judged from this file."
    hyp_pitches = [n.pitch for n in hyp]
    found = sum(1 for rn in soft_ref if any(abs(rn.pitch - hp) <= pitch_tolerance for hp in hyp_pitches))
    return clamp_score(100 * found / len(soft_ref)), f"{found}/{len(soft_ref)} soft reference notes were detected."


def summarize_texture(notes: list[NoteEvent]) -> dict[str, Any]:
    if not notes:
        return {"count": 0, "duration": 0, "pitch_range": "none", "max_simultaneous": 0, "avg_velocity": 0}
    duration = max(n.end for n in notes) - min(n.start for n in notes)
    pitches = [n.pitch for n in notes]
    # Estimate simultaneous-note density at note onset times.
    max_simultaneous = 0
    for time in [n.start for n in notes[:500]]:
        simultaneous = sum(1 for n in notes if n.start <= time < n.end)
        max_simultaneous = max(max_simultaneous, simultaneous)
    return {
        "count": len(notes),
        "duration": round(duration, 3),
        "pitch_range": f"{pretty_midi.note_number_to_name(min(pitches))}–{pretty_midi.note_number_to_name(max(pitches))}",
        "max_simultaneous": max_simultaneous,
        "avg_velocity": round(sum(n.velocity for n in notes) / len(notes), 1),
    }


def score_transcription(
    ref_notes: list[NoteEvent],
    hyp_notes: list[NoteEvent],
    onset_tolerance_ms: int,
    pitch_tolerance: int,
) -> dict[str, Any]:
    onset_tol_seconds = max(0.025, onset_tolerance_ms / 1000)
    matches = greedy_match_notes(ref_notes, hyp_notes, onset_tol_seconds, pitch_tolerance)
    note_recall = clamp_score(100 * len(matches) / len(ref_notes)) if ref_notes else 0
    note_precision = clamp_score(100 * len(matches) / len(hyp_notes)) if hyp_notes else 0
    pitch_score = pitch_coverage(ref_notes, hyp_notes, pitch_tolerance)

    if matches:
        avg_onset = sum(m.onset_error for m in matches) / len(matches)
        timing_score = clamp_score(100 * (1 - min(avg_onset / (onset_tol_seconds * 2), 1)))
        avg_duration_error = sum(m.duration_error for m in matches) / len(matches)
        avg_ref_duration = sum(ref_notes[m.ref_index].duration for m in matches) / len(matches)
        if avg_ref_duration > 0:
            duration_score = clamp_score(100 * (1 - min(avg_duration_error / max(avg_ref_duration, 0.001), 1)))
        else:
            duration_score = 0
    else:
        avg_onset = None
        avg_duration_error = None
        timing_score = 0
        duration_score = 0

    dyn_score, dyn_detail = dynamics_score(ref_notes, hyp_notes, pitch_tolerance)
    false_positive_ratio = (len(hyp_notes) / len(ref_notes)) if ref_notes else 0

    metrics = {
        "note_recall": {"score": note_recall, "detail": f"{len(matches)}/{len(ref_notes)} reference note events matched."},
        "note_precision": {"score": note_precision, "detail": f"{len(matches)}/{len(hyp_notes)} hypothesis notes matched a reference note."},
        "pitch_coverage": {"score": pitch_score, "detail": "Reference pitches found somewhere in the transcription, ignoring exact rhythm."},
        "timing": {"score": timing_score, "detail": "Average onset error: " + (f"{avg_onset:.3f} seconds." if avg_onset is not None else "no matches.")},
        "duration": {"score": duration_score, "detail": "Average duration error: " + (f"{avg_duration_error:.3f} seconds." if avg_duration_error is not None else "no matches.")},
        "dynamics": {"score": dyn_score, "detail": dyn_detail},
        "matched_notes": len(matches),
        "reference_notes": len(ref_notes),
        "hypothesis_notes": len(hyp_notes),
        "false_positive_ratio": round(false_positive_ratio, 2),
        "matches": [asdict(m) for m in matches],
    }
    return metrics


def overall_score(metrics: dict[str, Any]) -> Optional[int]:
    keys = ["note_recall", "note_precision", "pitch_coverage", "timing", "duration"]
    scores = [metrics[k]["score"] for k in keys if metrics.get(k, {}).get("score") is not None]
    if metrics.get("dynamics", {}).get("score") is not None:
        scores.append(metrics["dynamics"]["score"])
    if not scores:
        return None
    return clamp_score(sum(scores) / len(scores))


def build_radar_svg(metrics: dict[str, Any]) -> str:
    labels = [
        ("Recall", metrics["note_recall"]["score"]),
        ("Precision", metrics["note_precision"]["score"]),
        ("Pitch", metrics["pitch_coverage"]["score"]),
        ("Timing", metrics["timing"]["score"]),
        ("Duration", metrics["duration"]["score"]),
    ]
    cx, cy, radius = 175, 175, 112
    angles = [math.pi / 2 + i * 2 * math.pi / len(labels) for i in range(len(labels))]

    def point(score: float, angle: float) -> tuple[float, float]:
        r = radius * (score / 100)
        return cx + r * math.cos(angle), cy - r * math.sin(angle)

    grid = []
    for ring in [25, 50, 75, 100]:
        pts = []
        for angle in angles:
            x = cx + radius * (ring / 100) * math.cos(angle)
            y = cy - radius * (ring / 100) * math.sin(angle)
            pts.append(f"{x:.1f},{y:.1f}")
        grid.append(f"<polygon points='{ ' '.join(pts) }' fill='none' stroke='#3b2852' stroke-width='1'/>")

    axes = []
    label_svg = []
    for (label, score), angle in zip(labels, angles):
        x = cx + radius * math.cos(angle)
        y = cy - radius * math.sin(angle)
        axes.append(f"<line x1='{cx}' y1='{cy}' x2='{x:.1f}' y2='{y:.1f}' stroke='#3b2852'/>")
        lx = cx + (radius + 38) * math.cos(angle)
        ly = cy - (radius + 38) * math.sin(angle)
        anchor = "middle"
        if lx < cx - 10:
            anchor = "end"
        elif lx > cx + 10:
            anchor = "start"
        grade = letter_grade(score)
        label_svg.append(
            f"<text x='{lx:.1f}' y='{ly:.1f}' text-anchor='{anchor}' fill='#e8e0f5' font-size='11' font-family='monospace'>{label}</text>"
            f"<text x='{lx:.1f}' y='{ly + 15:.1f}' text-anchor='{anchor}' fill='{GRADE_COLORS[grade]}' font-size='12' font-weight='700' font-family='monospace'>{score}% {grade}</text>"
        )

    data_pts = [point(score, angle) for (_, score), angle in zip(labels, angles)]
    data_poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in data_pts)
    dots = "".join(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4' fill='#e879f9'/>" for x, y in data_pts)

    return f"""
    <svg viewBox='0 0 350 350' class='radar-svg' role='img' aria-label='Radar chart of transcription scores'>
      {''.join(grid)}
      {''.join(axes)}
      <polygon points='{data_poly}' fill='#c084fc' fill-opacity='0.25' stroke='#c084fc' stroke-width='2'/>
      {dots}
      {''.join(label_svg)}
    </svg>
    """


def build_timeline_svg(ref_notes: list[NoteEvent], hyp_notes: list[NoteEvent], max_notes: int = 160) -> str:
    if not hyp_notes and not ref_notes:
        return "<p class='muted'>No note events to visualize.</p>"
    sample_ref = ref_notes[:max_notes]
    sample_hyp = hyp_notes[:max_notes]
    all_notes = sample_ref + sample_hyp
    min_time = min(n.start for n in all_notes)
    max_time = max(n.end for n in all_notes)
    min_pitch = min(n.pitch for n in all_notes) - 2
    max_pitch = max(n.pitch for n in all_notes) + 2
    width, height = 920, 340
    pad_left, pad_right, pad_top, pad_bottom = 55, 20, 30, 45
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bottom

    def x_for(t: float) -> float:
        if max_time <= min_time:
            return pad_left
        return pad_left + ((t - min_time) / (max_time - min_time)) * plot_w

    def y_for(pitch: int) -> float:
        if max_pitch <= min_pitch:
            return pad_top + plot_h / 2
        return pad_top + (1 - ((pitch - min_pitch) / (max_pitch - min_pitch))) * plot_h

    ref_lines = []
    for n in sample_ref:
        x1, x2, y = x_for(n.start), x_for(n.end), y_for(n.pitch)
        ref_lines.append(f"<line x1='{x1:.1f}' x2='{x2:.1f}' y1='{y:.1f}' y2='{y:.1f}' class='ref-note'/>")
    hyp_lines = []
    for n in sample_hyp:
        x1, x2, y = x_for(n.start), x_for(n.end), y_for(n.pitch)
        hyp_lines.append(f"<line x1='{x1:.1f}' x2='{x2:.1f}' y1='{y:.1f}' y2='{y:.1f}' class='hyp-note'/>")

    pitch_labels = []
    for pitch in np.linspace(min_pitch, max_pitch, num=6):
        p = int(round(pitch))
        y = y_for(p)
        pitch_labels.append(
            f"<line x1='{pad_left}' x2='{width-pad_right}' y1='{y:.1f}' y2='{y:.1f}' class='grid-line'/>"
            f"<text x='10' y='{y+4:.1f}' class='axis-label'>{pretty_midi.note_number_to_name(p)}</text>"
        )

    return f"""
    <div class='timeline-wrap'>
      <svg viewBox='0 0 {width} {height}' class='timeline-svg' role='img' aria-label='Reference and hypothesis note timeline'>
        <text x='{pad_left}' y='18' class='axis-label'>Reference notes are green. AI transcription notes are pink.</text>
        {''.join(pitch_labels)}
        {''.join(ref_lines)}
        {''.join(hyp_lines)}
        <line x1='{pad_left}' x2='{width-pad_right}' y1='{height-pad_bottom}' y2='{height-pad_bottom}' class='axis-line'/>
        <text x='{pad_left}' y='{height-12}' class='axis-label'>0 sec</text>
        <text x='{width-pad_right-80}' y='{height-12}' class='axis-label'>{max_time-min_time:.1f} sec</text>
      </svg>
    </div>
    """


def build_report_html(
    metrics: Optional[dict[str, Any]],
    hyp_summary: dict[str, Any],
    ref_summary: Optional[dict[str, Any]],
    tempo: Optional[float],
    timeline_svg: str,
) -> str:
    tempo_text = f"{tempo:.1f} BPM" if tempo else "not detected"
    if metrics is None:
        return f"""
        <div class='report'>
          <h2>Transcription Summary</h2>
          <div class='summary-grid'>
            <div><span>Detected tempo</span><strong>{tempo_text}</strong></div>
            <div><span>AI note events</span><strong>{hyp_summary['count']}</strong></div>
            <div><span>Pitch range</span><strong>{hyp_summary['pitch_range']}</strong></div>
            <div><span>Max simultaneous notes</span><strong>{hyp_summary['max_simultaneous']}</strong></div>
          </div>
          <p class='muted'>Upload a reference MIDI to turn this into a scored report card.</p>
          {timeline_svg}
        </div>
        """

    overall = overall_score(metrics)
    grade = letter_grade(overall)
    radar = build_radar_svg(metrics)
    score_rows = []
    for key, label in [
        ("note_recall", "Note recall"),
        ("note_precision", "Note precision"),
        ("pitch_coverage", "Pitch coverage"),
        ("timing", "Timing"),
        ("duration", "Duration"),
        ("dynamics", "Dynamics"),
    ]:
        score = metrics[key]["score"]
        g = letter_grade(score)
        color = GRADE_COLORS[g]
        score_label = "N/A" if score is None else f"{score}%"
        bar_width = 0 if score is None else score
        score_rows.append(
            f"""
            <div class='metric-row'>
              <div class='metric-head'><span>{label}</span><strong style='color:{color}'>{score_label} {g}</strong></div>
              <div class='bar'><div style='width:{bar_width}%;background:{color}'></div></div>
              <p>{metrics[key]['detail']}</p>
            </div>
            """
        )

    false_ratio = metrics["false_positive_ratio"]
    warning = ""
    if false_ratio >= 2:
        warning = "<p class='warning'>The AI produced far more notes than the reference. This often means overtones, resonance, or noise are being counted as extra pitches.</p>"
    elif metrics["note_precision"]["score"] < 50:
        warning = "<p class='warning'>Low precision means many AI notes do not correspond to the reference. The score may look detailed while being musically misleading.</p>"

    return f"""
    <div class='report'>
      <h2>AMT Report Card</h2>
      <div class='report-grid'>
        <div>
          <div class='overall-card'>
            <span>Overall</span>
            <strong style='color:{GRADE_COLORS[grade]}'>{grade}</strong>
            <small>{overall}% average</small>
          </div>
          {''.join(score_rows)}
        </div>
        <div>{radar}</div>
      </div>
      {warning}
      <h3>Run summary</h3>
      <div class='summary-grid'>
        <div><span>Detected tempo</span><strong>{tempo_text}</strong></div>
        <div><span>Reference notes</span><strong>{ref_summary['count'] if ref_summary else 0}</strong></div>
        <div><span>AI notes</span><strong>{hyp_summary['count']}</strong></div>
        <div><span>False-positive ratio</span><strong>{false_ratio}</strong></div>
      </div>
      {timeline_svg}
    </div>
    """


def rule_based_review(metrics: Optional[dict[str, Any]], hyp_notes: list[NoteEvent], ref_notes: Optional[list[NoteEvent]]) -> str:
    hyp_summary = summarize_texture(hyp_notes)
    if metrics is None:
        return (
            "### Musician's Review\n\n"
            "This run produced a transcription, but no reference MIDI was provided, so I can only describe the output rather than grade it. "
            f"The AI produced **{hyp_summary['count']} note events** across a pitch range of **{hyp_summary['pitch_range']}**. "
            "To judge whether the score is performer-ready, upload a matching reference MIDI and compare pitch, timing, rhythm, and dynamics."
        )

    overall = overall_score(metrics)
    grade = letter_grade(overall)
    recall = metrics["note_recall"]["score"]
    precision = metrics["note_precision"]["score"]
    timing = metrics["timing"]["score"]
    duration = metrics["duration"]["score"]
    false_ratio = metrics["false_positive_ratio"]

    problems = []
    if precision < 60:
        problems.append("many extra notes that do not match the reference")
    if recall < 60:
        problems.append("missing or misplaced reference notes")
    if timing < 60:
        problems.append("unstable note onsets")
    if duration < 60:
        problems.append("durations that do not preserve the rhythm")
    if false_ratio >= 2:
        problems.append("possible overtone or resonance false positives")
    if not problems:
        problems.append("minor inaccuracies that still need performer review")

    performer = (
        "A performer could probably use this as a rough sketch only." if grade in {"C", "D"}
        else "A performer should not rely on this score without substantial correction." if grade == "F"
        else "A performer may be able to use this as a starting point, but it still needs checking."
    )

    return (
        "### Musician's Review\n\n"
        f"**Overall assessment:** This transcription receives a **{grade}** based on the available reference comparison.\n\n"
        f"**What went wrong:** The main issues are {', '.join(problems)}.\n\n"
        f"**Performer usability:** {performer} If the notation looks polished, remember that visual polish is not the same as musical accuracy.\n\n"
        "**One thing it got right:** Even weak AMT output can still reveal approximate pitch regions or contours, which may be useful as a first diagnostic artifact."
    )


def call_groq_review(metrics: Optional[dict[str, Any]], hyp_summary: dict[str, Any], ref_summary: Optional[dict[str, Any]]) -> Optional[str]:
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key or metrics is None:
        return None
    prompt = f"""
You are a musician and music theory teacher evaluating an AI-generated transcription.

Metrics:
{json.dumps(metrics, indent=2)[:5000]}

Hypothesis summary: {hyp_summary}
Reference summary: {ref_summary}

Write a concise musician-facing report with these sections:
- Overall assessment
- What went wrong
- What a performer would struggle with
- One thing it got right
- Grade
Keep it under 220 words. Be concrete about rhythm, pitch, timing, meter, voicing, dynamics, or notation readability where appropriate.
"""
    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "max_tokens": 500,
                "messages": [
                    {"role": "system", "content": "You are an expert music teacher reviewing AI music transcription."},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=30,
        )
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content")
    except Exception:
        return None


def run_lab(
    audio_path: Optional[str],
    reference_midi_path: Optional[str],
    onset_tolerance_ms: int,
    pitch_tolerance: int,
    use_llm_review: bool,
):
    if audio_path is None:
        return status_box("Upload an audio file or record from the microphone.", "warn"), "", "", None, None, None, None

    out_dir = tempfile.mkdtemp(prefix="amt-musician-lab-")
    try:
        tempo = estimate_tempo(audio_path)
        midi_path, hyp_notes = run_basic_pitch(audio_path, out_dir)
        xml_path, score = midi_to_musicxml(midi_path, out_dir, tempo)
        csv_path = os.path.join(out_dir, "transcription-note-events.csv")
        write_note_csv(hyp_notes, csv_path)
        score_html = render_lilypond_svg(score, out_dir) if score is not None else ""
        if not score_html:
            score_html = "<div class='score-fallback'>LilyPond rendering is unavailable. Download the MusicXML file and open it in MuseScore, Finale, Sibelius, or another notation program.</div>"

        ref_notes = None
        metrics = None
        ref_summary = None
        if reference_midi_path:
            ref_notes = extract_notes(reference_midi_path)
            ref_summary = summarize_texture(ref_notes)
            metrics = score_transcription(ref_notes, hyp_notes, onset_tolerance_ms, pitch_tolerance)
            timeline = build_timeline_svg(ref_notes, hyp_notes)
        else:
            timeline = build_timeline_svg([], hyp_notes)

        hyp_summary = summarize_texture(hyp_notes)
        report_html = build_report_html(metrics, hyp_summary, ref_summary, tempo, timeline)

        review = None
        if use_llm_review:
            review = call_groq_review(metrics, hyp_summary, ref_summary)
        if not review:
            review = rule_based_review(metrics, hyp_notes, ref_notes)

        summary_json_path = os.path.join(out_dir, "run-summary.json")
        with open(summary_json_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "tempo_bpm": tempo,
                    "hypothesis_summary": hyp_summary,
                    "reference_summary": ref_summary,
                    "metrics": metrics,
                },
                f,
                indent=2,
            )

        return "", report_html, score_html, review, midi_path, xml_path, csv_path, summary_json_path

    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        details = traceback.format_exc()
        html = status_box(f"Something went wrong: {error}", "bad") + f"<pre class='trace'>{details}</pre>"
        return html, "", "", "", None, None, None, None


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Mono:wght@300;400;500&display=swap');
body, .gradio-container {
  background: #090812 !important;
  color: #f2edf8 !important;
  font-family: 'DM Mono', monospace !important;
}
.gradio-container { max-width: 1180px !important; margin: 0 auto !important; }
.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 3rem;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(135deg,#c084fc,#e879f9,#fb923c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
  margin-bottom: 0.4rem;
}
.hero-subtitle { text-align:center; color:#b8aac9; margin-bottom:1.4rem; }
.panel, .report, .score-fallback, .status-box {
  background: #15101f !important;
  border: 1px solid #3b2852 !important;
  border-radius: 18px !important;
  padding: 1rem !important;
}
button.primary-btn {
  background: linear-gradient(135deg,#7c3aed,#db2777) !important;
  border: none !important;
  color: white !important;
  border-radius: 12px !important;
  font-weight: 800 !important;
}
label, .muted { color: #b8aac9 !important; }
.report h2, .report h3 { font-family: 'Playfair Display', serif; margin-top: 0; }
.report-grid { display: grid; grid-template-columns: minmax(240px, 1fr) minmax(260px, 0.8fr); gap: 1rem; align-items: start; }
.overall-card { background:#0f0b17; border:1px solid #3b2852; border-radius:16px; padding:1rem; text-align:center; margin-bottom:1rem; }
.overall-card span { display:block; color:#b8aac9; text-transform:uppercase; font-size:0.75rem; letter-spacing:0.12em; }
.overall-card strong { display:block; font-family:'Playfair Display',serif; font-size:4rem; line-height:1; }
.overall-card small { color:#b8aac9; }
.metric-row { margin-bottom:1rem; }
.metric-head { display:flex; justify-content:space-between; gap:1rem; align-items:baseline; }
.metric-head span { font-weight:800; }
.metric-row p { margin:0.35rem 0 0; color:#b8aac9; font-size:0.82rem; }
.bar { height:7px; border-radius:999px; background:#2b203a; overflow:hidden; margin-top:0.3rem; }
.bar div { height:100%; border-radius:999px; }
.summary-grid { display:grid; grid-template-columns: repeat(auto-fit,minmax(155px,1fr)); gap:0.7rem; margin:1rem 0; }
.summary-grid div { background:#0f0b17; border:1px solid #3b2852; border-radius:12px; padding:0.8rem; }
.summary-grid span { display:block; color:#b8aac9; font-size:0.75rem; }
.summary-grid strong { display:block; font-size:1.2rem; }
.warning { color:#facc15; background:rgba(250,204,21,0.1); border:1px solid rgba(250,204,21,0.25); padding:0.8rem; border-radius:12px; }
.radar-svg { width:100%; max-width:350px; display:block; margin:auto; }
.timeline-wrap { overflow-x:auto; background:#0f0b17; border:1px solid #3b2852; border-radius:14px; padding:0.5rem; margin-top:1rem; }
.timeline-svg { width:100%; min-width:760px; }
.ref-note { stroke:#4ade80; stroke-width:5; stroke-linecap:round; opacity:0.85; }
.hyp-note { stroke:#e879f9; stroke-width:3; stroke-linecap:round; opacity:0.75; }
.grid-line { stroke:#2b203a; stroke-width:1; }
.axis-line { stroke:#7a6d94; stroke-width:1.5; }
.axis-label { fill:#b8aac9; font-size:12px; font-family:monospace; }
.score-page { background:white; border-radius:12px; padding:1rem; margin-bottom:1rem; overflow:auto; }
.score-page svg { width:100%; height:auto; display:block; }
.trace { white-space: pre-wrap; color:#fca5a5; overflow:auto; max-height:300px; }
@media (max-width: 760px) { .report-grid { grid-template-columns: 1fr; } .hero-title { font-size: 2.2rem; } }
"""

with gr.Blocks(css=CSS, title="AMT Musician Lab") as demo:
    gr.HTML("""
    <div>
      <div class='hero-title'>AMT Musician Lab</div>
      <p class='hero-subtitle'>Audio → MIDI → MusicXML · Reference scoring · Musician-centered usability review</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1, elem_classes="panel"):
            audio_input = gr.Audio(
                label="Audio input",
                sources=["upload", "microphone"],
                type="filepath",
            )
            reference_midi = gr.File(
                label="Reference MIDI for report card (optional)",
                file_types=[".mid", ".midi"],
                type="filepath",
            )
            onset_tol = gr.Slider(
                minimum=50,
                maximum=500,
                step=25,
                value=150,
                label="Onset tolerance for note matching (ms)",
            )
            pitch_tol = gr.Slider(
                minimum=0,
                maximum=2,
                step=1,
                value=0,
                label="Pitch tolerance (semitones)",
            )
            llm_toggle = gr.Checkbox(
                label="Use Groq LLM review if GROQ_API_KEY is set",
                value=True,
            )
            run_button = gr.Button("Generate transcription report", elem_classes="primary-btn")
            gr.Markdown(
                """
                **Tips**
                - Start with short, clean audio.
                - Upload a matching reference MIDI for real scoring.
                - Without a reference MIDI, the app creates outputs but cannot grade accuracy.
                - Use the note-event CSV as evidence in the paper.
                """
            )

        with gr.Column(scale=2):
            status_output = gr.HTML()
            with gr.Tabs():
                with gr.Tab("Report Card"):
                    report_output = gr.HTML()
                with gr.Tab("Sheet Music Viewer"):
                    score_output = gr.HTML()
                with gr.Tab("Musician Review"):
                    review_output = gr.Markdown()
                with gr.Tab("Downloads"):
                    midi_output = gr.File(label="Generated MIDI")
                    xml_output = gr.File(label="Generated MusicXML")
                    csv_output = gr.File(label="Note-event CSV")
                    json_output = gr.File(label="Run summary JSON")

    run_button.click(
        fn=run_lab,
        inputs=[audio_input, reference_midi, onset_tol, pitch_tol, llm_toggle],
        outputs=[status_output, report_output, score_output, review_output, midi_output, xml_output, csv_output, json_output],
    )


demo.queue()
demo.launch(server_name="0.0.0.0", server_port=7860)
