#!/usr/bin/env python3
"""將 RAPTor v1 docs layout 規劃為 v2 layout。"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DIR_MAP = {
    "docs/01-discovery": "docs/discovery",
    "docs/02-data-model": "docs/ssot/dbml",
    "docs/03-access-control": "docs/ssot/haarm",
    "docs/04-features": "docs/ssot/habdd",
    "docs/05-backend-intent": "docs/ssot/haapi",
    "docs/06-frontend-intent": "docs/ssot/hapdl",
    "docs/06-openapi": "docs/generate/openapi",
    "docs/07-lofi-preview": "docs/generate/lofi",
    "docs/08-design-brief": "docs/generate/designbrief",
}

CREATE_DIRS = [
    "docs/ssot/dbml",
    "docs/ssot/habdd",
    "docs/ssot/haarm",
    "docs/ssot/haapi",
    "docs/ssot/hapdl",
    "docs/generate/pdl",
    "docs/generate/isabdd",
    "docs/generate/openapi",
    "docs/generate/lofi",
    "docs/generate/designbrief",
    "docs/discovery",
    "docs/reports",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = Path(args.root)
    print("# RAPTor docs layout v1 -> v2 migration plan")
    for rel in CREATE_DIRS:
        target = root / rel
        print(f"MKDIR {target}")
        if args.apply:
            target.mkdir(parents=True, exist_ok=True)
    for old_rel, new_rel in DIR_MAP.items():
        old = root / old_rel
        new = root / new_rel
        if old.exists():
            print(f"MOVE {old} -> {new}")
            if args.apply:
                new.parent.mkdir(parents=True, exist_ok=True)
                if new.exists():
                    print(f"SKIP target exists: {new}")
                else:
                    shutil.move(str(old), str(new))
        else:
            print(f"SKIP missing {old}")
    print("NOTE update .raptor/arguments.yml to arguments_schema_version: 2 after review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
