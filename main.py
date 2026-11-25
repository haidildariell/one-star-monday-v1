#!/usr/bin/env python3
"""One Star for Monday - writes a one-star review of Monday as a restaurant.

The entry is a single plain-text line (max 25 words, 1-180 characters) written
to /output/entry.txt, or to $MAKEFUN_OUTPUT_DIR/entry.txt when that variable
is set. The program self-checks the gate limits and fails hard if the line
is outside them.
"""

import os
import sys

LINE = (
    "Waiter sat us by the drafty door, served Monday still half-asleep, "
    "and charged extra for the weekend we just finished."
)


def main() -> int:
    words = LINE.split()
    if not 1 <= len(LINE) <= 180:
        print(f"FAIL: entry is {len(LINE)} chars, must be 1-180", file=sys.stderr)
        return 1
    if len(words) > 25:
        print(f"FAIL: entry is {len(words)} words, must be <= 25", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("FAIL: entry is blank", file=sys.stderr)
        return 1
    if "\n" in LINE:
        print("FAIL: entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)

    print(f"OK: wrote {len(LINE)} chars, {len(words)} words to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
