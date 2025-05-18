def pack_encounter_bdsp(location: int, encounter: dict):
    data = location.to_bytes(1, "little")
    data += encounter["encRate_gr"].to_bytes(1, "little")
    data += encounter["encRate_wat"].to_bytes(1, "little")
    data += encounter["encRate_turi_boro"].to_bytes(1, "little")
    data += encounter["encRate_turi_ii"].to_bytes(1, "little")
    data += encounter["encRate_sugoi"].to_bytes(1, "little")

    # Grass encounters
    for entry in encounter["ground_mons"]:
        data += entry["monsNo"].to_bytes(2, "little")
        data += entry["maxlv"].to_bytes(1, "little")
        data += b"\x00"  # 1 byte padding

    # Swarm modifiers (same level)
    for entry in encounter["tairyo"]:
        data += entry["monsNo"].to_bytes(2, "little")

    # Day modifiers (same level)
    for entry in encounter["day"]:
        data += entry["monsNo"].to_bytes(2, "little")

    # Night modifiers (same level)
    for entry in encounter["night"]:
        data += entry["monsNo"].to_bytes(2, "little")

    # Radar modifiers (same level)
    for entry in encounter["swayGrass"]:
        data += entry["monsNo"].to_bytes(2, "little")

    # FormProb (impacts Shellos/Gastrodon, skipping)

    # Nazo (seems unused)

    # Annoon Table (Unown)

    # Skipping dual slot encounters, the switch doesn't have a GBA reader

    # Surf
    for entry in encounter["water_mons"]:
        data += entry["monsNo"].to_bytes(2, "little")
        data += entry["maxlv"].to_bytes(1, "little")
        data += entry["minlv"].to_bytes(1, "little")

    # Old rod
    for entry in encounter["boro_mons"]:
        data += entry["monsNo"].to_bytes(2, "little")
        data += entry["maxlv"].to_bytes(1, "little")
        data += entry["minlv"].to_bytes(1, "little")

    # Good rod
    for entry in encounter["ii_mons"]:
        data += entry["monsNo"].to_bytes(2, "little")
        data += entry["maxlv"].to_bytes(1, "little")
        data += entry["minlv"].to_bytes(1, "little")

    # Super rod
    for entry in encounter["sugoi_mons"]:
        data += entry["monsNo"].to_bytes(2, "little")
        data += entry["maxlv"].to_bytes(1, "little")
        data += entry["minlv"].to_bytes(1, "little")

    return data


def pack_encounter_honey(location: int, encounter: dict):
    data = location.to_bytes(1, "little")
    data += b"\x00" # padding

    # Normal
    for entry in encounter:
        data += entry["Normal"].to_bytes(2, "little")
        data += b"\x0F"  # max level
        data += b"\x05"  # min level

    # Rare
    for entry in encounter:
        data += entry["Rare"].to_bytes(2, "little")
        data += b"\x0F"  # max level
        data += b"\x05"  # min level

    # Munchlax
    for entry in encounter:
        data += entry["SuperRare"].to_bytes(2, "little")
        data += b"\x0F"  # max level
        data += b"\x05"  # min level

    return data


def pack_encounter_underground(location: int, rand_mark_room: dict, special_pokemon_rates: dict, enabled_pokemon: dict, pokemon_data: dict):
    data = location.to_bytes(1, "little")
    data += rand_mark_room["min"].to_bytes(1, "little")
    data += rand_mark_room["max"].to_bytes(1, "little")
    data += len(enabled_pokemon).to_bytes(1, "little")
    data += len(special_pokemon_rates).to_bytes(1, "little")

    for rate in rand_mark_room["typerate"]:
        data += rate.to_bytes(1, "little")

    for rate in special_pokemon_rates:
        data += rate[0].to_bytes(2, "little")  # Rate
        data += rate[1].to_bytes(2, "little")  # Specie

    for enabled_pokemon in enabled_pokemon:
        pokemon = list(filter(lambda x: x["monsno"] == enabled_pokemon["monsno"], pokemon_data))[0]

        data += enabled_pokemon["monsno"].to_bytes(2, "little")
        for rate in pokemon["flagrate"]:
            data += rate.to_bytes(1, "little")
        data += enabled_pokemon["zukanflag"].to_bytes(1, "little")
        data += pokemon["rateup"].to_bytes(1, "little")
        data += pokemon["size"].to_bytes(1, "little")
        data += b"\x00"  # 1 byte padding

    return data
