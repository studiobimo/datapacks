# Agent guide: Datapacks

Instructions for AI coding agents (Codex, Claude Code, and others) working in this repo.

## Project

Studio Bimo's vanilla Minecraft: Java Edition datapacks, one per directory under `packs/`.
No mods, no resource packs, no build step beyond zipping.

- Catalog and install instructions: `README.md`
- Player-facing docs for a pack: `packs/<slug>/README.md`
- Workflow and conventions in full: `CONTRIBUTING.md`
- Commit scopes: a pack's slug (`cauldron-copper`), or `build`, `ci`, `docs`, `deps`, `devtools`

## Layout

```text
packs/<slug>/            one datapack; <slug> is kebab-case
  pack.toml              release metadata: name, version, minecraft
  pack.mcmeta            what the game reads: description and pack format
  pack.png               icon
  README.md              player-facing docs
  data/<namespace>/      the pack's own content; <namespace> is <slug> in snake_case
  data/minecraft/tags/   only to hook into vanilla tags (load, tick)
.devtools/               Makefile (project targets), base.mk (shared targets), pinned Python tools
  scripts/               build.py, check-packs.py, agent-guard.sh, template-sync.sh
dist/                    build output, ignored
```

<!-- >>> template:rules -->
## Non-negotiables

These hold in every studiobimo repo. Git hooks, CI and an agent hook all enforce them, so a
violation is caught before it is reviewed.

- **Commits:** [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/),
  `<type>(<scope>): <summary>`. PRs are squash-merged, so the **PR title** must be one too.
- **Branches:** [Conventional Branch](https://conventionalbranch.org/), `<type>/<description>`
  in lowercase with single hyphens, e.g. `feat/short-description`. Agents may use `claude/…` or
  `codex/…`.
- **PR size:** at most 20 changed files. Split bigger work with `gh stack`
  (`gh stack init`, `gh stack add`, `gh stack submit`).
- **Versioning:** SemVer, managed by release-please. Never edit a version, a
  `.release-please-manifest.json` or a `CHANGELOG.md` by hand.
- **Pinning:** third-party GitHub Actions and pre-commit hooks are pinned to full commit SHAs with
  the version in a comment; studiobimo's own reusable workflows are called at `@v1`. Python tools
  are locked in `.devtools/uv.lock`.
- **Workflows:** `permissions: {}` at the top, the minimum per job, `persist-credentials: false`
  on every checkout, secrets passed explicitly and never with `secrets: inherit`.
- **Say what you tested.** State what you ran and what it showed. If something could not be
  tested, say so plainly rather than implying it was.

A PreToolUse hook (`.devtools/scripts/agent-guard.sh`) blocks `gh pr create`, `gh stack submit`
and `git push` when the PR-size rule is violated, and blocks non-conventional branch names.

## Where shared things live

Some files here are not this repo's to edit. Changing them locally only creates drift, which a
weekly workflow reports as an issue.

| To change | Edit it in | It reaches this repo by |
| --- | --- | --- |
| CI behaviour (lint, PR checks, release) | `studiobimo/.github`, `.github/workflows/` | the `@v1` tag moving |
| Commit, branch and PR-size rules | `studiobimo/.github`, `.devtools/` | a `rev:` bump in `.pre-commit-config.yaml` |
| Files and blocks listed in the template's `.template/manifest` | `studiobimo/project-template` | `make -C .devtools sync` |

A managed block sits between `>>> template:<name>` and `<<< template:<name>` marker lines, like
this section. Edit outside the markers freely; inside them, change the template instead. If a
difference is deliberate, list the path in `.template-ignore` with a comment saying why.
<!-- <<< template:rules -->

## Pack rules

- **Versioning is per pack.** release-please owns `version` in every `pack.toml`; one release
  PR and one tag (`<slug>-v<version>`) per pack.
- **Namespaces:** a pack writes only to its own namespace and, for tags, to `minecraft`.
  It never ships another project's namespace.
- **Original work only:** never copy functions, assets, names or branding from third-party
  packs. Reimplement the idea from the vanilla command reference.
- **Clean uninstall:** every pack has `<namespace>:uninstall`, which removes everything the pack
  left in the world (schedules, scoreboards, storage, entities).
- **Build output stays out of git:** zips are built into `dist/` and attached to releases.

## Commands

```sh
make -C .devtools setup      # once: pinned tools + git hooks
make -C .devtools check      # everything CI runs (lint + validate), plus a build
make -C .devtools validate   # pack layout, namespaces, JSON and references only
make -C .devtools build      # zip every pack into dist/ (PACK=<slug> for one)
make -C .devtools lock       # after changing a tool version in .devtools/pyproject.toml
make -C .devtools drift      # where this repo differs from studiobimo/project-template
make -C .devtools sync       # pull the template's managed files
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
