# dom5_nostart

This script add nostart flags for provinces in a dom5 map.

To Use:
1. Install python 3
2. Put the script at the same folder of the map file
3. Adjust configurations at the top of the script
4. python add_nostart.py

These provinces will be modified with the flag:
Provinces with 7+ neighbors.
Cave provinces with 2- neighbors.
Coast provinces with 2- neighbors.
UW provinces with an adjacent land province and with 2- neighbors.
Other provinces with 3- neighbors.

Note that UW - land connections and impassible connections are not count as neighbors.