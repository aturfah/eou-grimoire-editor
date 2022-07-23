from pathlib import Path
from pprint import pprint
from unicode_to_sjis import UNICODE_TO_SJIS
from sjis_to_unicode import SJIS_TO_UNICODE
import unicodedata


def ascii_to_hex(str_in, padded_length=72):
    output_arr = []
    for char in str_in:
        ## Convert to full width characters
        if char != " " and ord(char) != 8140:
            output_arr.append(0xFEE0 + ord(char))
        else:
            output_arr.append(0x3000) ## Full Width Space?

    output = ""
    for idx in range(len(output_arr)):
        try: 
            output += UNICODE_TO_SJIS[output_arr[idx]]
        except Exception:
            raise RuntimeError("Invalid character in name: '{}'".format(str_in[idx]))

    output = output.replace(" ", "")

    while len(output) < padded_length:
        output += "0"

    if len(output) > padded_length:
        raise RuntimeError("Name too Long")

    return output


def load_skill_ids():
    """Map the Little Endian ID Tuple to Skill Name"""
    output = {}
    sn_path = Path("skill_data/skill_ids.txt")
    for line in sn_path.read_text().splitlines():
        try:
            name, _, leID1, leID2 = line.split("\t")
        except Exception:
            pass

        output["".join((leID1.lower().zfill(2), leID2.lower().zfill(2)))] = name

    valid_skills = Path("skill_data/player_skills.txt").read_text().splitlines()
    valid_skills.extend(Path("skill_data/enemy_skills.txt").read_text().splitlines())

    keys_to_delete = []
    for key in output:
        if output[key] in valid_skills or output[key] == "Blank":
            continue
        keys_to_delete.append(key)
    
    for key in keys_to_delete:
        del output[key]

    return output


GRIMOIRE_CLASS_MAP = {
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


def map_grimoire_class(grimoire_data):
    """First two bytes determine class"""
    grimoire_class_tuple = grimoire_data[:2]
    # print("\tClass Hex:", grimoire_class_tuple)
    try:
        grimoire_class = GRIMOIRE_CLASS_MAP[grimoire_class_tuple[1]]
    except Exception:
        grimoire_class = "???"
    # print("\t\tClass:", grimoire_class)

    if grimoire_class_tuple[0] == '30':
        # print("\t\tOrigin: Unknown")
        pass
    elif grimoire_class_tuple[0] == '08':
        # print("\t\tOrigin: Story")
        pass
    else:
        # print("\t\tOrigin: ???")
        pass

    return grimoire_class, grimoire_class_tuple


GRIMOIRE_QUALITY_MAP = {
    "00": "(Empty)",
    "01": "Flawless",
    "02": "Slightly Damaged",
    "03": "Damaged",
    "04": "Imperfect"
}


def map_grimoire_quality(grimoire_data):
    """Bytes 3/4 are Quality"""
    quality_tuple = grimoire_data[2:4]
    try:
        grimoire_quality = GRIMOIRE_QUALITY_MAP[quality_tuple[1]]
    except Exception:
        raise RuntimeError("Did not expect to see Grimoire quality bytes: {}".format(quality_tuple))
    # print("\tQuality", grimoire_quality)

    return grimoire_quality, quality_tuple
    

def map_grimoire_type(grimoire_data):
    """Bytes 5/6 are Type"""
    grimoire_type_tuple = tuple(grimoire_data[4:6])
    type_map = {
        "00": "--",
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
        # raise RuntimeError("Did not expect to see Grimoire type bytes: {}".format(grimoire_type_tuple))

    # print("\tType:", grim_type)
    return grim_type, grimoire_type_tuple


def map_grimoire_generator(grimoire_data):
    """Bytes 6-42 should be grimoire generator (person who generated)"""
    gg_hex = grimoire_data[6:42]
    gg_unicode = []
    cur_char = []
    for h_number in [x.upper() for x in gg_hex]:
        if not cur_char and h_number in SJIS_TO_UNICODE.keys():
            gg_unicode.append(SJIS_TO_UNICODE[h_number])
            if gg_unicode[-1] != 0:
                gg_unicode[-1] = chr(gg_unicode[-1])
            continue

        cur_char.append(h_number)
        if len(cur_char) == 2:
            char_hex = "".join(cur_char)
            char_unic = SJIS_TO_UNICODE[char_hex]
            gg_unicode.append(chr(char_unic))
            cur_char = []

    ## Entirely 0; unknown origin
    gg_unicode = [x for x in gg_unicode if x != 0]
    unknown_origin = False
    if not gg_unicode:
        unknown_origin = True
        gg_unicode = []

    gg_unicode = "".join(gg_unicode)
    ## Names correspond to full-width characters, need half width
    gg_unicode = unicodedata.normalize("NFKC", gg_unicode)
    # print("\tGG Name:", len(gg_hex), gg_unicode)

    return gg_unicode, "".join(gg_hex), unknown_origin


def map_grimoire_skills(grimoire_data):
    """
    From 42 onwards, we have skill info
    First 2 are skill ID, second 2 are skill level
    """
    grimoire_skill_data = grimoire_data[42:]
    # print("\tSkills:")
    output = []
    current_skill = []
    for gsd in grimoire_skill_data:
        current_skill.append(gsd)

        if len(current_skill) == 4:
            skill_id = "".join(tuple(current_skill[:2]))
            try:
                skill_name = SKILL_ID_MAP[skill_id]
            except Exception:
                raise RuntimeError("Did not expect to see skill ID: {}".format(skill_id))
            skill_level_hex = tuple(current_skill[2:])
            skill_level = int(skill_level_hex[0], 16)

            current_skill = []
            if skill_id == ('00', '00'):
                continue

            # print("\t\tSkill ID:", skill_id)
            # print("\t\tSkill Name:", skill_name)
            # print("\t\tSkill Level:", skill_level)
            output.append({
                "_id": skill_id,
                "name": skill_name,
                "level": skill_level,
                "level_hex": skill_level_hex
            })

    return output


def parse_grimoire(grimoire_data):
    """Wrapper function."""
    validity = True
    if set("".join(grimoire_data)) == set(["0"]):
        validity = False

    # # print(len(grimoire_data))
    # # print("\t".join([str(x) for x in grimoire_data]))
    try:
        g_class, g_class_hex = map_grimoire_class(grimoire_data)
        g_qual, g_qual_hex = map_grimoire_quality(grimoire_data)
        g_type, g_type_hex = map_grimoire_type(grimoire_data)
        g_name, g_name_hex, unknown_origin = map_grimoire_generator(grimoire_data)
        g_skills = map_grimoire_skills(grimoire_data)
    except Exception as exc:
        raise exc

    return {
        "valid": validity,
        "class": g_class,
        "class_hex": g_class_hex,
        "quality": g_qual,
        "quality_hex": g_qual_hex,
        "type": g_type,
        "type_hex": g_type_hex,
        "name": g_name,
        "name_hex": g_name_hex,
        "unknown_origin": unknown_origin,
        "skills": g_skills
    }


def parse_save_file(fname):
    fname_path = Path(fname)
    if fname_path.is_dir():
        fname_path = fname_path.joinpath("mor1rgame.sav")

    file_bytes = fname_path.read_bytes()
    file_hex = file_bytes.hex(" ").split(" ")
    num_bytes = len(file_hex)

    if GRIMOIRE_START > num_bytes:
        raise RuntimeError("Invalid File")

    grimoire_info = []
    grimoire_data = []
    counter = 0
    for idx in range(GRIMOIRE_START, num_bytes):
        grimoire_data.append(file_hex[idx])
        if len(grimoire_data) == 70:
            # print("Grimoire #{}".format(counter+1))
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


def write_save_file(file_hex, grimoire_list, output_file="mor1rgame.sav"):
    all_grimoire_str = ""
    for grimoire_datum in grimoire_list:
        grimoire_str = ""
        grimoire_str += "".join(grimoire_datum["class_hex"])
        grimoire_str += "".join(grimoire_datum["quality_hex"])
        grimoire_str += "".join(grimoire_datum["type_hex"])
        grimoire_str += "".join(grimoire_datum["name_hex"])

        for skill_datum in grimoire_datum["skills"]:
            grimoire_str += skill_datum["_id"]
            grimoire_str += "".join(skill_datum["level_hex"])

        all_grimoire_str += grimoire_str

    if len(all_grimoire_str) != 99 * 70 * 2:
        ## 99 grimoires, each is 70 bytes but each byte is 2 characters
        raise RuntimeError("Error in Grimorie Data; incorrect length.")

    REL_GRIM_START = 2 * GRIMOIRE_START

    output_hex = file_hex[:REL_GRIM_START] + all_grimoire_str + file_hex[(REL_GRIM_START + len(all_grimoire_str)):]
    assert len(output_hex) == len(file_hex)
    print(len(output_hex), len(file_hex))

    with open(output_file, "wb") as out_file:
        out_file.write(bytes.fromhex(output_hex))

    return output_file


"""
Based on NA version, Grimoires start at the offset 0x3C58.
Each length is 46 (hex) or 70 (dec)
"""
GRIMOIRE_START = int(0x3C58)
SKILL_ID_MAP = load_skill_ids()
