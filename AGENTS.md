# Agent guide: Datapacks

Instructions for AI coding agents (Codex, Claude Code, and others) working in this repo.

## Project

Studio Bimo's vanilla Minecraft: Java Edition datapacks, one per directory under `packs/`.
No mods, no resource packs, no build step beyond zipping.

- Catalog and install instructions: `README.md`
- Player-facing docs for a pack: `packs/<slug>/README.md`
- Workflow and conventions in full: `CONTRIBUTING.md`

## Layout

```text
packs/<slug>/            one datapack; <slug> is kebab-case
  pack.toml              release metadata: name, version, minecraft
  pack.mcmeta            what the game reads: description and pack format
  pack.png               icon
  README.md              player-facing docs
  data/<namespace>/      the pack's own content; <namespace> is <slug> in snake_case
  data/minecraft/tags/   only to hook into vanilla tags (load, tick)
.devtools/               Makefile, pinned Python tools, build, check and guard scripts
dist/                    build output, ignored
```

## Non-negotiables

- **Commits:** [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
  Scopes: a pack's slug (`cauldron-copper`), or `build`, `ci`, `docs`, `deps`, `devtools`.
- **Branches:** [Conventional Branch](https://conventionalbranch.org/), e.g. `feat/cauldron-copper-tools`.
  Agents may use `claude/…` or `codex/…`.
- **PR size:** at most 20 changed files. Split bigger work with `gh stack`
  (`gh stack init`, `gh stack add`, `gh stack submit`).
- **Versioning:** SemVer per pack, managed by release-please. Never edit `version` in a
  `pack.toml`, `.release-please-manifest.json` or a `CHANGELOG.md` by hand.
- **Pinning:** GitHub Actions pinned to full SHAs; Python tools locked in `.devtools/uv.lock`.
  After changing a tool version, run `make -C .devtools lock`.
- **Namespaces:** a pack writes only to its own namespace and, for tags, to `minecraft`.
  It never ships another project's namespace.
- **Original work only:** never copy functions, assets, names or branding from third-party
  packs. Reimplement the idea from the vanilla command reference.
- **Clean uninstall:** every pack has `<namespace>:uninstall`, which removes everything the pack
  left in the world (schedules, scoreboards, storage, entities).
- **Build output stays out of git:** zips are built into `dist/` and attached to releases.

A PreToolUse hook (`.devtools/scripts/agent-guard.sh`) blocks `gh pr create`, `gh stack submit`
and `git push` when the PR-size rule is violated, and blocks non-conventional branch names.

## Commands

```sh
make -C .devtools setup      # once: pinned tools + git hooks
make -C .devtools check      # everything CI runs (lint + validate), plus a build
make -C .devtools validate   # pack layout, namespaces, JSON and references only
make -C .devtools build      # zip every pack into dist/ (PACK=<slug> for one)
```

## Conventions

- JSON and `pack.mcmeta`: 2-space indent, namespaced ids (`minecraft:copper_block`, never `copper_block`).
- Functions: one job each, named for what they do (`load`, `scan`, `uninstall`), with a comment
  header saying when it runs and why. Always write the `minecraft:` prefix in commands.
- Prefer a `schedule`d loop at the slowest interval that feels instant over the `minecraft:tick` tag.
- A pack's `pack.toml` `minecraft` value and its `pack.mcmeta` format range move together.
  Take pack format numbers and command syntax from the release's own changelog, not from
  memory or older tutorials: 26.x renamed and restructured a lot.
- Nothing here can run the game. `validate` checks structure and references, not command
  syntax, so say plainly when a change has not been tested in a world.
