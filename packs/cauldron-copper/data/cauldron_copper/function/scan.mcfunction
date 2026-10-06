# Once a second: every copper item lying in a water cauldron becomes its fully
# oxidized, unwaxed variant. The whole stack converts and keeps its size.
schedule function cauldron_copper:scan 1s replace
execute as @e[type=minecraft:item] at @s if items entity @s contents #cauldron_copper:oxidizable if block ~ ~ ~ minecraft:water_cauldron run item modify entity @s contents cauldron_copper:oxidize
