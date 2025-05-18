import json
import os

from .narc import Narc
from .pack import pack_encounter_dppt, pack_encounter_dppt_honey
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    D_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/dp/d_enc_data.narc").get_elements()
    P_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/dp/p_enc_data.narc").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/dp/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/dp/mapnames.bin")
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(559):
            map_headers.append(f.read(24))

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["dppt"]

    d = bytes()
    p = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[14] | (map_header[15] << 8)

        # Mt Coronet Summit covers two maps, with the same tables
        if encounter_id == 14:
            continue

        # Old Chateau has only two tables that differ, skip the others
        if encounter_id in (126, 127, 128, 129, 130, 131, 133):
            continue

        # Turnback Cave has duplicate entries based on pillars encountered
        if encounter_id in (64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80):
            continue

        # Solaceon Ruins all share the same table
        if encounter_id in (31, 33, 35, 36, 37, 38, 39, 44, 45, 46):
            continue

        if encounter_id != 65535:
            location_number = map_header[18] | (map_header[19] << 8)
            location_name = MAP_NAMES[location_number]
            if location_name in location_modifiers and str(encounter_id) in location_modifiers[location_name]:
                location_name = location_modifiers[location_name][str(encounter_id)]

            map_name = (encounter_id, location_name)
            map_names.append(map_name)

            # Diamond
            d += pack_encounter_dppt(encounter_id ,D_ENCOUNTERS[encounter_id])

            # Pearl
            p += pack_encounter_dppt(encounter_id, P_ENCOUNTERS[encounter_id])

    with open("diamond.bin", "wb+") as f:
        f.write(d)

    with open("pearl.bin", "wb+") as f:
        f.write(p)

    map_names.append((183, "Floaroma Meadow"))

    if text:
        with open("dppt_en.txt", "w+", encoding="utf-8") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")


def honey():
    HONEY_ENCOUNT = Narc(f"{SCRIPT_FOLDER}/dp/encdata_ex.narc").get_elements()

    locations = (
        145, 146, 147, 148, 149, 150, 156, 157, 159, 160,
        161, 162, 163, 164, 167, 169, 170, 7, 8, 9, 183
    )

    d = bytes()
    p = bytes()

    for location in locations:
        d += pack_encounter_dppt_honey(location, HONEY_ENCOUNT[2] + HONEY_ENCOUNT[3] + HONEY_ENCOUNT[4])
        p += pack_encounter_dppt_honey(location, HONEY_ENCOUNT[5] + HONEY_ENCOUNT[6] + HONEY_ENCOUNT[7])

    with open("d_honey.bin", "wb") as f:
        f.write(d)

    with open("p_honey.bin", "wb") as f:
        f.write(p)
