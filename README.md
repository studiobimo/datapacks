# Studio Bimo Datapacks

[![Lint](https://github.com/studiobimo/datapacks/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/studiobimo/datapacks/actions/workflows/lint.yml)
[![Release](https://github.com/studiobimo/datapacks/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/studiobimo/datapacks/actions/workflows/release.yml)
![Minecraft 26.3](https://img.shields.io/badge/Minecraft-26.3-62B47A)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Small vanilla datapacks for Minecraft: Java Edition. No mods and nothing for players to install:
drop a zip into a world and it works, in singleplayer and on servers.

## Packs

| Pack | What it does | Minecraft |
| --- | --- | --- |
| [Cauldron Copper](packs/cauldron-copper/README.md) | Drop copper into a water cauldron to oxidize it instantly. | 26.3 |

## Install

1. Download a pack's zip from the [releases page](https://github.com/studiobimo/datapacks/releases).
2. Put the zip, unextracted, in your world's `datapacks` folder
   (`.minecraft/saves/<world>/datapacks`, or `<world>/datapacks` on a server).
3. Run `/reload`, or restart the world.

Each pack's page explains how to use it and how to uninstall it cleanly.

## Development

Requirements: [uv](https://docs.astral.sh/uv/).

```sh
make -C .devtools setup      # pinned tools + git hooks
make -C .devtools check      # lint + validate + build (lint is what CI runs)
make -C .devtools build      # zip every pack into dist/
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

## License

[MIT](LICENSE). Not an official Minecraft product; not approved by or associated with Mojang or
Microsoft.
