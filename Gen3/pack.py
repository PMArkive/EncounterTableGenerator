UNOWN = {
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER": [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 27],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_LIPTOO_CHAMBER": [2,  2,  2,  3,  3,  3,  7,  7,  7, 20, 20, 14],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_WEEPTH_CHAMBER": [13, 13, 13, 13, 18, 18, 18, 18,  8,  8,  4,  4],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_DILFORD_CHAMBER": [15, 15, 11, 11,  9,  9, 17, 17, 17, 16, 16, 16],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_SCUFIB_CHAMBER": [24, 24, 19, 19,  6,  6,  6,  5,  5,  5, 10, 10],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_RIXY_CHAMBER": [21, 21, 21, 22, 22, 22, 23, 23, 12, 12,  1,  1],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_VIAPOIS_CHAMBER": [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 26]
}


def pack_encounter_gen3(location: int, encounter: dict):
    data = location.to_bytes(1, "little")

    if (land := "land_mons" in encounter):
        data += encounter["land_mons"]["encounter_rate"].to_bytes(1, "little")
    else:
        data += b"\x00"

    if (water := "water_mons" in encounter):
        data += encounter["water_mons"]["encounter_rate"].to_bytes(1, "little")
    else:
        data += b"\x00"

    if (rock := "rock_smash_mons" in encounter):
        data += encounter["rock_smash_mons"]["encounter_rate"].to_bytes(1, "little")
    else:
        data += b"\x00"

    if (fish := "fishing_mons" in encounter):
        data += encounter["fishing_mons"]["encounter_rate"].to_bytes(1, "little")
    else:
        data += b"\x00"

    data += b"\x00"  # 1 byte padding

    if land:
        for i, slot in enumerate(encounter["land_mons"]["mons"]):
            specie = slot["species"]
            if encounter["map"] in UNOWN.keys():
                form = UNOWN[encounter["map"]][i]
                specie = (form << 11) | specie

            data += specie.to_bytes(2, "little")
            data += slot["min_level"].to_bytes(1, "little")
            data += b"\x00"  # 1 byte padding
    else:
        data += b"\x00" * (12 * 4)

    if water:
        for slot in encounter["water_mons"]["mons"]:
            data += slot["species"].to_bytes(2, "little")
            data += slot["max_level"].to_bytes(1, "little")
            data += slot["min_level"].to_bytes(1, "little")
    else:
        data += b"\x00" * (5 * 4)

    if rock:
        for slot in encounter["rock_smash_mons"]["mons"]:
            data += slot["species"].to_bytes(2, "little")
            data += slot["max_level"].to_bytes(1, "little")
            data += slot["min_level"].to_bytes(1, "little")
    else:
        data += b"\x00" * (5 * 4)

    if fish:
        for slot in encounter["fishing_mons"]["mons"]:
            data += slot["species"].to_bytes(2, "little")
            data += slot["max_level"].to_bytes(1, "little")
            data += slot["min_level"].to_bytes(1, "little")
    else:
        data += b"\x00" * (10 * 4)

    return data
