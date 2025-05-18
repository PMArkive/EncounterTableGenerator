import json
import os
import re
from pathlib import Path

from .pack import pack_encounter_bdsp, pack_encounter_honey, pack_encounter_underground

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    D_ENCOUNTERS = f"{SCRIPT_FOLDER}/bdsp/FieldEncountTable_d.json"
    P_ENCOUNTERS = f"{SCRIPT_FOLDER}/bdsp/FieldEncountTable_p.json"
    MAP_INFO = f"{SCRIPT_FOLDER}/bdsp/MapInfo.json"
    AREA_NAME = f"{SCRIPT_FOLDER}/bdsp/english_dp_fld_areaname.json"
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(D_ENCOUNTERS, "r") as f:
        d_encounters = json.load(f)["table"]

    with open(P_ENCOUNTERS, "r") as f:
        p_encounters = json.load(f)["table"]

    with open(MAP_INFO, "r", encoding="utf-8") as f:
        map_info = json.load(f)["ZoneData"]

    with open(AREA_NAME, "r", encoding="utf-8") as f:
        area_name = json.load(f)["labelDataArray"]

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["bdsp"]

    d = bytes()
    p = bytes()
    map_names = []

    for map_number, encounter in enumerate(d_encounters):
        # Mt Coronet Summit covers two maps, with the same tables
        if map_number == 14:
            continue

        # Old Chateau all share the same table
        if map_number in (126, 127, 128, 129, 130, 131, 132, 133):
            continue

        # Turnback Cave has duplicate entries based on pillars encountered
        if map_number in (64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80):
            continue

        # Solaceon Ruins all share the same table
        if map_number in (31, 33, 35, 36, 37, 38, 39, 44, 45, 46):
            continue

        zone_id = encounter["zoneID"]
        zone_data = next((zone for zone in map_info if zone["ZoneID"] == zone_id), None)
        if zone_data is None:
            continue

        place_name = zone_data["PokePlaceName"]
        label_data = next((label for label in area_name if label["labelName"] == place_name))
        if label_data is None:
            continue

        location_name = label_data["wordDataArray"][0]["str"]
        if location_name in location_modifiers and str(map_number) in location_modifiers[location_name]:
            location_name = location_modifiers[location_name][str(map_number)]

        map_name = (map_number, location_name)
        map_names.append(map_name)

        d += pack_encounter_bdsp(map_number, encounter)

    for map_number, encounter in enumerate(p_encounters):
        # Mt Coronet Summit covers two maps, with the same tables
        if map_number == 14:
            continue

        # Old Chateau all share the same table
        if map_number in (126, 127, 128, 129, 130, 131, 132, 133):
            continue

        # Turnback Cave has duplicate entries based on pillars encountered
        if map_number in (64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80):
            continue

        # Solaceon Ruins all share the same table
        if map_number in (31, 33, 35, 36, 37, 38, 39, 44, 45, 46):
            continue

        zone_id = encounter["zoneID"]

        zone_data = next((zone for zone in map_info if zone["ZoneID"] == zone_id), None)
        if zone_data is None:
            continue

        place_name = zone_data["PokePlaceName"]
        label_data = next((label for label in area_name if label["labelName"] == place_name))
        if label_data is None:
            continue

        p += pack_encounter_bdsp(map_number, encounter)

    with open("bd.bin", "wb+") as f:
        f.write(d)

    with open("sp.bin", "wb+") as f:
        f.write(p)

    map_names.append((201, "Floaroma Meadow"))

    if text:
        with open("bdsp_en.txt", "w+", encoding="utf-8") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")


def honey():
    D_HONEY_ENCOUNT = f"{SCRIPT_FOLDER}/bdsp/FieldEncountTable_d.json"
    P_HONEY_ENCOUNT = f"{SCRIPT_FOLDER}/bdsp/FieldEncountTable_p.json"

    locations = (
        145, 146, 147, 148, 149, 150, 156, 157, 159, 160,
        161, 162, 163, 164, 167, 169, 170, 7, 8, 9, 201
    )

    with open(D_HONEY_ENCOUNT, "r") as f:
        d_honey_encount = json.load(f)["mistu"]

    with open(P_HONEY_ENCOUNT, "r") as f:
        p_honey_encount = json.load(f)["mistu"]

    d = bytes()
    p = bytes()

    for location in locations:
        d += pack_encounter_honey(location, d_honey_encount)
        p += pack_encounter_honey(location, p_honey_encount)

    with open("bd_honey.bin", "wb+") as f:
        f.write(d)

    with open("sp_honey.bin", "wb+") as f:
        f.write(p)


def underground():
    ENCOUNT = [str(path) for path in Path(f"{SCRIPT_FOLDER}/bdsp/").rglob("UgEncount*")]
    POKEMON_DATA = f"{SCRIPT_FOLDER}/bdsp/UgPokemonData.json"
    RAND_MARK = f"{SCRIPT_FOLDER}/bdsp/UgRandMark.json"
    SPECIAL_POKEMON = f"{SCRIPT_FOLDER}/bdsp/UgSpecialPokemon.json"

    encount = {}
    for path in ENCOUNT:
        with open(path, "r") as f:
            name = re.search(r"(UgEncount_\d+)", path).group(0)
            encount[name] = json.load(f)["table"]

    with open(POKEMON_DATA, "r") as f:
        pokemon_data = json.load(f)["table"]

    with open(RAND_MARK, "r") as f:
        rand_mark = json.load(f)["table"]

    with open(SPECIAL_POKEMON, "r") as f:
        special_pokemon = json.load(f)["Sheet1"]

    d = bytes()
    p = bytes()

    for room_id in range(2, 20):
        special_pokemon_room = list(filter(lambda x: x["id"] == room_id, special_pokemon))

        special_pokemon_rates_d = filter(lambda x: x["version"] != 3, special_pokemon_room)
        special_pokemon_rates_d = list(map(lambda x: (x["Dspecialrate"], x["monsno"]), special_pokemon_rates_d))
        special_pokemon_rates_d.sort(key=lambda x: x[0], reverse=True)

        special_pokemon_rates_p = filter(lambda x: x["version"] != 2, special_pokemon_room)
        special_pokemon_rates_p = list(map(lambda x: (x["Pspecialrate"], x["monsno"]), special_pokemon_rates_p))
        special_pokemon_rates_p.sort(key=lambda x: x[1], reverse=True)

        rand_mark_room = list(filter(lambda x: x["id"] == room_id, rand_mark))[0]
        ug_encount = encount[rand_mark_room["FileName"]]
        enabled_pokemon_d = list(filter(lambda x: x["version"] != 3, ug_encount))
        enabled_pokemon_p = list(filter(lambda x: x["version"] != 2, ug_encount))

        d += pack_encounter_underground(room_id, rand_mark_room, special_pokemon_rates_d, enabled_pokemon_d, pokemon_data)

        p += pack_encounter_underground(room_id, rand_mark_room, special_pokemon_rates_p, enabled_pokemon_p, pokemon_data)

    with open("bd_underground.bin", "wb+") as f:
        f.write(d)

    with open("sp_underground.bin", "wb+") as f:
        f.write(p)
