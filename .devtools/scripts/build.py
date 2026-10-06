#!/usr/bin/env python3
"""Packages each datapack into dist/<slug>-<version>+mc<minecraft>.zip.

Usage: build.py [pack ...]   (defaults to every pack)

Archives are reproducible: entries are sorted and carry a fixed timestamp and
mode, so the same sources always produce the same bytes. Only what the game
reads ships (pack.mcmeta, pack.png, data/), plus the license.
"""

from __future__ import annotations

import sys
import zipfile

from packs import DIST_DIR, ROOT, Pack, discover

EPOCH = (1980, 1, 1, 0, 0, 0)
SHIPPED = ("pack.mcmeta", "pack.png", "data")


def shipped_files(pack: Pack) -> list[tuple[str, bytes]]:
    files = []
    for name in SHIPPED:
        source = pack.path / name
        paths = sorted(p for p in source.rglob("*") if p.is_file()) if source.is_dir() else [source]
        for path in paths:
            if any(part.startswith(".") for part in path.relative_to(pack.path).parts):
                continue
            files.append((path.relative_to(pack.path).as_posix(), path.read_bytes()))
    files.append(("LICENSE", (ROOT / "LICENSE").read_bytes()))
    return files


def build(pack: Pack) -> None:
    DIST_DIR.mkdir(exist_ok=True)
    target = DIST_DIR / pack.archive_name
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in shipped_files(pack):
            info = zipfile.ZipInfo(name, date_time=EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    print(f"✔ {target.relative_to(ROOT)}")


if __name__ == "__main__":
    for pack in discover(sys.argv[1:]):
        build(pack)
