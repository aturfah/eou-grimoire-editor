from tkinter import *
 
class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
 
        self.title("Python Tkinter")
        self.minsize(500,400)
 
root = Root()
root.mainloop()