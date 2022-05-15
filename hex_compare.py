from pathlib import Path


base_b = Path("backups/base/mor1rgame.sav").read_bytes()
posdel_b = Path("backups/delete-chaser/mor1rgame.sav").read_bytes()

# base_hex = ["{:02x}".format(c) for c in base_b]
base_hex = base_b.hex(" ").split(" ")
posdel_hex = ["{:02x}".format(c) for c in posdel_b]

print(len(base_hex))
print(len(posdel_hex))


grimoire_start = int(0x3C58)

"""
Based on NA version, Grimoires start at the offset 0x3C58.
Each length is 46 (hex) or 70 (dec)
"""

num_bytes = len(posdel_hex)
counter = 0
# for idx in range(grimoire_start, num_bytes):
#     if base_hex[idx] != posdel_hex[idx]:
#         counter += 1
#         print(idx, base_hex[idx], posdel_hex[idx])

# print(counter)

def load_skill_ids():
    """Map the Little Endian ID Tuple to Skill Name"""
    output = {}
    sn_path = Path("skill_data/skill_ids.txt")
    for line in sn_path.read_text().splitlines():
        try:
            name, _, leID1, leID2 = line.split("\t")
        except Exception:
            pass

        output[(leID1.lower(), leID2.lower())] = name

    return output

skill_id_map = load_skill_ids()

def map_grimoire_class(grimoire_data):
    """First two bytes determine class"""
    grimoire_class_tuple = tuple(grimoire_data[:2])
    print("\tClass Hex:", grimoire_class_tuple)
    class_map = {
        "00": "Landsknecht (Sword/Axe)",
        "01": "Survivalist (Bow)",
        "02": "Protector (Shield)",
        "03": "Dark Hunter (Sword/Whip)",
        "04": "Medic (Flask) (Staff)",
        "05": "Alchemist (Staff) (no bonus)",
        "06": "Troubadour (no bonus)",
        "07": "Ronin (Katana)",
        "08": "Hexer (no bonus)",
        "09": "Highlander (Spear)",
        "0a": "Gunner (Gun)"
    }

    try:
        grimoire_class = class_map[grimoire_class_tuple[1]]
    except Exception:
        grimoire_class = "???"
    print("\t\tClass:", grimoire_class)

    if grimoire_class_tuple[0] == '30':
        print("\t\tOrigin: Unknown")
    elif grimoire_class_tuple[0] == '08':
        print("\t\tOrigin: Story")
    else:
        print("\t\tOrigin: ???")

    return grimoire_class, grimoire_class_tuple


def map_grimoire_quality(grimoire_data):
    """Bytes 3/4 are Quality"""
    quality_tuple = tuple(grimoire_data[2:4])
    quality_map = {
        "01": "Flawless",
        "02": "Slightly Damaged",
        "03": "Damaged",
        "04": "Imperfect"
    }
    grimoire_quality = quality_map[quality_tuple[1]]
    print("\tQuality", grimoire_quality)

    return grimoire_quality, quality_tuple
    

def map_grimoire_type(grimoire_data):
    """Bytes 5/6 are Type"""
    grimoire_type_tuple = tuple(grimoire_data[4:6])
    type_map = {
        "06": "Sword Grimoire",
        "07": "Battle Grimoire",
        "08": "Gather Grimoire",
        "15": "Gun Grimoire",
        "14": "Spear Grimoire",
        "02": "Power Grimoire", # Troubadour Skills
        "03": "Power Grimoire", # This was with the Chasers, maybe Silver
        "0c": "Heal Grimoire",
        "0d": "Shield Grimoire",
        "0e": "Whip",
        "10": "Spell",
        "13": "Curse",
        "16": "Bull",
        "17": "Beast"
    }
    
    try:
        grim_type = type_map[grimoire_type_tuple[0]]
    except Exception as exc:
        grim_type = "???"
        raise exc

    print("\tType:", grim_type)
    return grim_type, grimoire_type_tuple


def map_grimoire_generator(grimoire_data):
    """Bytes 6-42 should be grimoire generator"""
    temp = "82	71	82	81	82	91	82	95	82	8E	82	81	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00".split("\t")
    print("\tGG Name:", len(grimoire_data[6:42]), len(temp))
    return tuple(grimoire_data[6:42])


def map_grimoire_skills(grimoire_data):
    """
    From 42 onwards, we have skill info
    First 2 are skill ID, second 2 are skill level
    """
    grimoire_skill_data = grimoire_data[42:]
    print("\tSkills:")
    output = []
    current_skill = []
    for gsd in grimoire_skill_data:
        current_skill.append(gsd)

        if len(current_skill) == 4:
            skill_id = tuple(current_skill[:2])
            skill_name = skill_id_map[skill_id]
            skill_level = tuple(current_skill[2:])
            skill_level = int(skill_level[0], 16)

            current_skill = []
            if skill_id == ('00', '00'):
                continue

            print("\t\tSkill ID:", skill_id)
            print("\t\tSkill Name:", skill_name)
            print("\t\tSkill Level:", skill_level)
            output.append({
                "_id": skill_id,
                "name": skill_name,
                "level": skill_level
            })

    return output


def parse_grimoire(grimoire_data):
    """
    
    """
    if set("".join(grimoire_data)) == set(["0"]):
        return

    # print(len(grimoire_data))
    # print("\t".join([str(x) for x in grimoire_data]))
    g_class, g_class_hex = map_grimoire_class(grimoire_data)
    g_qual, g_qual_hex = map_grimoire_quality(grimoire_data)
    g_type, g_type_hex = map_grimoire_type(grimoire_data)
    g_generator = map_grimoire_generator(grimoire_data)
    g_skills = map_grimoire_skills(grimoire_data)

    return {
        "class": g_class,
        "class_hex": g_class_hex,
        "quality": g_qual,
        "quality_hex": g_qual_hex,
        "type": g_type,
        "type_hex": g_type_hex,
        "generator": g_generator,
        "skills": g_skills
    }


grimoire_info = []
grimoire_data = []
counter = 1
for idx in range(grimoire_start, num_bytes):
    grimoire_data.append(base_hex[idx])
    if len(grimoire_data) == 70:
        print("Grimoire #{}".format(counter))
        # grimoire_data = "00	02	04	01	07	00	82	71	82	81	82	91	82	95	82	8E	82	81	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	48	00	0A	00	89	00	0A	00	B1	01	0A	00	04	02	0A	00	02	00	0A	00	03	00	0A	00	41	00	0A	00".lower().split("\t")
        grimoire_info.append(parse_grimoire(grimoire_data))
        # break
        counter += 1
        grimoire_data = []

    if counter == 99:
        break
