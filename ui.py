from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import ui_helpers as uih

class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
 
        self.title("Etrian Odyssey Untold - Grimoire Editor")
        self.minsize(500,400)

        ## Prepare label
        header = ttk.Label(
            self,
            text="Hello, Tkinter",
            anchor=CENTER)
        header.config(font=("EOU Grimoire Editor", 16))
        header.grid(row =0, column=1, padx=5,pady=5)

        ## Get load/save buttons ready
        self.buttonframe = Frame(self)
        self.buttonframe.grid(row=1, column=0, columnspan=2)
        load_button = ttk.Button(text="Load File", command=self.load_wrapper)
        load_button.grid(row=1, column=0)
        save_button = ttk.Button(text="Save File", command=self.save_wrapper)
        save_button.grid(row=1, column=2)

        ## Set the variables
        self.file_hex = None
        self.grimoire_data = []
        self.name_id_map = uih.name_id_map()

    def load_wrapper(self):
        filename = filedialog.askopenfilename(filetypes=[("SAV files", ".sav")])
        if not filename:
            return

        try:
            self.grimoire_data, self.file_hex = uih.load_wrapper(filename)
        except Exception:
            pass

        print(len(self.grimoire_data), len(self.file_hex))

    def save_wrapper(self):
        uih.save_wrapper(self.file_hex, self.grimoire_data)
 
root = Root()
root.mainloop()