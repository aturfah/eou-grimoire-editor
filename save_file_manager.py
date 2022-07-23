import tkinter as tk
from tkinter import filedialog
from copy import deepcopy
from pprint import pprint

import ui_helpers as uih
import map_helpers as mh

## Hide tkinter Window
root = tk.Tk()
root.wm_attributes('-topmost', 1)
root.withdraw()

NAME_ID_MAP = uih.name_id_map()
ID_NAME_MAP = mh.load_skill_ids()

class SaveFileManager:
    def __init__(self):
        self.filename = None
        self.orig_grimoire_data = None
        self.orig_hex = None
        self.grimoire_data = None
        self.chosen_idx = 0

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("SAV files", ".sav")])
        if not self.filename:
            return

        try:
            self.orig_grimoire_data, self.orig_hex = uih.load_wrapper(self.filename)
            self.grimoire_data = deepcopy(self.orig_grimoire_data)
        except Exception as exc:
            self._error_message("Error Loading", "Error: {}.\nPlease verify you're loading the mor1rgame.sav file.".format(exc))
            return

    def save_file(self):
        destination = filedialog.asksaveasfilename(filetypes=[("SAV files", ".sav")])
        if not destination:
            return

        try:
            uih.save_wrapper(destination, self.orig_hex, self.grimoire_data)
        except Exception as exc:
            raise exc

    def get_grimoire_labels(self):
        grim_names = []
        counter = 0
        name_str = "{ctr} {qlty} {cls} Grimoire; {nskills} Skills"
        for gdatum in self.grimoire_data:
            counter += 1
            if not gdatum["valid"]:
                grim_names.append("{ctr} Empty".format(ctr=counter))
            else:
                grim_class = gdatum["class"].split("(")[0]
                num_skills = 0
                for sdatum in gdatum["skills"]:
                    if sdatum["name"] != "Blank":
                        num_skills += 1

                grim_names.append(name_str.format(
                    ctr=counter,
                    qlty=gdatum["quality"],
                    cls=grim_class.strip(),
                    nskills=num_skills
                ))

        return grim_names

    def get_chosen_grimoire(self):
        return self.grimoire_data[self.chosen_idx]

    def set_grimoire_skill_name(self, idx, skill_name):
        old_skill_name = deepcopy(self.grimoire_data[self.chosen_idx]["skills"][idx]["name"])
        skill_level = self.grimoire_data[self.chosen_idx]["skills"][idx]["level"]

        self.grimoire_data[self.chosen_idx]["skills"][idx]["name"] = skill_name
        self.grimoire_data[self.chosen_idx]["skills"][idx]["_id"] = NAME_ID_MAP[skill_name]

        if skill_name == "Blank" and skill_level != 0:
            self.set_grimoire_skill_level(idx, "0")
        elif old_skill_name == "Blank":
            self.set_grimoire_skill_level(idx, "1")

    def set_grimoire_skill_level(self, idx, skill_level):
        skill_name = self.grimoire_data[self.chosen_idx]["skills"][idx]["name"]
        if not isinstance(skill_level, int):
            skill_level = int(skill_level)

        self.grimoire_data[self.chosen_idx]["skills"][idx]["level"] = skill_level
        self.grimoire_data[self.chosen_idx]["skills"][idx]["level_hex"] = (str(skill_level).zfill(2), "00")

        if skill_level == 0 and skill_name != "Blank":
            self.set_grimoire_skill_name(idx, "Blank")

    def set_grimoire_class(self, new_class):
        self.grimoire_data[self.chosen_idx]["class"] = new_class
        self.grimoire_data[self.chosen_idx]["class_hex"][1] = uih.class_id_map()[new_class]

    def set_grimoire_quality(self, new_quality):
        self.grimoire_data[self.chosen_idx]["quality"] = new_quality
        self.grimoire_data[self.chosen_idx]["quality_hex"][1] = uih.quality_id_map()[new_quality]

    def set_grimoire_generator(self, new_name):
        try:
            self.grimoire_data[self.chosen_idx]["name_hex"] = uih.ascii_to_hex(new_name)
            self.grimoire_data[self.chosen_idx]["name"] = new_name
        except Exception as exc:
            raise exc

        if new_name:
            self.grimoire_data[self.chosen_idx]["unknown_origin"] = False
            self.grimoire_data[self.chosen_idx]["class_hex"][0] = "00"
        else:
            self.grimoire_data[self.chosen_idx]["unknown_origin"] = True
            self.grimoire_data[self.chosen_idx]["class_hex"][0] = "30"
