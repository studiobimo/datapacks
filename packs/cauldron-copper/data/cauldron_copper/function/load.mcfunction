# Runs on world load and on /reload. Starts the scan loop; `replace` keeps a
# reload from stacking a second loop on top of the first.
schedule function cauldron_copper:scan 1s replace
