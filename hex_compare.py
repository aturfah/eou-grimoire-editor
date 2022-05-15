from pathlib import Path
from pprint import pprint
import json

GRIMOIRE_START = int(0x3C58)

"""
Based on NA version, Grimoires start at the offset 0x3C58.
Each length is 46 (hex) or 70 (dec)
"""

def load_skill_ids():
    """Map the Little Endian ID Tuple to Skill Name"""
    output = {}
    sn_path = Path("skill_data/skill_ids.txt")
    for line in sn_path.read_text().splitlines():
        try:
            name, _, leID1, leID2 = line.split("\t")
        except Exception:
            pass

        output["".join((leID1.lower(), leID2.lower()))] = name

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
    return "".join(grimoire_data[6:42])


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
            skill_id = "".join(tuple(current_skill[:2]))
            skill_name = skill_id_map[skill_id]
            skill_level_hex = tuple(current_skill[2:])
            skill_level = int(skill_level_hex[0], 16)

            current_skill = []
            if skill_id == ('00', '00'):
                continue

            print("\t\tSkill ID:", skill_id)
            print("\t\tSkill Name:", skill_name)
            print("\t\tSkill Level:", skill_level)
            output.append({
                "_id": skill_id,
                "name": skill_name,
                "level": skill_level,
                "level_hex": skill_level_hex
            })

    return output


def parse_grimoire(grimoire_data):
    """Wrapper function."""
    if set("".join(grimoire_data)) == set(["0"]):
        return {
            "valid": False,
            "hex": "".join(grimoire_data)
        }

    # print(len(grimoire_data))
    # print("\t".join([str(x) for x in grimoire_data]))
    g_class, g_class_hex = map_grimoire_class(grimoire_data)
    g_qual, g_qual_hex = map_grimoire_quality(grimoire_data)
    g_type, g_type_hex = map_grimoire_type(grimoire_data)
    g_generator = map_grimoire_generator(grimoire_data)
    g_skills = map_grimoire_skills(grimoire_data)

    return {
        "valid": True,
        "class": g_class,
        "class_hex": g_class_hex,
        "quality": g_qual,
        "quality_hex": g_qual_hex,
        "type": g_type,
        "type_hex": g_type_hex,
        "generator": g_generator,
        "skills": g_skills
    }


def parse_grimoire_file(fname):
    fname_path = Path(fname)
    if fname_path.is_dir():
        fname_path = fname_path.joinpath("mor1rgame.sav")

    file_bytes = fname_path.read_bytes()
    file_hex = file_bytes.hex(" ").split(" ")
    num_bytes = len(file_hex)

    grimoire_info = []
    grimoire_data = []
    counter = 0
    for idx in range(GRIMOIRE_START, num_bytes):
        grimoire_data.append(file_hex[idx])
        if len(grimoire_data) == 70:
            print("Grimoire #{}".format(counter+1))
            # grimoire_data = "00	02	04	01	07	00	82	71	82	81	82	91	82	95	82	8E	82	81	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	48	00	0A	00	89	00	0A	00	B1	01	0A	00	04	02	0A	00	02	00	0A	00	03	00	0A	00	41	00	0A	00".lower().split("\t")
            g_info = parse_grimoire(grimoire_data)
            if g_info:
                grimoire_info.append(g_info)
            # break
            counter += 1
            grimoire_data = []

        if counter == 99:
            ## Max of 99 Grimoires
            break

    return grimoire_info, "".join(file_hex)

base_grimoires, base_hex = parse_grimoire_file("backups/base/mor1rgame.sav")

with open("base.json", 'w') as out_file:
    json.dump(base_grimoires, out_file, indent=2)

# delvr_grimoires, delvr_hex = parse_grimoire_file("backups/delete-voltrounds")
# delchaser_grimoires, delchaser_hex = parse_grimoire_file("backups/delete-chaser")

# with open("del_vr.json", 'w') as out_file:
#     json.dump(delvr_grimoires, out_file, indent=2)

# with open("del_chaser.json", "w") as out_file:
#     json.dump(delchaser_grimoires, out_file, indent=2)

## Make an Edit to the first Grimoire
base_grimoires[0]["skills"][0]["_id"] = "0700"
base_grimoires[0]["skills"][0]["level_hex"] = ["08", "00"]

with open("base_mod.json", 'w') as out_file:
    json.dump(base_grimoires, out_file, indent=2)


def write_sav_file(file_hex, grimoire_list, output_file="backups/base_mod/mor1rgame.sav"):
    all_grimoire_str = ""
    for grimoire_datum in grimoire_list:
        pprint(grimoire_datum)
        grimoire_str = ""
        if grimoire_datum["valid"]:
            grimoire_str += "".join(grimoire_datum["class_hex"])
            grimoire_str += "".join(grimoire_datum["quality_hex"])
            grimoire_str += "".join(grimoire_datum["type_hex"])
            grimoire_str += "".join(grimoire_datum["generator"])
            
            for skill_datum in grimoire_datum["skills"]:
                grimoire_str += skill_datum["_id"]
                grimoire_str += "".join(skill_datum["level_hex"])

            all_grimoire_str += grimoire_str
        else:
            all_grimoire_str += grimoire_datum["hex"]


    output_hex = file_hex[:GRIMOIRE_START] + all_grimoire_str + file_hex[(GRIMOIRE_START + len(all_grimoire_str)):]
    assert len(output_hex) == len(file_hex)

    with open(output_file, "wb") as out_file:
        out_file.write(bytes.fromhex(output_hex))

write_sav_file(base_hex, base_grimoires)