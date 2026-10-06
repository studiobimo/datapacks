# Run once before removing the pack: /function cauldron_copper:uninstall
# Stops the scan loop so nothing is left scheduled in the world.
schedule clear cauldron_copper:scan
tellraw @s "Cauldron Copper stopped. It is now safe to remove the datapack."
