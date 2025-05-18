import io
import json
import os
import struct

from .narc import Narc
from .pack import pack_encounter_hgss, pack_encounter_hgss_bug, pack_encounter_hgss_headbutt
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    HG_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/hgss/hg_encount").get_elements()
    SS_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/hgss/ss_encount").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/hgss/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/hgss/mapnames.bin")
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(540):
            map_headers.append(f.read(24))

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["hgss"]

    hg = bytes()
    ss = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[0]

        # Sprout Tower has the same tables for the entire location
        if encounter_id == 7:
            continue

        # Future note: 23/24 National Park tables depend on national dex or not

        # Bell Tower has the same tables for the entire location
        if encounter_id in (31, 32, 33, 34, 35, 36, 37, 84):
            continue

        # Mt. Moon has two seperate location inside the cave with the same tables
        if encounter_id == 107:
            continue

        # Ruins of Alpha interior all share the same table
        if encounter_id in (12, 13):
            continue

        if (encounter_id := map_header[0]) != 255:
            location_number = map_header[18]
            location_name = MAP_NAMES[location_number]
            if location_name in location_modifiers and str(encounter_id) in location_modifiers[location_name]:
                location_name = location_modifiers[location_name][str(encounter_id)]

            map_name = (encounter_id, location_name)
            map_names.append(map_name)

            # HG
            hg += pack_encounter_hgss(encounter_id, HG_ENCOUNTERS[encounter_id])

            # SS
            ss += pack_encounter_hgss(encounter_id, SS_ENCOUNTERS[encounter_id])

    with open("heartgold.bin", "wb+") as f:
        f.write(hg)

    with open("soulsilver.bin", "wb+") as f:
        f.write(ss)

    map_names.append((142, "Bug Contest"))
    map_names.append((143, "Bug Contest (Tuesday)"))
    map_names.append((144, "Bug Contest (Thursday)"))
    map_names.append((145, "Bug Contest (Saturday)"))
    map_names.append((146, "Azalea Town"))
    map_names.append((147, "Pewter City"))
    map_names.append((148, "Safari Zone Gate"))
    map_names.append((149, "Safari Zone (Plains)"))
    map_names.append((150, "Safari Zone (Meadow)"))
    map_names.append((151, "Safari Zone (Savannah)"))
    map_names.append((152, "Safari Zone (Peak)"))
    map_names.append((153, "Safari Zone (Rocky Beach)"))
    map_names.append((154, "Safari Zone (Wetland)"))
    map_names.append((155, "Safari Zone (Forest)"))
    map_names.append((156, "Safari Zone (Swamp)"))
    map_names.append((157, "Safari Zone (Marshland)"))
    map_names.append((158, "Safari Zone (Wasteland)"))
    map_names.append((159, "Safari Zone (Mountain)"))
    map_names.append((160, "Safari Zone (Desert)"))

    if text:
        with open("hgss_en.txt", "w+", encoding="utf-8") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")


def bug():
    BUG_ENCOUNT = f"{SCRIPT_FOLDER}/hgss/mushi_encount.bin"

    with open(BUG_ENCOUNT, "rb") as f:
        data = f.read()

    bug = pack_encounter_hgss_bug(data)

    with open("hgss_bug.bin", "wb") as f:
        f.write(bug)


def headbutt():
    HG_HEADBUTT_ENCOUNT = [x for x in Narc(f"{SCRIPT_FOLDER}/hgss/hg_headbutt").get_elements() if len(x) != 4]
    SS_HEADBUTT_ENCOUNT = [x for x in Narc(f"{SCRIPT_FOLDER}/hgss/ss_headbutt").get_elements() if len(x) != 4]

    locations = (
        111, 112, 113, 114, 115, 116, 117, 118, 121, 92, 122, 123,
        124, 125, 127, 129, 131, 103, 104, 105, 1, 3, 4, 8,
        17, 21, 22, 25, 26, 38, 39, 52, 57, 59, 67, 68,
        95, 96, 147, 97, 98, 99, 100, 0, 2, 5, 146, 27,
        58, 85, 128, 24, 20, 137, 71, 102, 148, 136, 125, 87
    )

    hg_headbutt = bytes()
    for i, encounter in enumerate(HG_HEADBUTT_ENCOUNT):
        # Skip double Route 16
        if i == 58:
            continue

        hg_headbutt += pack_encounter_hgss_headbutt(locations[i], encounter)

    ss_headbutt = bytes()
    for i, encounter in enumerate(SS_HEADBUTT_ENCOUNT):
        # Skip double Route 16
        if i == 58:
            continue

        ss_headbutt += pack_encounter_hgss_headbutt(locations[i], encounter)

    with open("hg_headbutt.bin", "wb") as f:
        f.write(hg_headbutt)

    with open("ss_headbutt.bin", "wb") as f:
        f.write(ss_headbutt)


def safari():
    SAFARI_ENCOUNT = Narc(f"{SCRIPT_FOLDER}/hgss/safari").get_elements()

    safari = bytes()
    LOCATION_START = 149
    # HG and SS encounters match
    for index, safari_encounter in enumerate(SAFARI_ENCOUNT):
        safari += (LOCATION_START + index).to_bytes(1, "little")

        water_flag = index in (1, 4, 5, 7, 8)
        safari += b"\x01" if water_flag else b"\x00"

        stream = io.BytesIO(safari_encounter)

        tall_grass_encounters = int.from_bytes(stream.read(1), "little")  # 10
        surfing_encounters = int.from_bytes(stream.read(1), "little")  # 3
        old_rod_encounters = int.from_bytes(stream.read(1), "little")  # 2
        good_rod_encounters = int.from_bytes(stream.read(1), "little")  # 2
        super_rod_encounters = int.from_bytes(stream.read(1), "little")  # 2
        stream.read(3)  # Pad

        encounters = (
            tall_grass_encounters, surfing_encounters, old_rod_encounters,
            good_rod_encounters, super_rod_encounters
        )

        # Grass, Surfing, Old Rod, Good Rod, Super Rod
        for encounter in encounters:
            # Normal slots
            for _ in range(30):
                specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
                level = stream.read(1)
                stream.read(1)

                safari += specie
                safari += level
                safari += b"\x00"  # 1 byte padding

            # Block modifiers
            for _ in range(encounter * 3):
                specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
                level = stream.read(1)
                stream.read(1)

                safari += specie
                safari += level
                safari += b"\x00"  # 1 byte padding

            first_block_type = []
            first_block_quantity = []
            second_block_type = []
            second_block_quantity = []

            # Blocks
            for _ in range(encounter):
                first_block_type.append(stream.read(1))
                first_block_quantity.append(stream.read(1))
                second_block_type.append(stream.read(1))
                second_block_quantity.append(stream.read(1))

            for type in first_block_type:
                safari += type

            for quantity in first_block_quantity:
                safari += quantity

            for type in second_block_type:
                safari += type

            for quantity in second_block_quantity:
                safari += quantity

            # Handle blank water encounter below
            if not water_flag:
                break

        if not water_flag:
            safari += b"\x00" * 624

    with open("hgss_safari.bin", "wb") as f:
        f.write(safari)
