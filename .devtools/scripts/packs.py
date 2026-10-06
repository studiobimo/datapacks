"""Pack discovery and metadata shared by build.py and check-packs.py."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKS_DIR = ROOT / "packs"
DIST_DIR = ROOT / "dist"


@dataclass(frozen=True)
class Pack:
    path: Path

    @property
    def slug(self) -> str:
        """Directory name, e.g. cauldron-copper."""
        return self.path.name

    @property
    def namespace(self) -> str:
        """The pack's own data namespace, e.g. cauldron_copper."""
        return self.slug.replace("-", "_")

    @property
    def meta(self) -> dict:
        return tomllib.loads((self.path / "pack.toml").read_text(encoding="utf-8"))

    @property
    def archive_name(self) -> str:
        meta = self.meta
        return f"{self.slug}-{meta['version']}+mc{meta['minecraft']}.zip"


def discover(names: list[str] | None = None) -> list[Pack]:
    """Every directory under packs/, or only the named ones."""
    packs = [Pack(p) for p in sorted(PACKS_DIR.iterdir()) if p.is_dir()]
    if not names:
        return packs
    known = {p.slug: p for p in packs}
    if missing := [n for n in names if n not in known]:
        raise SystemExit(f"unknown pack(s): {', '.join(missing)} (have: {', '.join(known)})")
    return [known[n] for n in names]
