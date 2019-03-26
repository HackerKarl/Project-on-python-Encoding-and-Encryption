
from tkinter import *
from tkinter import messagebox
import os


alphavit = ["а","б","в","г","ґ","д",
      "е","є","ж","з","	и","і",
      "ї","й","к","л","м","н",
      "о","п","р","с","т","у",
      "ф","х","ц","ч","ш","щ",
      "ь","ю","я"]

root = Tk()
root.title('Gui Python')


coder_text = StringVar()


main_menu = Menu()
сoding_main_menu = Menu()
encryption_main_menu = Menu()

def message_box():
    messagebox.showinfo("Programm", coder_text.get())
   
def clear_entry():
   Edit1.delete(0, END)

def vishener_table():
   root = Tk()
   root.title('Алфавит')
   root.geometry("640x480")
   labelImg = Label(root, text = 'fgfgfg')
   root.mainloop

def coding():
   symbol = e1.get()
   if symbol not in alphavit:
      l3.config(text = "Такой символ не сушествует")
   else:
      inc = alphavit.index(symbol) + 1
      coder = alphavit[inc]
   if inc > 32:
      coder = alphavit[inc - 33]
      l3.config(text = "Закодированый символ - " + " "+ coder)
   else:
      coder = alphavit[inc]
      l3.config(text = "Закодированый символ - " + " "+ coder)

def Caesar():
   global e1, l3
   root = Tk()
   root.title("Цезарь")
   root.geometry("210x140")
   l1 = Label(root, text = "Код Цезаря", fg = "red")
   l1.place(x = 40, y = 0)
   l2 = Label(root, text = "Введите символ")
   l2.place(x = 0, y = 30)
   e1 = Entry(root, width = 10)
   e1.place(x = 100, y = 30)
   l3 = Label(root, text = "закодированый символ - ", fg = "blue")
   l3.place(x = 0, y = 60)
   b1 = Button(root, text = "Закодировать", command = coding)
   b1.place(x = 60, y = 90)
   root.mainloop()

def Haffman_algorithm():
   source = 'Haffman.py'
   open_file = "python3 {}".format(source)
   os.system(open_file)
   
def Lzw_algorithm():
   source = 'lzw.py'
   open_file = "python3 {}".format(source)
   os.system(open_file)

def Caesar_algorithm():
   source = 'Ceasar.py'
   open_file = "python3 {}".format(source)
   os.system(open_file)
   
def donate():
   messagebox.showinfo("Donate", "По 100 грн для Ярика")

main_menu.add_cascade(label = "Кодирование", menu = сoding_main_menu)
main_menu.add_cascade(label = "Шифрование", menu = encryption_main_menu)
сoding_main_menu.add_command(label = "ShanonFano")
сoding_main_menu.add_command(label = "Haffman", command = Haffman_algorithm)
сoding_main_menu.add_command(label = "LZW", command = Lzw_algorithm)
сoding_main_menu.add_command(label = "BWT")
encryption_main_menu.add_command(label = "Wizhener", command = vishener_table)
encryption_main_menu.add_command(label = "Цезарь", command = Caesar)
encryption_main_menu.add_command(label = "Цеазрь 2.0", command = Caesar_algorithm)

Label(text = 'Просто прокольная программа', font = "courier 14 bold").grid(row = 0, pady = (0,20))
Button(text = "На развите проекта", command = donate).grid(row = 1)

root.config(menu = main_menu)
root.resizable(height = False, width = False )
root.minsize(width=250, height=100)
root.mainloop()