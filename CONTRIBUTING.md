# Contributing

Thanks for helping! This project follows a few strict conventions, and tooling enforces them.

## Setup

1. Install **[mise](https://mise.jdx.dev/getting-started.html)** (`brew install mise`). It installs
   every other tool, Python included, at the version `mise.toml` pins.
2. Run `make -C .devtools setup`. This installs the pinned tools and the `pre-commit`, `commit-msg`
   and `pre-push` hooks, which [lefthook](https://lefthook.dev/) runs.
3. Run `make -C .devtools check` to confirm everything passes.

`make -C .devtools help` lists all targets.

## Project layout

| Path | Purpose |
| --- | --- |
| `packs/<slug>/` | One datapack. `<slug>` is kebab-case and is also the release component. |
| `packs/<slug>/pack.toml` | Release metadata: display name, version, target Minecraft version |
| `packs/<slug>/pack.mcmeta`, `pack.png`, `data/` | The datapack itself. Only these ship in the zip, plus `LICENSE`. |
| `packs/<slug>/README.md` | Player-facing docs, reused for the download page |
| `.devtools/` | Makefile, shared `base.mk`, the shared hooks (`lefthook-base.yml`), build, check and guard scripts |
| `mise.toml`, `mise.lock` | Every tool the hooks and CI run, pinned with checksums |
| `lefthook.yml` | This project's own hooks, on top of the shared ones |
| `dist/` | Build output. Ignored by git. |

## Adding a pack

1. Create `packs/<slug>/` with `pack.toml`, `pack.mcmeta`, `pack.png`, `README.md` and
   `data/<namespace>/`, where `<namespace>` is the slug in snake_case.
2. Add an `uninstall` function that undoes everything the pack leaves in a world.
3. Register it in `release-please-config.json` and `.release-please-manifest.json`, copying the
   `cauldron-copper` entries, and add it to the catalog in the root `README.md` and to the
   bug-report template.
4. `make -C .devtools check`.

## Testing

`make -C .devtools validate` checks layout, namespaces, JSON and that every id a pack refers to
exists. It cannot check command syntax; only the game can. Before opening a PR:

1. `make -C .devtools build PACK=<slug>` and copy the zip from `dist/` into a test world's
   `datapacks` folder.
2. `/reload` and read the log: a function that fails to parse is reported there and nowhere else.
3. Exercise the feature, then run `/function <namespace>:uninstall` and confirm it stops.

<!-- >>> template:workflow -->
## Workflow

### Branches: [Conventional Branch](https://conventionalbranch.org/)

`<type>/<description>`, lowercase, with single hyphens. Types: `feature`/`feat`, `bugfix`/`fix`,
`hotfix`, `release`, `chore`, plus `claude`/`codex`/`ai` for agent-authored work.
Examples: `feat/short-description`, `fix/what-was-broken`.

### Commits: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

`<type>(<scope>): <summary>`. Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`,
`test`, `build`, `ci`, `chore`, `revert`. Breaking changes use `!` or a `BREAKING CHANGE:` footer.
The scopes this project uses are listed in `AGENTS.md` and enforced from `.commitlintrc.yaml`:
a scope is optional, but one that is not listed is rejected. The rest is
[commitlint's conventional config](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional):
a lowercase subject with no full stop, and at most 100 characters in the header and in each
body line.

PRs are **squash-merged**, so the **PR title** must also be a Conventional Commit.
It becomes the commit on `main` that release-please reads.

### Pull requests: at most 20 files

Keep every PR to **20 changed files or fewer**. Split larger work into a **stack**:

```sh
gh extension install github/gh-stack   # once
gh stack init feat/first-slice         # start a stack from main
# ...commit...
gh stack add feat/second-slice         # next layer on top
gh stack submit                        # push all layers and open linked PRs
gh stack sync                          # after a lower layer merges
```

Each layer is measured against the layer below it. The limit is enforced in the `pre-push` hook,
in CI, and for AI agents through a PreToolUse hook (`.devtools/scripts/agent-guard.sh`).

### Files the template manages

Some files, and the regions of others between `>>> template:<name>` and `<<< template:<name>`
markers, are kept in step with `studiobimo/project-template`. Change them there, not here; then
`make -C .devtools sync` brings the change in. `make -C .devtools drift` shows what differs, and a
weekly workflow opens an issue when something does. A deliberate difference goes in
`.template-ignore`, with a comment saying why.
<!-- <<< template:workflow -->

### One pack per pull request

Scopes are a pack's slug (`cauldron-copper`), or `build`, `ci`, `docs`, `deps`, `devtools`.
release-please assigns a commit to a pack by the files it touches, so keep a PR to one pack.
Example branches: `feat/cauldron-copper-tools`, `fix/waxed-chests`.

## Pack standards

- **Namespaces:** a pack writes to its own namespace and, for tags only, to `minecraft`.
- **Original work only:** nothing copied from third-party packs: no functions, assets,
  namespaces, names or branding.
- **Clean uninstall:** `<namespace>:uninstall` leaves nothing scheduled or stored in the world.
- **Light on the server:** prefer a scheduled loop at the slowest interval that feels instant
  over per-tick work.
- **Formatting:** 2-space JSON, fully namespaced ids, a comment header on every function.

## Porting to a new Minecraft version

1. Update `minecraft` in the pack's `pack.toml` and the format range in its `pack.mcmeta`, using
   the pack format from that release's changelog.
2. Check the changelog for renamed commands, components and ids, and for new blocks or items the
   pack should cover.
3. Test in a world on that version, then land it as `feat(<slug>): support Minecraft <version>`.

## Releases

[release-please](https://github.com/googleapis/release-please) maintains one release PR per pack
from the Conventional Commits on `main`. Merging it tags `<slug>-v<version>`, cuts the GitHub
Release, and the release workflow attaches `<slug>-<version>+mc<minecraft>.zip`. Never edit a
version by hand.

## Repository settings (maintainers)

`main` is protected by org rulesets: PRs required, squash-only, linear history, and required
checks `pr-checks` and `lint`.
