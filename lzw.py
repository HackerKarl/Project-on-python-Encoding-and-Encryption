from tkinter import *

class Application(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.grid()

        Label(master, text = 'Сжатие методом LZW', font = "courier 14 bold").grid(row = 0, columnspan = 3, pady = (0,20))
        self.label_for_text = Label(master, text = "Оригинальный текст")
        self.label_for_text.grid(row = 1, column = 0, pady = (5,5))

        self.text = Text(master, width = 50, height = 10)
        self.text.grid(row = 2, padx = 10, pady = 10)
        
        Button(master, text = "Нажать для магии", command = self.compress).grid(row = 3)
        
        
        self.label_for_binary_text  = Label( master, width = 50, text = 'Закодированный текст')
        self.label_for_binary_text.grid(row = 4, column = 0, pady = (25,10)) 

        self.text_binary = Text(master, width = 50, height = 10)
        self.text_binary.grid(row = 5, column = 0)

        Button(master, text = "Clear", command = self.clear_label).grid(row = 6)

    def clear_label(self):
        self.text.delete(1.0, END)
        self.text_binary.delete(1.0, END)

    def compress(self):
        input_text = self.text.get(1.0, END)
        size = 256
        dictionary = {chr(i):i for i in range(size)}
        w = ""
        self.result = []
        for c in input_text:
            wc  = w + c
            if wc in dictionary:
                w = wc
            else:
                self.result.append(dictionary[w])
                dictionary[wc] = size
                size += 1
                w = c
        if w:
            self.result.append(dictionary[w])
            self.text_binary.insert(END, self.result)


root = Tk()
root.config(bd=10)
root.option_add("*Font", "courier")
root.wm_title('LZW Algorithm')
root.minsize(width=550, height=650)
root.resizable(width=False, height=False)
app = Application(master=root)
app.mainloop()