from time import sleep

#config
INPUT_FILE_NAME = "tlou1.map"
OUTPUT_FILE_NAME = "tlou1_nostart.map"

MAX_START = 6
MIN_START = 4
MIN_START_COAST = 3
MIN_START_CAVE = 3

#const
NO_START_BIT = 512
SEA_BIT = 4
DEEP_SEA_BIT = 2048
CAVE_BIT = 4096
IMPASSIBLE_BIT = 4

#var
province_flag = {}              # province terrain
neighbor_counts = {}            # province neighbor count. land - sea connections and impassible connections are not included
province_uw = {}                # True if province is sea or deep sea
province_cave = {}              # True if province is cave
province_uw_neighbor = {}       # True if province has uw neighbour
province_land_neighbor = {}     # True if province has land neighbour

def read_file():
    f = open(INPUT_FILE_NAME, "r")
    splited_lines = []
    while True:
        line = f.readline()
        if len(line) == 0:      # EOF
            break
        if len(line) == 1:      # empty line
            continue
        line = line.rstrip()    # remove \n
        splited_line = line.split(" ")
        splited_lines.append(splited_line)
    f.close()

    for splited_line in splited_lines:
        read_flag(splited_line)

    for splited_line in splited_lines:
        read_neighbor(splited_line)


def read_flag(splited_line):
    if splited_line[0] == "#terrain":
        province = splited_line[1]
        flag = int(splited_line[2])
        province_flag[province] = flag
        neighbor_counts[province] = 0
        province_uw[province] = bool(flag & (SEA_BIT | DEEP_SEA_BIT))   # either sea or deep sea
        province_cave[province] = bool(flag & CAVE_BIT)                 # cave
        province_uw_neighbor[province] = False
        province_land_neighbor[province] = False

def update_neighbor(province, neighbour):
    if province_uw[neighbour]:
        province_uw_neighbor[province] = True
    else:
        province_land_neighbor[province] = True

    if province_uw[province] == province_uw[neighbour]:
        neighbor_counts[province] += 1

def read_neighbor(splited_line):
    if splited_line[0] == "#neighbour":
        province1 = splited_line[1]
        province2 = splited_line[2]
        update_neighbor(province1, province2)
        update_neighbor(province2, province1)
    else:
        if splited_line[0] == "#neighbourspec":
            flag = int(splited_line[3])
            if flag & IMPASSIBLE_BIT:           # check impassible
                province1 = splited_line[1]
                province2 = splited_line[2]
                if province_uw[province1] == province_uw[province2]:
                    neighbor_counts[province1] -= 1
                    neighbor_counts[province2] -= 1

def check_nostart(province):
    neighbor_count = neighbor_counts[province]

    if (neighbor_count > MAX_START):
        return True

    if province_uw[province]:   # uw province
        if province_land_neighbor[province]:
            return neighbor_count < MIN_START_COAST
        else:
            return neighbor_count < MIN_START
    else:                       # land province
        if province_cave[province]:
            return neighbor_count < MIN_START_CAVE
        else:
            if province_uw_neighbor[province]:
                return neighbor_count < MIN_START_COAST
            else:
                return neighbor_count < MIN_START
    
    return False

def mark_nostart():
    start_count = 0
    nostart_count = 0
    for province in neighbor_counts.keys():
        if check_nostart(province):
            province_flag[province] |= NO_START_BIT
            nostart_count += 1
            print("no start: ", province)
        else:
            start_count += 1

    print("start count: ", len(province_flag.keys()) - nostart_count)
    print("no start count: ", nostart_count)

def generate_output():
    fin = open(INPUT_FILE_NAME, "r")
    lines = fin.readlines()
    fin.close()
    
    fout = open(OUTPUT_FILE_NAME, "w")
    for line in lines:
        if line.startswith("#terrain"): # replace original terrain command with generated one
            line = line.rstrip()        # remove \n
            splited_line = line.split(" ")
            province = splited_line[1]
            splited_line[2] = str(province_flag[province]) + "\n"
            fout.write(" ".join(splited_line))
        else:                           # copy line from the input file
            fout.write(line)
    fout.close()


def main():
    read_file()
    mark_nostart()
    generate_output()

main()