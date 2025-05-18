import json
import os

from .narc import Narc
from .pack import pack_encounter_gen5
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    B_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw/b_encount").get_elements()
    W_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw/w_encount").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/bw/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/bw/mapnames.bin")
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(427):
            map_headers.append(f.read(48))

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["bw"]

    b = bytes()
    w = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[20] | (map_header[21] << 8)

        # Invalid encounter area
        if encounter_id == 65535:
            continue

        # The lowest part in Relic Castle all share the same tables
        if encounter_id in (16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 32):
            continue

        # The Volcarona room and it's entrance in Relic Castle share the same table
        if encounter_id == 31:
            continue

        # Relic Castle B2F-B6F share the same tables
        if encounter_id in (12, 13, 14, 33, 34, 35, 36, 37):
            continue

        # Relic Castle 1F-B1F share the same tables
        if encounter_id in (10, 38, 39):
            continue

        location_number = map_header[26]
        location_name = MAP_NAMES[location_number]
        if location_name in location_modifiers and str(encounter_id) in location_modifiers[location_name]:
            location_name = location_modifiers[location_name][str(encounter_id)]

        map_name = (encounter_id, location_name)
        map_names.append(map_name)

        # Black
        b += pack_encounter_gen5(encounter_id, B_ENCOUNTERS[encounter_id])

        # White
        w += pack_encounter_gen5(encounter_id, W_ENCOUNTERS[encounter_id])

    with open("black.bin", "wb+") as f:
        f.write(b)

    with open("white.bin", "wb+") as f:
        f.write(w)

    if text:
        with open("bw_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
