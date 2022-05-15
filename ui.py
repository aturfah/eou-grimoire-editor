from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox


import ui_helpers as uih

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
        header.grid(row =0, column=1, padx=5,pady=5)

        ## Get load/save buttons ready
        self.buttonframe = Frame(self)
        self.buttonframe.grid(row=1, column=0, columnspan=2)
        self.load_button = ttk.Button(text="Load File", command=self._load_wrapper)
        self.load_button.grid(row=1, column=1)
        self.save_button = ttk.Button(text="Save File", state=DISABLED, command=self._save_wrapper)
        self.save_button.grid(row=1, column=3)

        ## This text determines if loaded
        self.file_loaded = False
        self.loaded_text = StringVar()
        self.loaded_text.set("No File Loaded")
        self.loaded_label = Label(self, textvariable=self.loaded_text)
        self.loaded_label.grid(row=2, column=1)

        ## Get the grimoire listbox
        self.grimoire_choices = StringVar(value=[])
        self.grimoire_disp_list = Listbox(self, listvariable=self.grimoire_choices, height=15)
        self.grimoire_disp_list.grid(row=3, column=1)

        ## Set the Grimoire variables
        self.file_hex = None
        self.grimoire_data = []
        self.name_id_map = uih.name_id_map()

    def _error_message(self, title, message):
        messagebox.showerror(title, message)

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

        print(len(self.grimoire_data), len(self.file_hex))

    def _save_wrapper(self):
        if not self.file_loaded:
            self._error_message("Error Saving", "Can't save if you haven't loaded...")
            return

        uih.save_wrapper(self.file_hex, self.grimoire_data)
 
root = Root()
root.mainloop()