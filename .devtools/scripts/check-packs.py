#!/usr/bin/env python3
"""Validates every datapack under packs/ against the repo conventions.

Usage: check-packs.py [pack ...]   (defaults to every pack)

Checks, per pack:
- layout: kebab-case directory, pack.toml, pack.mcmeta, pack.png, README.md
- namespaces: only the pack's own (directory name in snake_case) and `minecraft`
- every JSON file parses
- an uninstall function exists
- every reference to the pack's own namespace in a function or a tag resolves
to a file, so a rename cannot leave a dangling id behind

It does not validate command syntax; only the game can. See CONTRIBUTING.md.
"""

from __future__ import annotations

import json
import re
import sys

from packs import ROOT, Pack, discover

SLUG = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
SEMVER = re.compile(r"\d+\.\d+\.\d+")
REQUIRED_FILES = ("pack.toml", "pack.mcmeta", "pack.png", "README.md")


def resolves(pack: Pack, ref: str) -> bool:
    """Whether `ns:path` or `#ns:path` names a file in the pack's own namespace."""
    is_tag = ref.startswith("#")
    path = ref.lstrip("#").split(":", 1)[1]
    base = pack.path / "data" / pack.namespace
    pattern = f"tags/*/{path}.json" if is_tag else f"*/{path}.*"
    return any(base.glob(pattern))


def layout_errors(pack: Pack) -> list[str]:
    errors = []
    if not SLUG.fullmatch(pack.slug):
        errors.append(f"directory name '{pack.slug}' is not kebab-case")
    errors += [f"missing {name}" for name in REQUIRED_FILES if not (pack.path / name).is_file()]
    return errors


def metadata_errors(pack: Pack) -> list[str]:
    meta = pack.meta
    errors = [
        f"pack.toml: '{key}' must be a non-empty string"
        for key in ("name", "version", "minecraft")
        if not isinstance(meta.get(key), str) or not meta[key]
    ]
    version = meta.get("version")
    if isinstance(version, str) and not SEMVER.fullmatch(version):
        errors.append(f"pack.toml: version '{version}' is not MAJOR.MINOR.PATCH")
    return errors


def namespace_errors(pack: Pack) -> list[str]:
    data = pack.path / "data"
    namespaces = {p.name for p in data.iterdir() if p.is_dir()} if data.is_dir() else set()
    errors = []
    if pack.namespace not in namespaces:
        errors.append(f"missing own namespace data/{pack.namespace}/")
    for extra in sorted(namespaces - {pack.namespace, "minecraft"}):
        errors.append(f"foreign namespace data/{extra}/ (allowed: {pack.namespace}, minecraft)")
    return errors


def json_errors(pack: Pack) -> list[str]:
    errors = []
    for path in sorted([pack.path / "pack.mcmeta", *(pack.path / "data").rglob("*.json")]):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except ValueError as error:
            errors.append(f"{path.relative_to(pack.path)}: invalid JSON ({error})")
    return errors


def uninstall_errors(pack: Pack) -> list[str]:
    if (pack.path / "data" / pack.namespace / "function" / "uninstall.mcfunction").is_file():
        return []
    return [f"missing data/{pack.namespace}/function/uninstall.mcfunction"]


def reference_errors(pack: Pack) -> list[str]:
    data = pack.path / "data"
    own_ref = re.compile(rf"#?{re.escape(pack.namespace)}:[a-z0-9_./-]+")
    sources = sorted([*data.rglob("*.mcfunction"), *data.glob("*/tags/**/*.json")])
    errors = []
    for path in sources:
        for ref in sorted(set(own_ref.findall(path.read_text(encoding="utf-8")))):
            if not resolves(pack, ref):
                errors.append(f"{path.relative_to(pack.path)}: '{ref}' does not resolve to a file")
    return errors


def check(pack: Pack) -> list[str]:
    errors = layout_errors(pack)
    if errors:
        return errors
    return (
        metadata_errors(pack)
        + namespace_errors(pack)
        + json_errors(pack)
        + uninstall_errors(pack)
        + reference_errors(pack)
    )


if __name__ == "__main__":
    failed = False
    for pack in discover(sys.argv[1:]):
        errors = check(pack)
        failed |= bool(errors)
        print(f"{'✖' if errors else '✔'} {pack.path.relative_to(ROOT)}")
        for error in errors:
            print(f"    {error}")
    sys.exit(1 if failed else 0)
