import json
import os
import re

from .pack import pack_encounter_gen3
from .text import clean_string_rse

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    DATA = f"{SCRIPT_FOLDER}/emerald/wild_encounters.json"

    with open(DATA, "r") as f:
        encounters = json.load(f)

    emerald = bytes()
    map_names = []
    for map_number, encounter in enumerate(encounters):
        # Altering cave has 8 unused tables
        if re.match(r"gAlteringCave[2-9]", encounter["base_label"]):
            continue

        # Cave of Origin has 3 unused tables
        if "Unused" in encounter["base_label"]:
            continue

        # Mt Pyre 1F-3F share the same table
        # Mt Pyre 4F-6F share the same table
        if map_number in (38, 39, 41, 42):
            continue

        # Abandoned Ship has the same table for all locations
        if map_number == 56:
            continue

        # All Seafloor locations share the same table even if each one doesn't offer each encounter type (grass/water/fish)
        # The two that offer all 3 are 62/63 Room 6/Room 7
        if map_number in (57, 58, 59, 60, 61, 63, 64, 65):
            continue

        # All non ice room Shoal Cave share the same table even if each one doesn't offer each encounter type (grass/water/fish)
        # The two that offer all 3 are 82/83 Inner Room/Entrance Room
        if map_number in (80, 81, 83):
            continue

        # Magma Hideout has the same table for all locations
        if map_number in (100, 101, 102, 103, 104, 105, 106):
            continue

        # Mirage Tower has the same table for all locations
        if map_number in (108, 109, 110):
            continue

        # Artisan Cave has the same table for all locations
        if map_number == 113:
            continue

        map_name = (map_number, clean_string_rse(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        emerald += pack_encounter_gen3(map_number, encounter)

    with open("emerald.bin", "wb+") as f:
        f.write(emerald)

    if text:
        with open("e_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
