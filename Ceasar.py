from tkinter import *

class Application(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.grid()

root = Tk()
root.config(bd = 10)
root.option_add("*Font", "courier")
root.wm_title('Caeasar Algorithm')
root.minsize(width = 550, height = 650)
root.resizable(width = False, height = False)
app = Application(master = root)
app.mainloop()