import tkinter as tk
from tkinter import filedialog
from copy import deepcopy

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