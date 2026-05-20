const cases = {
  scale: {
    title: "C major scale",
    summary: "The simplest baseline. The pitch contour mostly survives, but the rhythm is wrong enough that the notation is barely performable.",
    points: [
      "Pitch contour loosely visible.",
      "Uniform quarter notes become uneven durations.",
      "This shows that rhythm fails even before polyphony becomes an issue."
    ],
    image: "https://raw.githubusercontent.com/annabelle-z-li/AI-research-level-2/main/assets/scale-output.png",
    alt: "Output score for C major scale",
    caption: "Actual output from the Music to Sheet Music pipeline."
  },
  twinkle: {
    title: "Twinkle Twinkle Little Star",
    summary: "A familiar melody should be easy to recognize, but the transcription expands into dense chord clusters and loses the melody.",
    points: [
      "Single melody becomes multi-note vertical clusters.",
      "The score grows far longer than the simple tune should require.",
      "Likely false positives and overtones bury the actual melody."
    ],
    image: "https://raw.githubusercontent.com/annabelle-z-li/AI-research-level-2/main/assets/twinkle-output.png",
    alt: "Output score for Twinkle Twinkle Little Star",
    caption: "A simple melody becomes visually dense and difficult to identify."
  },
  minuet: {
    title: "Minuet in G",
    summary: "The repertoire stress test shows the clearest breakdown: wrong meter, missing voice structure, dense clusters, and little performer usability.",
    points: [
      "The piece is in 3/4, but the output defaults to unsuitable groupings.",
      "The two-voice structure is not represented cleanly.",
      "The result looks like notation but does not function as a score."
    ],
    image: "https://raw.githubusercontent.com/annabelle-z-li/AI-research-level-2/main/assets/minuet-output.png",
    alt: "Output score for Minuet in G",
    caption: "The most complex test produces the least performer-readable output."
  }
};

const title = document.getElementById("case-title");
const summary = document.getElementById("case-summary");
const points = document.getElementById("case-points");
const image = document.getElementById("case-image");
const caption = document.getElementById("case-caption");

function setCase(key) {
  const item = cases[key];
  title.textContent = item.title;
  summary.textContent = item.summary;
  image.src = item.image;
  image.alt = item.alt;
  caption.textContent = item.caption;
  points.innerHTML = item.points.map(point => `<li>${point}</li>`).join("");
  document.querySelectorAll(".tab").forEach(button => {
    button.classList.toggle("active", button.dataset.case === key);
  });
}

document.querySelectorAll(".tab").forEach(button => {
  button.addEventListener("click", () => setCase(button.dataset.case));
});
