import io
import json
import os

from .narc import Narc
from .pack import pack_encounter_gen5
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    B_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw2/b2_encount").get_elements()
    W_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw2/w2_encount").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/bw2/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/bw2/mapnames.bin")
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(615):
            map_headers.append(f.read(48))

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["bw2"]

    b = bytes()
    w = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[20]

        # Invalid encounter area
        if encounter_id == 255:
            continue

        # Clay Tunnel tables are all the same, we opt to choose one that has the water tables included
        if encounter_id in (84, 86):
            continue

        # Floccessy Rance tables are the same, we opt to choose the one with the grass tables included
        if encounter_id == 44:
            continue

        # Giant Chasm Crater Forest has two tables that are the same
        if encounter_id == 35:
            continue

        # Route 4 has two tables that are the same
        if encounter_id == 105:
            continue

        # The lowest part in Relic Castle all share the same tables
        if encounter_id in (15, 16, 17):
            continue

        # The Volcarona room and it's entrance in Relic Castle share the same table
        if encounter_id == 19:
            continue

        # Reversal Mountain 1F all share the same table
        if encounter_id in (51, 53, 54, 55, 57, 59, 60):
            continue

        # Reversal Mountain B1F share the same table
        if encounter_id == 56:
            continue

        # Reversal Mountain B1F Chamber share the same table
        if encounter_id == 58:
            continue

        # Victory Road 1F has two identical tables
        if encounter_id == 78:
            continue

        # Victory Road (Outside 1) has two identical tables
        if encounter_id == 79:
            continue

        # Underground Ruins has 3 identical tables
        if encounter_id in (88, 89):
            continue

        # Strange House Entrance/Library share the same tables and also have duplicates
        if encounter_id in (62, 63, 64, 66):
            continue

        # Strange House Rooms 1-5 share the same table
        if encounter_id in (67, 68, 69, 70):
            continue

        # Castelia Sewers all have identical tables
        # Table 38 technically modifies levels of rippling water, but the map doesn't have any water
        if encounter_id in (38, 39, 40, 41):
            continue

        location_number = map_header[26]
        location_name = MAP_NAMES[location_number]
        if location_name in location_modifiers and str(encounter_id) in location_modifiers[location_name]:
            location_name = location_modifiers[location_name][str(encounter_id)]

        map_name = (encounter_id, location_name)
        map_names.append(map_name)

        # Black 2
        b += pack_encounter_gen5(encounter_id, B_ENCOUNTERS[encounter_id])

        # White 2
        w += pack_encounter_gen5(encounter_id, W_ENCOUNTERS[encounter_id])

    with open("black2.bin", "wb+") as f:
        f.write(b)

    with open("white2.bin", "wb+") as f:
        f.write(w)

    map_names.append((135, "Route 6 (Cave)"))
    map_names.append((136, "Route 13 (Giant Chasm)"))
    map_names.append((137, "Abundant Shrine (Pond)"))
    map_names.append((138, "Route 3 (Pond)"))

    if text:
        with open("bw2_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")


def hidden_grotto():
    BW_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw2/grotto").get_elements()
    locations = (45, 106, 126, 107, 135, 111, 121, 136, 118, 34, 130, 131, 123, 137, 9, 8, 101, 138, 100, 127)

    bw = bytes()
    for encounter, location in zip(BW_ENCOUNTERS, locations):
        stream = io.BytesIO(encounter)

        bw += location.to_bytes(1, "little")
        bw += b"\x00"  # 1 byte padding

        species = [0]*12
        max_level = [0]*12
        min_level = [0]*12
        gender = [0]*12
        item = [0]*16
        hidden_item = [0]*16

        for i in range(3):
            for j in range(4):
                species[i + j * 3] = stream.read(2)

            for j in range(4):
                max_level[i + j * 3] = stream.read(1)

            for j in range(4):
                min_level[i + j * 3] = stream.read(1)

            for j in range(4):
                gender[i + j * 3] = stream.read(1)

            stream.read(4)  # Form, always 0 -> skip
            stream.read(2)  # Padding

        stream.seek(0x9c)
        for i in range(4):
            for j in range(4):
                item[i + j * 4] = stream.read(2)

        for i in range(4):
            for j in range(4):
                hidden_item[i + j * 4] = stream.read(2)

        for i in range(12):
            bw += species[i]
            bw += max_level[i]
            bw += min_level[i]
            bw += gender[i]
            bw += b"\x00"  # 1 byte padding

        for x in item:
            bw += x

        for x in hidden_item:
            bw += x

    with open("bw2_grotto.bin", "wb+") as f:
        f.write(bw)
