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
        ## Store these to form padded strings later
        invalid_idx = []
        str1s = []
        gens = []
        nskills = []

        ## Check the longest lengths
        gen_width = 0
        skill_width = 0
        str1_width = 0
        counter = 0

        for gdatum in self.grimoire_data:
            if not gdatum["valid"]:
                invalid_idx.append(counter)
                str1s.append("")
                gens.append("")
                nskills.append("")
            else:
                grim_class = gdatum["class"].split("(")[0]
                num_skills = 0
                for sdatum in gdatum["skills"]:
                    if sdatum["name"] != "Blank":
                        num_skills += 1

                if num_skills == 1:
                    num_skills = "{} Skill".format(num_skills)
                else:
                    num_skills = "{} Skills".format(num_skills)

                gen_name = gdatum["name"]
                if gdatum["unknown_origin"] == True:
                    gen_name = "(Unknown Origin)"

                str1 = "{qlty} {cls} Grimoire".format(
                    qlty=gdatum["quality"],
                    cls=grim_class.strip()
                )

                str1s.append(str1)
                if len(str1) > str1_width:
                    str1_width = len(str1)

                gens.append(gen_name)
                if len(gen_name) > gen_width:
                    gen_width = len(gen_name)

                nskills.append(num_skills)
                if len(num_skills) > skill_width:
                    skill_width = len(num_skills)
            
            counter += 1

        posn_counter = 0
        grim_names = []
        name_str = "{ctr} | {str1:{width_str}} | {gen:{width_gen}} | {nskills:{width_skills}}"
        while posn_counter < len(self.grimoire_data):
            posn_ctr_str = str(posn_counter+1).zfill(2)
            if posn_counter in invalid_idx:
                grim_names.append("{ctr} Empty".format(ctr=posn_ctr_str))
            else:
                grim_names.append(name_str.format(
                    ctr=posn_ctr_str,
                    str1=str1s[posn_counter],
                    width_str=str1_width,
                    gen=gens[posn_counter],
                    width_gen=gen_width,
                    nskills=nskills[posn_counter],
                    width_skills=skill_width
                ).replace(" ", "&nbsp;"))
            posn_counter += 1

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

    def set_grimoire_unkown_origin(self, new_value):
        self.grimoire_data[self.chosen_idx]["unknown_origin"] = new_value

    def set_grimoire_active(self, new_value):
        self.grimoire_data[self.chosen_idx]["valid"] = new_value
