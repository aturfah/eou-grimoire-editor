import map_helpers as mh

def save_wrapper(file_hex, grimoire_list):
    print("Save Wrapper")

def load_wrapper(filename):
    print("Load Wrapper")
    return mh.parse_save_file(filename)

def name_id_map():
    """Get the reverse for the map from load_skill_ids"""
    output = {}
    temp = mh.load_skill_ids()
    for key in temp.keys():
        output[temp[key]] = key

    return output
