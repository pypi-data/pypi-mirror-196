import argparse
from typing import Any

from ._version import __version__
from .cliargs import process_cli_vars
from .engine.render import render
from .engine.unfold import unfold
from .load.file_loader import load_file
from .load.module import load_modules
from .types import Path


def process(data: Any) -> str:
    match data:
        case str():
            return data
        case dict():
            ctx = load_modules(data)
            data2 = unfold(ctx, data)
            return render(data2)
        case _:
            raise ValueError("unexpected input argument")


def _main(input_file: Path, output_file: Path, values_files: list[Path] | None, overrides: list[str] | None) -> None:
    values = process_cli_vars(values_files, overrides)
    data = load_file(input_file, kwargs=values)
    out = "\n\n".join([process(x) for x in data])
    with open(output_file, "w+") as fh:
        fh.write(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("input", type=str, help="path to docker.yml input file")
    parser.add_argument("output", type=str, help="output Dockerfile")
    parser.add_argument("-f", "--file", action="append", type=str, help="values.yml file")
    parser.add_argument("-s", "--set", action="append", type=str, metavar="KEY=VALUE")
    args = parser.parse_args()
    _main(args.input, args.output, args.file, args.set)


main()
