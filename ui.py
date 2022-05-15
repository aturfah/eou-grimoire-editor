from tkinter import *
from tkinter import ttk

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
        load_button = ttk.Button(text="Load File")
        load_button.grid(row=1, column=0)
        save_button = ttk.Button(text="Save File")
        save_button.grid(row=1, column=2)

 
root = Root()
root.mainloop()