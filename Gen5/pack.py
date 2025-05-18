from ctypes import Structure, c_uint8, c_uint16


class DynamicSlot(Structure):
    _fields_ = [
        ("specie", c_uint16),
        ("min_level", c_uint8),
        ("max_level", c_uint8)
    ]


class StaticSlot(Structure):
    _fields_ = [
        ("specie", c_uint16),
        ("level", c_uint8)
    ]


class EncounterSeason(Structure):
    _fields_ = [
        ("grassRate", c_uint8),
        ("grassDoubleRate", c_uint8),
        ("grassSpecialRate", c_uint8),
        ("surfRate", c_uint8),
        ("surfSpecialRate", c_uint8),
        ("fishRate", c_uint8),
        ("fishSpecialRate", c_uint8),
        ("grass", StaticSlot * 12),
        ("grassDouble", StaticSlot * 12),
        ("grassSpecial", StaticSlot * 12),
        ("surf", DynamicSlot * 5),
        ("surfSpecial", DynamicSlot * 5),
        ("fish", DynamicSlot * 5),
        ("fishSpecial", DynamicSlot * 5),
    ]


class Encounter(Structure):
    _fields_ = [
        ("seasons", EncounterSeason * 1)
    ]


class EncounterSeasons(Structure):
    _fields_ = [
        ("seasons", EncounterSeason * 4)
    ]


def pack_encounter_gen5(location: int, encounter: bytes):
    if len(encounter) == 232:
        entry = Encounter.from_buffer_copy(encounter)
    else:
        entry = EncounterSeasons.from_buffer_copy(encounter)

    data = location.to_bytes(1, "little")
    data += len(entry.seasons).to_bytes(1, "little")
    for season in entry.seasons:
        data += season.grassRate.to_bytes(1, "little")
        data += season.grassDoubleRate.to_bytes(1, "little")
        data += season.grassSpecialRate.to_bytes(1, "little")
        data += season.surfRate.to_bytes(1, "little")
        data += season.surfSpecialRate.to_bytes(1, "little")
        data += season.fishRate.to_bytes(1, "little")
        data += season.fishSpecialRate.to_bytes(1, "little")
        data += b"\x00"  # 1 byte padding

        # Grass
        for slot in season.grass:
            data += slot.specie.to_bytes(2, "little")
            data += slot.level.to_bytes(1, "little")
            data += b"\x00"  # 1 byte padding

        # Grass Double
        for slot in season.grassDouble:
            data += slot.specie.to_bytes(2, "little")
            data += slot.level.to_bytes(1, "little")
            data += b"\x00"  # 1 byte padding

        # Grass Special
        for slot in season.grassSpecial:
            data += slot.specie.to_bytes(2, "little")
            data += slot.level.to_bytes(1, "little")
            data += b"\x00"  # 1 byte padding

        # Surf
        for slot in season.surf:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

        # Surf Special
        for slot in season.surfSpecial:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

        # Fish
        for slot in season.fish:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

        # Fish Special
        for slot in season.fishSpecial:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

    return data
