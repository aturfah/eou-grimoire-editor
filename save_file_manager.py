import tkinter as tk
from tkinter import filedialog
from copy import deepcopy
from pprint import pprint

import ui_helpers as uih

## Hide tkinter Window
root = tk.Tk()
root.wm_attributes('-topmost', 1)
root.withdraw()


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