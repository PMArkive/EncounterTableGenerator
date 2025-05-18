import json
import os
import re

from .pack import pack_encounter_gen3
from .text import clean_string_frlg

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    DATA = f"{SCRIPT_FOLDER}/frlg/wild_encounters.json"

    with open(DATA, "r") as f:
        encounters = json.load(f)

    map_names = []

    fr = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "FireRed" in x["base_label"], encounters)):
        # Altering Cave has 8 unused tables
        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            continue

        # Victory Road 1F and 3F share the same table
        if map_number == 15:
            continue

        # Pokemon Mansion 1F, 2F and 3F share the same table
        if map_number in (17, 18):
            continue

        # Pokemon Tower 4F and 5F share the same table
        if map_number == 36:
            continue

        # Mt Ember Summit Path 1F and 3F share the same table
        if map_number == 43:
            continue

        # Four Island Icefall Cave 1F and B1F share the same table
        if map_number == 53:
            continue

        # Five Island Lost Cave Room 1-10 share the same table
        if map_number in (57, 58, 59, 60, 61, 62, 63, 64, 65):
            continue

        # Five Island Lost Cave Room 11-14 share the same table
        if map_number in (67, 68, 69):
            continue

        # Route 21 North/South share the same table
        if map_number == 108:
            continue

        map_name = (map_number, clean_string_frlg(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        fr += pack_encounter_gen3(map_number, encounter)

    lg = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "LeafGreen" in x["base_label"], encounters)):
        # Altering Cave has 8 unused tables
        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            continue

        # Victory Road 1F and 3F share the same table
        if map_number == 15:
            continue

        # Pokemon Mansion 1F, 2F and 3F share the same table
        if map_number in (17, 18):
            continue

        # Pokemon Tower 4F and 5F share the same table
        if map_number == 36:
            continue

        # Mt Ember Summit Path 1F and 3F share the same table
        if map_number == 43:
            continue

        # Four Island Icefall Cave 1F and B1F share the same table
        if map_number == 53:
            continue

        # Five Island Lost Cave Room 1-10 share the same table
        if map_number in (57, 58, 59, 60, 61, 62, 63, 64, 65):
            continue

        # Five Island Lost Cave Room 11-14 share the same table
        if map_number in (67, 68, 69):
            continue

        # Route 21 North/South share the same table
        if map_number == 108:
            continue

        lg += pack_encounter_gen3(map_number, encounter)

    with open("firered.bin", "wb+") as f:
        f.write(fr)

    with open("leafgreen.bin", "wb+") as f:
        f.write(lg)

    if text:
        with open("frlg_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
