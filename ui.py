from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox

from pprint import pprint

import ui_helpers as uih
from tkinter_complete import AutocompleteCombobox

class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
 
        self.title("Etrian Odyssey Untold - Grimoire Editor")
        self.minsize(500,400)

        ## Prepare label
        header = ttk.Label(
            self,
            text="EOU Grimoire Editor",
            anchor=CENTER)
        header.config(font=("EOU Grimoire Editor", 16))
        header.grid(row=0, column=1, padx=5,pady=5)

        ## Get load/save buttons ready
        self.buttonframe = ttk.Frame(self)
        self.buttonframe.grid(row=1, column=0, columnspan=2)
        self.load_button = ttk.Button(self.buttonframe, text="Load File", command=self._load_wrapper)
        self.load_button.grid(row=1, column=1)
        self.save_button = ttk.Button(self.buttonframe, text="Save File", state=DISABLED, command=self._save_wrapper)
        self.save_button.grid(row=1, column=3)

        ## This text determines if loaded
        self.file_loaded = False
        self.loaded_text = StringVar()
        self.loaded_text.set("No File Loaded")
        self.loaded_label = Label(self, textvariable=self.loaded_text)
        self.loaded_label.grid(row=2, column=1)

        ## Get the grimoire listbox
        self.chosen_idx = 0
        self.grimoire_frame = ttk.Frame(self)
        self.grimoire_frame.grid(row=2, column=2, columnspan=8)
        self.grimoire_choices = StringVar(value=[])
        self.grimoire_disp_list = Listbox(self,
            listvariable=self.grimoire_choices,
            height=15, exportselection=False)
        self.grimoire_disp_list.grid(row=3, column=1)
        self.grimoire_disp_list.bind('<<ListboxSelect>>', self._on_listbox_select)

        ## Set the Grimoire variables
        self.file_hex = None
        self.grimoire_data = []
        self.name_id_map = uih.name_id_map()

    def _error_message(self, title, message):
        messagebox.showerror(title, message)

    def _on_listbox_select(self, evt):
        if not self.file_loaded:
            return

        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        self.chosen_idx = index
        self._create_grimoire_dataframe()

    def _load_wrapper(self):
        filename = filedialog.askopenfilename(filetypes=[("SAV files", ".sav")])
        if not filename:
            return

        try:
            self.grimoire_data, self.file_hex = uih.load_wrapper(filename)
            self.file_loaded = True
            self.loaded_text.set("File Loaded")
        except Exception:
            self._error_message("Error Loading", "Please verify you're loading the mor1rgame.sav file")
            return
        
        ## Get everything functional
        self.grimoire_choices.set([x for x in range(1, len(self.grimoire_data) + 1)])
        self.save_button["state"] = NORMAL
        self._create_grimoire_dataframe()

        print(len(self.grimoire_data), len(self.file_hex))

    def _create_grimoire_dataframe(self):
        print("Hello!", self.chosen_idx)
        chosen_grimoire = self.grimoire_data[self.chosen_idx]

        ## Skill 1 Name Dropdown
        self.chosen_grimoire_frame = ttk.Frame(self)
        self.chosen_grimoire_frame.grid(row=2, column=2, columnspan=8)

        ## First Skill
        grimoire_skills = sorted([x for x in self.name_id_map.keys()])

        skill0_name_label = ttk.Label(
            self.chosen_grimoire_frame, text="Skill #1:"
        )
        skill0_name_label.grid(row=0, column=0)
        self.skill0_option_var = StringVar(self.chosen_grimoire_frame)
        skill0_name_dropdown = AutocompleteCombobox(
            self.chosen_grimoire_frame,
            textvariable=self.skill0_option_var
        )
        skill0_name_dropdown.set_completion_list(grimoire_skills)
        skill0_name_dropdown["values"] = grimoire_skills
        # skill0_name_dropdown["state"] = "readonly"
        skill0_name_dropdown.bind('<<ComboboxSelected>>', self._update_grim_skill0)
        self.skill0_option_var.set(chosen_grimoire["skills"][0]["name"])
        skill0_name_dropdown.grid(row=0, column=1)

        self.skill0_level_var = StringVar(self.chosen_grimoire_frame)
        skill0_level_entry = ttk.OptionMenu(
            self.chosen_grimoire_frame,
            self.skill0_level_var,
            *[x for x in range(1, 11)],
            command=self._update_grim_level0
        )
        self.skill0_level_var.set(chosen_grimoire["skills"][0]["level"])
        skill0_level_entry.grid(row=0, column=2)

    def _update_grim_skill0(self, event):
        self._update_grimoire_skills(0, self.skill0_option_var.get())

    def _update_grim_level0(self, event):
        self._update_grimoire_levels(0, event)

    def _update_grimoire_levels(self, index, new_level):
        self.grimoire_data[self.chosen_idx]["skills"][index]["level"] = new_level
        self.grimoire_data[self.chosen_idx]["skills"][index]["level_hex"] = [str(new_level).zfill(2), "00"]

        print(self.grimoire_data[self.chosen_idx]["skills"][index])

    def _update_grimoire_skills(self, index, new_name):
        self.grimoire_data[self.chosen_idx]["skills"][index]["name"] = new_name
        self.grimoire_data[self.chosen_idx]["skills"][index]["_id"] = self.name_id_map[new_name]

        print(self.grimoire_data[self.chosen_idx]["skills"][index])

    def _save_wrapper(self):
        if not self.file_loaded:
            self._error_message("Error Saving", "Can't save if you haven't loaded...")
            return

        uih.save_wrapper(self.file_hex, self.grimoire_data)
 
root = Root()
root.mainloop()