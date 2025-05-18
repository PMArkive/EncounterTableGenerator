from ctypes import Structure, c_uint8, c_uint16, c_uint32


def pack_encounter_dppt(location: int, encounter: bytes):
    class DynamicSlot(Structure):
        _fields_ = [
            ("max_level", c_uint8),
            ("min_level", c_uint8),
            ("specie", c_uint32)
        ]

    class StaticSlot(Structure):
        _fields_ = [
            ("level", c_uint8),
            ("specie", c_uint32)
        ]

    class Encounter(Structure):
        _fields_ = [
            ("grassRate", c_uint32),
            ("grass", StaticSlot * 12),
            ("swarm", c_uint32 * 2),
            ("noon", c_uint32 * 2),
            ("night", c_uint32 * 2),
            ("radar", c_uint32 * 4),
            ("forms", c_uint32 * 5),
            ("anoon", c_uint32),
            ("ruby", c_uint32 * 2),
            ("sapphire", c_uint32 * 2),
            ("emerald", c_uint32 * 2),
            ("firered", c_uint32 * 2),
            ("leafgreen", c_uint32 * 2),
            ("surfRate", c_uint32),
            ("surf", DynamicSlot * 5),
            ("rockRate", c_uint32),
            ("rock", DynamicSlot * 5),
            ("oldRate", c_uint32),
            ("old", DynamicSlot * 5),
            ("goodRate", c_uint32),
            ("good", DynamicSlot * 5),
            ("superRate", c_uint32),
            ("super", DynamicSlot * 5)
        ]

    entry = Encounter.from_buffer_copy(encounter)

    data = location.to_bytes(1, "little")
    data += entry.grassRate.to_bytes(1, "little")
    data += entry.surfRate.to_bytes(1, "little")
    data += entry.oldRate.to_bytes(1, "little")
    data += entry.goodRate.to_bytes(1, "little")
    data += entry.superRate.to_bytes(1, "little")

    # Grass
    for slot in entry.grass:
        data += slot.specie.to_bytes(2, "little")
        data += slot.level.to_bytes(1, "little")
        data += b"\x00"  # 1 byte padding

    # Swarm
    for specie in entry.swarm:
        data += specie.to_bytes(2, "little")

    # Noon
    for specie in entry.noon:
        data += specie.to_bytes(2, "little")

    # Night
    for specie in entry.night:
        data += specie.to_bytes(2, "little")

    # Radar
    for specie in entry.radar:
        data += specie.to_bytes(2, "little")

    # Forms (impacts Shellos/Gastrodon, skipping)

    # AnnoonTable (used for unown)

    # Ruby
    for specie in entry.ruby:
        data += specie.to_bytes(2, "little")

    # Sapphire
    for specie in entry.sapphire:
        data += specie.to_bytes(2, "little")

    # Emerald
    for specie in entry.emerald:
        data += specie.to_bytes(2, "little")

    # Fire Red
    for specie in entry.firered:
        data += specie.to_bytes(2, "little")

    # Leaf Green
    for specie in entry.leafgreen:
        data += specie.to_bytes(2, "little")

    # Surf
    for slot in entry.surf:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    # Rock smash (no actual rock smash encounters in DPPt)

    # Old rod
    for slot in entry.old:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    # Good rod
    for slot in entry.good:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    # Super rod
    for slot in entry.super:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    return data

def pack_encounter_dppt_honey(location: int, encounter: bytes):
    class Slot(Structure):
        _fields_ = [
            ("specie", c_uint16),
            ("dummy", c_uint8 * 2)
        ]

    class Encounter(Structure):
        _fields_ = [
            ("slot", Slot * 18)
        ]

    entry = Encounter.from_buffer_copy(encounter)

    data = location.to_bytes(1, "little")
    data += b"\x00" # padding

    for slot in entry.slot:
        data += slot.specie.to_bytes(2, "little")
        data += b"\x0F"  # max level
        data += b"\x05"  # min level

    return data

def pack_encounter_hgss(location: int, encounter: bytes):
    class DynamicSlot(Structure):
        _fields_ = [
            ("min_level", c_uint8),
            ("max_level", c_uint8),
            ("specie", c_uint16)
        ]

    class EncounterGrass(Structure):
        _fields_ = [
            ("level", c_uint8 * 12),
            ("morning", c_uint16 * 12),
            ("day", c_uint16 * 12),
            ("night", c_uint16 * 12)
        ]

    class Encounter(Structure):
        _fields_ = [
            ("grassRate", c_uint8),
            ("surfRate", c_uint8),
            ("rockRate", c_uint8),
            ("oldRate", c_uint8),
            ("goodRate", c_uint8),
            ("superRate", c_uint8),
            ("pad", c_uint16),
            ("grass", EncounterGrass),
            ("hoennSound", c_uint16 * 2),
            ("sinnohSound", c_uint16 * 2),
            ("surf", DynamicSlot * 5),
            ("rock", DynamicSlot * 2),
            ("old", DynamicSlot * 5),
            ("good", DynamicSlot * 5),
            ("super", DynamicSlot * 5),
            ("swarm", c_uint16 * 4)
        ]

    entry = Encounter.from_buffer_copy(encounter)

    data = location.to_bytes(1, "little")
    data += entry.grassRate.to_bytes(1, "little")
    data += entry.surfRate.to_bytes(1, "little")
    data += entry.rockRate.to_bytes(1, "little")
    data += entry.oldRate.to_bytes(1, "little")
    data += entry.goodRate.to_bytes(1, "little")
    data += entry.superRate.to_bytes(1, "little")
    data += b"\x00"  # 1 byte padding

    # Grass
    for specie in entry.grass.morning:
        data += specie.to_bytes(2, "little")

    for specie in entry.grass.day:
        data += specie.to_bytes(2, "little")

    for specie in entry.grass.night:
        data += specie.to_bytes(2, "little")

    for level in entry.grass.level:
        data += level.to_bytes(1, "little")

    # Hoenn Radio
    for specie in entry.hoennSound:
        data += specie.to_bytes(2, "little")

    # Sinnoh Radio
    for specie in entry.sinnohSound:
        data += specie.to_bytes(2, "little")

    # Surf
    for slot in entry.surf:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    # Rock Smash
    for slot in entry.rock:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    # Old Rod
    for slot in entry.old:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    # Good Rod
    for slot in entry.good:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    # Super Rod
    for slot in entry.super:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    # Swarm
    for specie in entry.swarm:
        data += specie.to_bytes(2, "little")

    return data

def pack_encounter_hgss_bug(encounter: bytes):
    class Slot(Structure):
        _fields_ = [
            ("specie", c_uint16),
            ("min_level", c_uint8),
            ("max_level", c_uint8),
            ("rate", c_uint8),
            ("score", c_uint8),
            ("dummy", c_uint8 * 2)
        ]

    class EncounterArea(Structure):
        _fields_ = [
            ("slots", Slot * 10)
        ]

    class Encounter(Structure):
        _fields_ = [
            ("areas", EncounterArea * 4)
        ]

    data = bytes()
    LOCATION_START = 142
    entry = Encounter.from_buffer_copy(encounter)

    for i, area in enumerate(entry.areas):
        data += (LOCATION_START + i).to_bytes(1, "little")
        data += b"\x00" # 1 byte padding
        for slot in area.slots:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

    return data

def pack_encounter_hgss_headbutt(location: int, encounter: bytes):
    class Slot(Structure):
        _fields_ = [
            ("specie", c_uint16),
            ("min_level", c_uint8),
            ("max_level", c_uint8)
        ]

    class Tree(Structure):
        _fields_ = [
            ("x", c_uint16),
            ("y", c_uint16)
        ]

    class Encounter(Structure):
        _fields_ = [
            ("tree_count", c_uint16),
            ("special_tree_count", c_uint16),
            ("tree", Slot * 12),
            ("special_tree", Slot * 6),
            ("tree_coord", Tree * 0)
        ]

    entry = Encounter.from_buffer_copy(encounter)

    data = location.to_bytes(1, "little")
    data += b"\x01" if entry.special_tree_count != 0 else b"\x00"

    for slot in entry.tree:
        data += slot.specie.to_bytes(2, "little")
        data += slot.max_level.to_bytes(1, "little")
        data += slot.min_level.to_bytes(1, "little")

    if entry.special_tree_count != 0:
        for slot in entry.special_tree:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")
    else:
        data += b"\x00" * (6 * 4)

    return data
