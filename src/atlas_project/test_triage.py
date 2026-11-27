from pathlib import Path

import pytest

from atlas_project.log_triage import format_report, parse, top_codes, triage


@pytest.fixture
def sample_log(tmp_path: Path) -> Path:
    path = tmp_path / "support.log"
    path.write_text(
        "2026-11-20 09:00:01 ERROR E1042 Disk full\n"
        "2026-11-20 09:00:01 ERROR E1042 Disk full\n"
        "2026-11-20 09:00:02 INFO started\n"
        "garbage line\n"
    )
    return path


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("2026-11-20 09:00:01 ERROR E1042 Disk full", "E1042"),
        ("2026-11-20 09:00:01 ERROR E2001 Timeout", "E2001"),
        ("2026-11-20 09:00:01 INFO started", None),
        ("", None),
    ],
    ids=["disk", "timeout", "info", "empty"],
)
def test_parse_code(line, expected):
    assert (parse(line) or {}).get("code") == expected


def test_ranks_most_common_first():
    assert top_codes(["E1", "E2", "E1"]) == [("E1", 2), ("E2", 1)]


def test_empty_input_gives_empty_list():
    assert top_codes([]) == []


def test_skips_malformed_and_duplicate_lines(sample_log):
    assert triage(sample_log) == [("E1042", 1)]


def test_report_is_aligned():
    report = format_report([("E1042", 3), ("E2001", 1)])
    assert report.splitlines()[1] == "E1042          3   75.0%"