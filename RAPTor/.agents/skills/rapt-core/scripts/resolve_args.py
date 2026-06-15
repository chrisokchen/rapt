#!/usr/bin/env python3
"""解析 `.raptor/arguments.yml` 的輕量工具。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


EXIT_ARGUMENTS_NOT_FOUND = 2
EXIT_SCHEMA_UNSUPPORTED = 3
EXIT_KEY_MISSING = 4


def _strip_comment(line: str) -> str:
    in_quote = False
    quote = ""
    for index, char in enumerate(line):
        if char in {"'", '"'}:
            if not in_quote:
                in_quote = True
                quote = char
            elif quote == char:
                in_quote = False
        if char == "#" and not in_quote:
            return line[:index]
    return line


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in text.splitlines():
        line = _strip_comment(raw_line).rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("- "):
            raise ValueError("list syntax is not supported in arguments.yml")
        indent = len(line) - len(line.lstrip(" "))
        if ":" not in line:
            raise ValueError(f"invalid mapping line: {raw_line}")
        key, value = line.strip().split(":", 1)
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"invalid indentation: {raw_line}")
        parent = stack[-1][1]
        if value.strip() == "":
            child: dict[str, Any] = {}
            parent[key.strip()] = child
            stack.append((indent, child))
        else:
            parent[key.strip()] = _parse_scalar(value)
    return root


def get_nested(data: dict[str, Any], dotted_key: str) -> Any:
    current: Any = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted_key)
        current = current[part]
    return current


def normalize_value(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return ""
    return str(value)


def read_keys(args: argparse.Namespace) -> list[str]:
    keys = list(args.key or [])
    if not sys.stdin.isatty():
        keys.extend(line.strip() for line in sys.stdin if line.strip())
    return keys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="專案根目錄，預設目前工作目錄")
    parser.add_argument("--file", default=".raptor/arguments.yml")
    parser.add_argument("--key", action="append", help="要解析的 dotted key，可重複")
    parser.add_argument("--strict-v2", action="store_true", help="要求 arguments_schema_version: 2")
    args = parser.parse_args(argv)

    arguments_path = Path(args.root) / args.file
    if not arguments_path.exists():
        print(f"ERROR arguments.yml not found: {arguments_path}", file=sys.stderr)
        return EXIT_ARGUMENTS_NOT_FOUND

    try:
        data = parse_simple_yaml(arguments_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"ERROR cannot parse arguments.yml: {exc}", file=sys.stderr)
        return EXIT_SCHEMA_UNSUPPORTED

    schema_version = data.get("arguments_schema_version", 1)
    if args.strict_v2 and str(schema_version) != "2":
        print("ERROR arguments_schema_version is not 2", file=sys.stderr)
        return EXIT_SCHEMA_UNSUPPORTED

    keys = read_keys(args)
    if not keys:
        print("ERROR no key provided", file=sys.stderr)
        return EXIT_KEY_MISSING

    missing: list[str] = []
    for key in keys:
        try:
            print(f"{key}={normalize_value(get_nested(data, key))}")
        except KeyError:
            missing.append(key)
    if missing:
        print("ERROR missing keys: " + ", ".join(missing), file=sys.stderr)
        return EXIT_KEY_MISSING
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
