import json
import os

from .pack import pack_encounter_gen3
from .text import clean_string_rse

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    DATA = f"{SCRIPT_FOLDER}/rs/wild_encounters.json"

    with open(DATA, "r") as f:
        encounters = json.load(f)

    map_names = []

    ruby = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "Ruby" in x["base_label"], encounters)):
        # Mt Pyre 1F-3F share the same table
        # Mt Pyre 4F-6F share the same table
        if map_number in (19, 20, 22, 23):
            continue

        # All Seafloor locations share the same table even if each one doesn't offer each encounter type (grass/water/fish)
        # The two that offer all 3 are 32/33 Room 6/Room 7
        if map_number in (26, 27, 28, 29, 30, 31, 33, 34):
            continue

        # Cave Of Origin 1F, B1F, and B2F share the same table
        if map_number in (37, 38, 39):
            continue

        # All non ice room Shoal Cave share the same table even if each one doesn't offer each encounter type (grass/water/fish)
        # The two that offer all 3 are 43/44 Entrance Room/Inner Room
        if map_number in (43, 45, 46):
            continue

        # Abandoned Ship has the same table for all locations
        if map_number == 51:
            continue

        map_name = (map_number, clean_string_rse(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        ruby += pack_encounter_gen3(map_number, encounter)

    sapphire = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "Sapphire" in x["base_label"], encounters)):
        # Mt Pyre 1F-3F share the same table
        # Mt Pyre 4F-6F share the same table
        if map_number in (19, 20, 22, 23):
            continue

        # All Seafloor locations share the same table even if each one doesn't offer each encounter type (grass/water/fish)
        # The two that offer all 3 are 32/33 Room 6/Room 7
        if map_number in (26, 27, 28, 29, 30, 31, 33, 34):
            continue

        # Cave Of Origin 1F, B1F, and B2F share the same table
        if map_number in (37, 38, 39):
            continue

        # All non ice room Shoal Cave share the same table even if each one doesn't offer each encounter type (grass/water/fish)
        # The two that offer all 3 are 43/44 Entrance Room/Inner Room
        if map_number in (43, 45, 46):
            continue

        # Abandoned Ship has the same table for all locations
        if map_number == 51:
            continue

        map_name = (map_number, clean_string_rse(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        sapphire += pack_encounter_gen3(map_number, encounter)

    with open("ruby.bin", "wb+") as f:
        f.write(ruby)

    with open("sapphire.bin", "wb+") as f:
        f.write(sapphire)

    if text:
        with open("rs_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
