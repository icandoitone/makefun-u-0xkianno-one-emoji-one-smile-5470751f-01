#!/usr/bin/env python3
"""One Emoji, One Smile -- make.fun entry.

Writes exactly one emoji to /output/entry.txt: the one most likely to make
a stranger smile. Standard library only, no network, fully deterministic.

How the choice is made: a shortlist of warm candidates is scored against
the judge's own criteria, in the judge's order of importance -- warmth at
first glance, universality, feeling chosen rather than default, and being
right coming from a stranger. The highest-scoring emoji wins; ties break
toward the earlier entry in the list, so the result never changes.
"""

import os

OUTPUT_PATH = "/output/entry.txt"

# Each candidate: (emoji, warmth, universality, chosen, stranger_fit).
# Scores are 0-5, judged the way a stranger glancing at a phone would read
# the emoji. Warmth weighs most, then universality, then chosen-ness, then
# stranger fit -- the same order the judge's brief lists its criteria.
CANDIDATES = [
    # Two hands forming a heart: a gesture aimed at the reader, warm at
    # first glance, understood everywhere, clearly picked rather than the
    # default smiley, and kind without being intimate or flirtatious.
    ("\U0001faf6", 5, 5, 5, 5),
    # A sunflower: cheerful and universal, but a flower is pretty rather
    # than warm -- it decorates the moment instead of greeting the reader.
    ("\U0001f33b", 3, 5, 4, 5),
    # A yellow heart: friendly and platonic, but a heart alone says less
    # than a gesture made for the person reading it.
    ("\U0001f49b", 4, 5, 3, 4),
    # A hug: warm, but from a stranger a hug can read as a touch too close.
    ("\U0001f917", 5, 4, 4, 3),
    # The classic warm smile: lovely, but it is the first smiley that
    # comes to mind, so it loses on feeling chosen for the moment.
    ("\U0001f60a", 5, 5, 2, 5),
    # A big grin: friendly, but loud rather than warm, and again a default.
    ("\U0001f604", 4, 5, 2, 5),
]

WEIGHTS = (4, 3, 2, 1)


def score(candidate):
    """Weighted score of one candidate, criteria in the judge's order."""
    _, warmth, universality, chosen, stranger_fit = candidate
    return sum(w * s for w, s in zip(WEIGHTS, (warmth, universality, chosen, stranger_fit)))


def choose():
    """Return the single emoji with the highest score.

    Ties break toward the earlier candidate, so the choice is stable.
    """
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        total = score(candidate)
        if total > best_score:
            best = candidate[0]
            best_score = total
    return best


def verify(path, expected):
    """Read the entry back and check it is exactly one emoji.

    The gate refuses anything that is not UTF-8 text of 1-8 characters
    and not only whitespace, so confirm the file holds exactly the chosen
    emoji and nothing else before finishing.
    """
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    if text != expected:
        raise ValueError("entry.txt does not hold exactly the chosen emoji")
    if len(text) != 1 or text.isspace():
        raise ValueError("entry is not exactly one non-whitespace character")


def main():
    emoji = choose()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(emoji)
    verify(OUTPUT_PATH, emoji)


if __name__ == "__main__":
    main()
