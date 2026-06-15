#!/usr/bin/env python3
"""偵測 SSoT 變更是否尚未被 rapt-human-sync 登錄。

此工具只讀取 git diff 與 HSYNC fingerprint，不寫任何檔案。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import human_sync_scan as hsync


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--baseline")
    parser.add_argument("--mode", choices=["auto", "committed", "working_tree", "mixed"], default="auto")
    parser.add_argument("--output-dir", default=".raptor/human-sync")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    try:
        arguments = hsync.load_arguments(root)
        baseline = hsync.resolve_baseline(root, args.baseline)
        paths = hsync.ssot_paths(arguments)
        mode, raw_changes, _dirty = hsync.collect_changes(root, baseline, args.mode, paths)
        existing = hsync.existing_fingerprints(root / args.output_dir)
        operator = {"name": "detect_unsynced", "source": "tool"}
        records, skipped = hsync.build_records(root, arguments, baseline, mode, operator, "", raw_changes, existing)
    except FileNotFoundError as exc:
        print(f"ERROR arguments.yml not found: {exc}", file=sys.stderr)
        return hsync.EXIT_ARGUMENTS_NOT_FOUND
    except (LookupError, RuntimeError) as exc:
        print(f"ERROR cannot inspect unsynced changes: {exc}", file=sys.stderr)
        return hsync.EXIT_GIT_ERROR

    if records:
        print(f"UNSYNCED {len(records)} SSoT change(s) are not covered by HSYNC records.")
        print("建議先執行 /rapt-human-sync，再執行 /rapt-verify。")
        for record in records:
            print(f"- {record.file} ({record.change_type}, {record.dsl})")
        return 1
    if raw_changes:
        print(f"OK all {skipped} SSoT change(s) are covered by existing HSYNC records.")
    else:
        print("OK no SSoT changes detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

