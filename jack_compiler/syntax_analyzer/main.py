from argparse import ArgumentParser
from pathlib import Path
import sys


def get_jack_files(input_path: Path) -> list[Path]:
    if input_path.is_dir():
        files = list(input_path.glob("*.jack"))
        if not files:
            print(f"Error: no .jack files found in '{input_path}'", file=sys.stderr)
            sys.exit(1)
        return files
    if input_path.suffix != ".jack":
        print(f"Error: '{input_path}' is not a .jack file", file=sys.stderr)
        sys.exit(1)
    return [input_path]


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

    for jack_file in get_jack_files(args.input):
        analyze(jack_file)


if __name__ == "__main__":
    main()


