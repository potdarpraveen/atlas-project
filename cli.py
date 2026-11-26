import argparse
from importlib.metadata import version


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="atlas")
    p.add_argument(
        "--version",
        action="version",
        version=f"atlas {version('atlas')}",
    )
    p.parse_args(argv)