from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox

from pprint import pprint

import ui_helpers as uih
from tkinter_complete import AutocompleteCombobox, AutocompleteEntry

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
        print("Now chosen Grimoire #{}".format(index+1))

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

        print("Successfully loaded {}".format(filename))

    def _create_grimoire_dataframe(self):
        chosen_grimoire = self.grimoire_data[self.chosen_idx]

        self.chosen_grimoire_frame = ttk.Frame(self)
        self.chosen_grimoire_frame.grid(row=2, column=2, rowspan=8)

        ## Make the Grimoire type dropdown
        grimoire_class_frame = ttk.Frame(self.chosen_grimoire_frame)
        grimoire_class_frame.grid(row=0, column=0, columnspan=2)
        grimoire_class_label = ttk.Label(
            grimoire_class_frame, text="Class:"
        )
        grimoire_class_label.grid(row=0, column=0)

        grimoire_class_var = StringVar()
        grimoire_class_dropdown = ttk.OptionMenu(
            grimoire_class_frame,
            grimoire_class_var,
            "",
            *list(uih.class_id_map()),
            command=lambda e: self._update_grim_class(e)
        )
        grimoire_class_var.set(chosen_grimoire["class"])
        grimoire_class_dropdown.grid(row=0, column=1)

        ## Make Creator name dropdown
        grimoire_generator_frame = self.chosen_grimoire_frame
        # grimoire_generator_frame.grid(row=1, column=0, columnspan=2)
        grimoire_generator_label = ttk.Label(
            grimoire_generator_frame, text="Generator:"
        )
        grimoire_generator_label.grid(row=1, column=0)

        self.grimoire_generator_var = StringVar(
            grimoire_generator_frame)
        grimoire_generator_entry = ttk.Entry(
            grimoire_generator_frame,
            textvariable=self.grimoire_generator_var
        )
        grimoire_generator_entry.bind("<Return>", lambda e: self._update_grim_generator_field())
        self.grimoire_generator_var.set(chosen_grimoire["name"])
        grimoire_generator_entry.grid(row=1, column=1)

        self.grimoire_unknown_flag = BooleanVar(grimoire_generator_frame)
        """
        grimoire_unknown_var = ttk.Checkbutton(
            grimoire_generator_frame,
            variable=self.grimoire_unknown_flag,
            onvalue=False, offvalue=True,
            text="Known Origin")
        self.grimoire_unknown_flag.set(chosen_grimoire["unknown_origin"])
        grimoire_unknown_var.grid(row=1, column=2)
        """

        ## Make the skill dropdowns
        skill_dropdown_offset = 2
        grimoire_skills = sorted([x for x in self.name_id_map.keys()])
        self.skill1_option_var = StringVar(self.chosen_grimoire_frame)
        self.skill2_option_var = StringVar(self.chosen_grimoire_frame)
        self.skill3_option_var = StringVar(self.chosen_grimoire_frame)
        self.skill4_option_var = StringVar(self.chosen_grimoire_frame)
        self.skill5_option_var = StringVar(self.chosen_grimoire_frame)
        self.skill6_option_var = StringVar(self.chosen_grimoire_frame)
        self.skill7_option_var = StringVar(self.chosen_grimoire_frame)

        self.option_vars = [
            self.skill1_option_var,
            self.skill2_option_var,
            self.skill3_option_var,
            self.skill4_option_var,
            self.skill5_option_var,
            self.skill6_option_var,
            self.skill7_option_var
        ]

        skill_update_lambdas = {
            0: lambda e: self._update_grimoire_skills(0, self.option_vars[0].get()),
            1: lambda e: self._update_grimoire_skills(1, self.option_vars[1].get()),
            2: lambda e: self._update_grimoire_skills(2, self.option_vars[2].get()),
            3: lambda e: self._update_grimoire_skills(3, self.option_vars[3].get()),
            4: lambda e: self._update_grimoire_skills(4, self.option_vars[4].get()),
            5: lambda e: self._update_grimoire_skills(5, self.option_vars[5].get()),
            6: lambda e: self._update_grimoire_skills(6, self.option_vars[6].get()),
        }

        level_update_lambdas = {
            0: lambda e : self._update_grimoire_levels(0, e),
            1: lambda e : self._update_grimoire_levels(1, e),
            2: lambda e : self._update_grimoire_levels(2, e),
            3: lambda e : self._update_grimoire_levels(3, e),
            4: lambda e : self._update_grimoire_levels(4, e),
            5: lambda e : self._update_grimoire_levels(5, e),
            6: lambda e : self._update_grimoire_levels(6, e)
        }

        for idx in range(7):
            idx = int(idx)
            skill_name_label = ttk.Label(
                self.chosen_grimoire_frame, text="Skill #{}:".format(idx+1)
            )
            skill_name_label.grid(row=idx+skill_dropdown_offset, column=0)

            skill_name_dropdown = AutocompleteEntry(
            # skill_name_dropdown = AutocompleteCombobox(
                self.chosen_grimoire_frame,
                textvariable=self.option_vars[idx]
            )
            skill_name_dropdown.set_completion_list(grimoire_skills)
            # skill_name_dropdown["values"] = grimoire_skills
            # skill_name_dropdown.bind("<<ComboboxSelected>>",
                # skill_update_lambdas[idx])
            skill_name_dropdown.bind("<Return>", skill_update_lambdas[idx])
            self.option_vars[idx].set(chosen_grimoire["skills"][idx]["name"])
            skill_name_dropdown.grid(row=idx+skill_dropdown_offset, column=1)

            skill_level_var = StringVar(self.chosen_grimoire_frame)
            skill_level_entry = ttk.OptionMenu(
                self.chosen_grimoire_frame,
                skill_level_var,
                *[x for x in range(-1, 11)],
                command=level_update_lambdas[idx]
            )
            skill_level_var.set(chosen_grimoire["skills"][idx]["level"])
            skill_level_entry.grid(row=idx+skill_dropdown_offset, column=2)

    def _update_grim_generator_field(self):
        new_name = self.grimoire_generator_var.get()
        self.grimoire_data[self.chosen_idx]["name"] = new_name
        self.grimoire_data[self.chosen_idx]["name_hex"] = uih.ascii_to_hex(new_name)
        if new_name:
            self.grimoire_data[self.chosen_idx]["unknown_origin"] = False
            self.grimoire_data[self.chosen_idx]["class_hex"][0] = "00"
            self.grimoire_unknown_flag.set(False)
        else:
            self.grimoire_data[self.chosen_idx]["unknown_origin"] = True
            self.grimoire_data[self.chosen_idx]["class_hex"][0] = "30"
            self.grimoire_unknown_flag.set(True)

        print("Grimoire #{gidx} Generator now {name}; Unknown Origin: {unk}".format(
            gidx=self.chosen_idx+1, name=new_name, unk=self.grimoire_unknown_flag.get()
        ))
        self._create_grimoire_dataframe()


    def _update_grim_class(self, new_class):
        self.grimoire_data[self.chosen_idx]["class"] = new_class
        self.grimoire_data[self.chosen_idx]["class_hex"][1] = uih.class_id_map()[new_class]

        print("Grimoire #{gidx} Class now {cls}".format(
            gidx=self.chosen_idx+1, cls=new_class
        ))
        self._create_grimoire_dataframe()

    def _update_grimoire_levels(self, index, new_level):
        self.grimoire_data[self.chosen_idx]["skills"][index]["level"] = new_level
        self.grimoire_data[self.chosen_idx]["skills"][index]["level_hex"] = [format(new_level, 'x').zfill(2), "00"]

        print("Grimoire #{gidx} Skill #{sidx} Level now {lvl}".format(
            gidx=self.chosen_idx+1, sidx=index+1, lvl=new_level
        ))
        self._create_grimoire_dataframe()

    def _update_grimoire_skills(self, index, new_name):
        if new_name == "" or new_name == "Blank":
            new_name = "Blank"
            self.option_vars[index].set(new_name)
            self._update_grimoire_levels(index, 0)
        
        old_name = str(self.grimoire_data[self.chosen_idx]["skills"][index]["name"])

        self.grimoire_data[self.chosen_idx]["skills"][index]["name"] = new_name
        self.grimoire_data[self.chosen_idx]["skills"][index]["_id"] = self.name_id_map[new_name]

        print("Grimoire #{gidx} Skill #{sidx} Skill now {skl}".format(
            gidx=self.chosen_idx+1, sidx=index+1, skl=new_name
        ))

        if old_name == "Blank":
            self._update_grimoire_levels(index, 1)
        else:
            self._create_grimoire_dataframe()


    def _save_wrapper(self):
        if not self.file_loaded:
            self._error_message("Error Saving", "Can't save if you haven't loaded...")
            return

        output_file = filedialog.asksaveasfilename(
            initialfile = 'mor1rgame.sav',
            confirmoverwrite=True)

        uih.save_wrapper(self.file_hex, self.grimoire_data, output_file)
 
root = Root()
root.mainloop()