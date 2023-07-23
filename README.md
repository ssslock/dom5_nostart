# dom5_nostart

This script add nostart flags for provinces in a dom5 map.

To Use:
1. Install python 3
2. Put the script at the same folder of the map file
3. Adjust configurations at the top of the script
4. python add_nostart.py

These provinces will be modified with the flag:
1. Provinces with 7+ neighbors.
2. Cave provinces with 2- neighbors.
3. Coast provinces with 2- neighbors.
4. UW provinces with an adjacent land province and 2- neighbors.
5. Other provinces with 3- neighbors.

Note that UW - land connections and impassible connections are not count as neighbors.
Also note that the script only add onstart flags for the above provinces and will not remove any existing nostart flag nor add any start flag.
