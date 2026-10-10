# Cauldron Copper

Drop copper into a water cauldron and it oxidizes on the spot. No waiting weeks for a roof to
turn green.

| | |
| --- | --- |
| Minecraft | 26.3 (Java Edition) |
| Type | Data pack, server-side. Works in singleplayer and on servers; players need nothing installed. |
| License | [MIT](../../LICENSE) |

## How it works

1. Fill a cauldron with water. Any level works.
2. Throw copper items into it.
3. Within a second the whole stack turns into its **oxidized** variant. Pick it up.

The water is not used up, so one cauldron converts as much copper as you throw at it.

## What converts

Every stage (fresh, exposed, weathered), waxed or not, becomes the oxidized, unwaxed variant of
the same block:

| | | |
| --- | --- | --- |
| Copper block | Cut copper | Cut copper stairs |
| Cut copper slab | Chiseled copper | Copper grate |
| Copper bulb | Copper door | Copper trapdoor |
| Lightning rod | Copper chest | Copper bars |
| Copper chain | Copper lantern | Copper golem statue |

Waxed oxidized copper loses its wax too. Everything else is left alone, including copper ingots,
raw copper and copper ore.

## Install

1. Download the latest `cauldron-copper-<version>+mc<minecraft>.zip` from the
   [releases page](https://github.com/studiobimo/datapacks/releases). Version 1.0.1 was
   published without its zip; use 1.0.2 or later.
2. Put the zip, unextracted, in your world's `datapacks` folder.
3. Run `/reload`, or restart the world.

`/datapack list` shows it as enabled once it has loaded.

## Uninstall

1. Run `/function cauldron_copper:uninstall`.
2. Remove the zip from the `datapacks` folder and run `/reload`.

The pack stores nothing in your world. Copper you already converted stays oxidized.

## Technical notes

- Namespace: `cauldron_copper`. The only vanilla file it touches is the `minecraft:load` function
  tag, which it appends to.
- One scheduled function runs once a second and checks item entities. There is no per-tick work.
- No scoreboards, storage, markers or advancements.
