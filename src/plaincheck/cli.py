"""Command-line interface."""

import argparse
from pathlib import Path

from .checker import analyze, load_rules
from .reporting import write_reports


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check a local text file with transparent rules")
    parser.add_argument("text_file")
    parser.add_argument("--rules", default="config/rules.json")
    parser.add_argument("--output", default="reports")
    args = parser.parse_args(argv)
    result = analyze(Path(args.text_file).read_text(encoding="utf-8"), load_rules(args.rules))
    write_reports(result, args.output)
    print(f"Reviewed {result['metrics']['words']} words; found {len(result['findings'])} prompts.")
    print("Source text was not copied into the reports.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

