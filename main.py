"""One Star for Monday — single-line review entry generator.

Writes exactly one line of review text to the output directory and
refuses to write anything that breaks the competition gate:
  * UTF-8, exactly one line
  * 1-200 characters
  * at most 25 words
  * not whitespace-only
"""

import os
import sys

REVIEW_LINE = (
    "Waiter sat us by the drafty door, served Monday still half-asleep, "
    "and charged extra for the weekend we just finished."
)

MAX_CHARS = 200
MAX_WORDS = 25


def _check_not_blank(line: str) -> str | None:
    return None if line.strip() else "line is empty or whitespace-only"


def _check_length(line: str) -> str | None:
    if len(line) > MAX_CHARS:
        return f"line is {len(line)} chars, over the {MAX_CHARS} limit"
    return None


def _check_word_count(line: str) -> str | None:
    words = len(line.split())
    if words > MAX_WORDS:
        return f"line has {words} words, over the {MAX_WORDS} limit"
    return None


def _check_single_line(line: str) -> str | None:
    if "\n" in line or "\r" in line:
        return "line must be a single line"
    return None


GATE_CHECKS = (_check_not_blank, _check_length, _check_word_count, _check_single_line)


def check_gate(line: str) -> list[str]:
    """Run every gate validator; return the list of problems found."""
    return [msg for fn in GATE_CHECKS if (msg := fn(line)) is not None]


def resolve_output_dir() -> str:
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def write_entry(line: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return target


def main() -> int:
    out_dir = resolve_output_dir()
    problems = check_gate(REVIEW_LINE)
    if problems:
        for problem in problems:
            print(f"gate failed: {problem}", file=sys.stderr)
        return 1

    target = write_entry(REVIEW_LINE, out_dir)
    print(f"wrote {len(REVIEW_LINE)} chars, {len(REVIEW_LINE.split())} words -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
