from argparse import ArgumentParser
from pathlib import Path
import sys

from jack_compiler.syntax_analyzer.jack_analyzer import JackAnalyser


def analyze(jack_file: Path) -> None:
    source = jack_file.read_text()
    # TODO: tokenize and parse
    print(f"Analyzing {jack_file.name} ({len(source)} chars)")
    print(source)


def main():
    parser = ArgumentParser(
        description="Analyze Jack source code and produce XML output representing the syntax structure"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input .jack file or directory containing .jack files",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: '{args.input}' does not exist", file=sys.stderr)
        sys.exit(1)

    analyzer = JackAnalyser(args.input)
    analyzer.run(only_tokens=True)


if __name__ == "__main__":
    main()
