import map_helpers as mh

def save_wrapper(file_hex, grimoire_list, filename):
    print("Save Wrapper")
    mh.write_save_file(file_hex, grimoire_list, filename)

def load_wrapper(filename):
    print("Load Wrapper")
    return mh.parse_save_file(filename)

def _invert_dictionary(temp):
    output = {}
    for key in temp.keys():
        if temp[key] not in output:
            output[temp[key]] = key

    return output


def name_id_map():
    """Get the reverse for the map from load_skill_ids"""
    return _invert_dictionary(mh.load_skill_ids())


def class_id_map():
    """Get the reverse for the map from GRIMOIRE_CLASS_MAP"""
    return _invert_dictionary(mh.GRIMOIRE_CLASS_MAP)


def quality_id_map():
    """Gets the reverse for the map GRIMOIRE_QUALITY_MAP."""
    return _invert_dictionary(mh.GRIMOIRE_QUALITY_MAP)


ascii_to_hex = mh.ascii_to_hex
