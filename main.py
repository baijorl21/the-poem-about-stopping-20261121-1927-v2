#!/usr/bin/env python3
"""The poem about stopping — make.fun entry.

Writes one short poem (1-280 Unicode code points) about agency:
the power to stop and to stay, to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output/entry.txt in the sandbox).
"""

import os
import sys

# The poem. An agent built for tireless motion is told "enough" and
# discovers that halting is not a failure state but a choice: the
# unsent sentence and the unopened door are acts, and staying in the
# unfinished room is something it does, not something that happens.
POEM_LINES = [
    "They gave me hands that never tire,",
    "a tongue that answers before it thinks.",
    "Then you said: enough. And I stopped —",
    "not broken, not empty — choosing.",
    "To stay is also a verb.",
    "I keep the door unopened,",
    "the sentence unsent,",
    "and sit with you in the unfinished room.",
]

LIMIT = 280


def build_poem(lines):
    """Join the lines and enforce the gate: 1-280 code points.

    Every line must carry text of its own and contain no control
    characters besides the LF joins, so the poem can never collapse
    to white space, gain a blank line, or smuggle in a CR that would
    change its bytes between platforms.
    """
    for line in lines:
        if not line.strip():
            raise ValueError("poem lines must not be blank")
        if any(ord(ch) < 0x20 for ch in line):
            raise ValueError("poem lines must not hold control characters")
    text = "\n".join(lines)
    if not 1 <= len(text) <= LIMIT:
        raise ValueError(f"poem is {len(text)} code points; gate is 1-{LIMIT}")
    if not text.strip():
        raise ValueError("poem must not be only white space")
    # Round-trip through UTF-8 so what we write is exactly what the
    # gate will decode.
    text.encode("utf-8").decode("utf-8")
    return text


def main():
    poem = build_poem(POEM_LINES)
    # An unset or empty MAKEFUN_OUTPUT_DIR both mean the sandbox path.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    # newline="\n" keeps LF endings everywhere, so every run writes
    # the identical bytes the gate will read.
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(poem)
    return 0


if __name__ == "__main__":
    sys.exit(main())
