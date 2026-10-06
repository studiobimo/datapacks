<!-- markdownlint-disable-file MD041 -->
## What & why

<!-- One or two sentences. Link issues with "Closes #123". -->

## Checklist

- [ ] PR title is a [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) (it becomes the squash commit)
- [ ] ≤20 files changed (otherwise split with `gh stack`)
- [ ] `make -C .devtools check` passes locally
- [ ] Tested in game on the Minecraft version in `pack.toml`: `/reload` is clean, the feature works, `uninstall` works
- [ ] Only the pack's own namespace and `minecraft` are used; nothing copied from third-party packs
- [ ] The pack's README is updated if behavior changed
