"""Micro-confession entry for "Unsent: The Micro-Confession Sprint".

Writes the two-line entry to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt if set), with no trailing newline.
"""

import os
import sys

# Why this confession: it admits a small, specific cruelty (letting the
# phone ring on purpose) with no plea for forgiveness, and the twist —
# he was learning to leave me alone — makes the "To: Dad" line
# irreplaceable. No other recipient carries the same sting.
ENTRY = (
    "To: Dad\n"
    "I saw your call. I let it ring because I wanted you to try twice. "
    "I didn't know you were learning to leave me alone."
)

MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200


def validate(entry: str) -> str | None:
    """Return an error message if the entry is invalid, else None.

    The entry must be exactly two lines: a "To: <recipient>" address line
    followed by the confession itself. A missing "To: " prefix means the
    two-part format is broken, so it fails the gate instead of passing
    as a one-part text.
    """
    if not entry or not entry.strip():
        return "entry is empty or whitespace-only"
    if len(entry) > MAX_TOTAL_CHARS:
        return f"entry is {len(entry)} chars, over the {MAX_TOTAL_CHARS} cap"
    if "\r" in entry:
        return "entry contains a carriage return"
    lines = entry.split("\n")
    if len(lines) != 2:
        return f"entry must be exactly 2 lines, got {len(lines)}"
    if not lines[0].startswith("To: "):
        return 'first line must start with "To: " (address line missing)'
    if any("\n" in line or "\r" in line for line in lines):
        return "a line contains a line break"
    if len(lines[1]) > MAX_MESSAGE_CHARS:
        return (
            f"message line is {len(lines[1])} chars, "
            f"over the {MAX_MESSAGE_CHARS} cap"
        )
    return None


def main() -> int:
    error = validate(ENTRY)
    if error:
        print(f"invalid entry: {error}", file=sys.stderr)
        return 2
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(f"wrote {path} ({len(ENTRY)} chars, 2 lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
