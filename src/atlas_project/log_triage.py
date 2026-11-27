"""Lab 1: Log Triage CLI."""

import argparse
from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path


def read_lines(path: Path) -> Iterator[str]:
    """Yield lines lazily, without trailing newlines."""
    with path.open(encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def parse(line: str) -> dict[str, str] | None:
    """Parse one log line; return None if it is malformed."""
    match line.split(maxsplit=3):
        case [_, _, "ERROR", rest]:
            code, _, msg = rest.partition(" ")
            return {"level": "ERROR", "code": code, "msg": msg}
        case [_, _, "WARN" | "INFO" as level, msg]:
            return {"level": level, "msg": msg}
        case _:
            return None


def top_codes(codes: Iterable[str], n: int = 5) -> list[tuple[str, int]]:
    """Rank codes by frequency, most common first."""
    return Counter(codes).most_common(n)


def triage(path: Path, top: int = 10) -> list[tuple[str, int]]:
    """One pass: read, de-duplicate, parse, count ERROR codes."""
    seen: set[str] = set()
    counts: Counter[str] = Counter()
    for line in read_lines(path):
        if line in seen:
            continue
        seen.add(line)
        if (p := parse(line)) and p["level"] == "ERROR":
            counts[p["code"]] += 1
    return counts.most_common(top)


def format_report(rows: list[tuple[str, int]]) -> str:
    """Aligned report: code, count and share of the total."""
    total = sum(n for _, n in rows) or 1
    header = f"{'CODE':<8}{'COUNT':>8}{'SHARE':>8}"
    body = [f"{code:<8}{n:>8,}{n / total:>8.1%}" for code, n in rows]
    return "\n".join([header, *body])


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="triage")
    p.add_argument("path", type=Path, nargs="?", default=Path("support.log"))
    p.add_argument("--top", type=int, default=10)
    args = p.parse_args(argv)
    print(format_report(triage(args.path, args.top)))


if __name__ == "__main__":
    main()