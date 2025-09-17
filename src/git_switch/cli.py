#!/usr/bin/env python3
import argparse
import sys
from typing import List, Optional

from .ssh_manager import build_ssh_subparser, handle_ssh_command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="git-switch", description="Developer utilities")
    subparsers = parser.add_subparsers(dest="command", required=False)

    # SSH manager
    build_ssh_subparser(subparsers)

    # Default action prints greeting
    parser.set_defaults(func=lambda _args: (print("Hello from git-switch 👋") or 0))
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "command", None) == "ssh":
        return handle_ssh_command(args)
    func = getattr(args, "func", None)
    if callable(func):
        return int(func(args))
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
