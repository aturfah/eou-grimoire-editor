from helpers import parse_save_file, write_save_file

import json

base_grimoires, base_hex = parse_save_file("backups/base")

with open("base.json", 'w') as out_file:
    json.dump(base_grimoires, out_file, indent=2)

write_save_file(base_hex, base_grimoires)