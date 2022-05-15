from map_helpers import parse_save_file, write_save_file

import json

base_grimoires, base_hex = parse_save_file("backups/base")

with open("base.json", 'w') as out_file:
    json.dump(base_grimoires, out_file, indent=2)

with open("override.json", 'r') as in_file:
    override_grimoires = json.load(in_file)

write_save_file(base_hex, base_grimoires)
write_save_file(base_hex, override_grimoires)