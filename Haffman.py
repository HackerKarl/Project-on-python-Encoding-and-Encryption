# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from heapq import heappush, heappop, heapify
import collections


def huffman_encoding(symb2freq):
    
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    
    # преобразование открытого файла для облегчения работы с доннами
    heapify(heap)
        
    while len(heap) > 1:
        
        # la fonction heappop retourne l'element le plus leger d'un tas
        # on recupere les 2 elements les plus legers (i.e. plus faible frequence d'occurence) pour former un nouvel arbre (le plus leger des deux elements est place sur la branche de gauche)
        
        left = heappop(heap)
        rigth = heappop(heap)
        
        # encodage de Huffman: 0 pour la branche de gauche et 1 pour la branche de droite
        # une paire est un tuple (symbole, code_de_Huffman)
        
        for pair in left[1:]:
            pair[1] = '0' + pair[1]
        
        for pair in rigth[1:]:
            pair[1] = '1' + pair[1]
        
        # l'arbre cree est ajoute au tas. Son poids est la somme des frequences d'occurence des caracteres qu'il contient

        heappush( heap, [ left[0] + rigth[0] ] + left[1:] + rigth[1:] )

    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def text2tree(txt):

    symb2freq = collections.Counter(txt)
    huff = huffman_encoding(symb2freq)
    
    return [ ( p[0], symb2freq[p[0]], p[1], int(symb2freq[p[0]])*len(p[1]) ) for p in huff ]




BIN_HEX = {'0000':'0', '0001':'1', '0010':'2', '0011':'3', '0100':'4', '0101':'5',
          '0110':'6', '0111':'7', '1000':'8', '1001':'9', '1010':'A', '1011':'B',
          '1100':'C', '1101':'D', '1110':'E', '1111':'F'}

def bin2hexa(binVal):  
    '''Преобразование строки из двоичной в шестнадцатеричную строку'''
    output = ""
    bits = []
    length = len(binVal)
    if(length%4 != 0):
        for x in range(4-(length%4)):
            binVal += "0"
            length +=1
    for i in range(length//4):
        bits.append(binVal[i*4:(4 + (i*4))])
    for halfByte in bits:
        output+= BIN_HEX[halfByte]
    return output


class Application(Frame):
    """Графическое приложение использует модуль Tkinter."""

    def __init__(self, master=None):
        
        super().__init__(master)
        self.grid()

        # titre de l'application
        Label(master, text='Сжатие методом Хаффмана', font="courier 14 bold").grid(row=0, columnspan=3, pady=(0,20))

        # label du panel
        self.label_for_text  = Label(master, text ="Оригинальный текст" )
        self.label_for_text.grid(row=1, column=0, pady=(5,5))

        # widget text
        self.text = Text(master, width=50, height=10)
        self.text.insert(END, "Текст для сжатия - только символы ascii!")
        self.text.grid(row=2, padx=10, pady=10)

        Button(master, text='Сжать текст', command=self.compute_and_display).grid(row=3)

    
        # panel nord est
        # les resultats du calcul de l'encodage selon Huffamn sont affiches sous forme de tableau (tree dans le vocabulaire tkinter)
        ##################################

        # label du panel
        self.label_for_tree  = Label(master, text ="Подробности кадировки" )
        self.label_for_tree.grid(row=1, column=1, pady=(5,5))

        # creation et mise en forme du tableau
        style = ttk.Style()
        style.configure("Treeview", font=('courier', 10))
        self.tree = ttk.Treeview(master, height=10)
        ysb = ttk.Scrollbar(master, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        self.tree['show'] = 'headings' # ne pas afficher la premiere colonne incluse par defaut
        
        # definition des colonnes
        self.tree["columns"]=("symbole", "frequence", "code", "total_bits")
        
        self.tree.column("symbole", width=100)
        self.tree.column("frequence", width=100)
        self.tree.column("code", width=200)
        self.tree.column("total_bits", width=100)
        
        self.tree.heading("symbole", text="Символ")
        self.tree.heading("frequence", text="Частота")
        self.tree.heading("code", text="Код")
        self.tree.heading("total_bits", text="Всего бит")
        
        self.tree.grid(row=2, rowspan=2, column=1)
        ysb.grid(row=2, rowspan=2, column=2)
        

        # panel sud est
        # Conversion de chaque caractere du texte entre par l'utilisateur vers son code de Huffamn (texte binaire)
        ##################################

        self.label_for_binary_text  = Label( master, width = 50, text = 'Закодированный текст по Хаффману')
        self.label_for_binary_text.grid(row=4, column=1, pady=(25,10)) 

        self.text_binary = Text(master, width=50, height=10)
        self.text_binary.grid(row=5, column=1)


        # panel sud ouest
        # Conversion du texte du panel sud est (texte binaire) en hexastring pour constater la compression en espace
        ##################################

        self.label_for_compressed_text  = Label( master, width = 50, text = 'Сжатый текст')
        self.label_for_compressed_text.grid(row=4, column=0, pady=(25,10))

        self.text_compressed = Text(master, width=50, height=10)
        self.text_compressed.grid(row=5, column=0)

    def compute_and_display(self):
        
        # reset des vues affichant les resultats d'encodage
        self.tree.delete(*self.tree.get_children())
        self.text_compressed.delete('1.0', END)
        self.text_binary.delete('1.0', END)
        text = self.text.get(1.0, 'end-1c') # peut etre vide si presence de caracteres speciaux sur certaines plateformes !
        
        if text:

            self.label_for_text.config(text='Оригинальный текст содержит - {} символов'.format(len(text)))  
            
            matrix = text2tree(text)
            huffman = {}
            text_compressed_total_bits = 0

            for row in matrix:
                # creation d'un dictionnaire pour convertir facilement un caractere en son code de Huffman
                huffman[row[0]] = row[2]
                # cacul du nombre total de bits utilises pour encoder le texte selon Huffman
                text_compressed_total_bits += row[3]
                # mise a jour de l'affichage de l'arbre avec les resultats du calcul
                self.tree.insert('', 'end', values=row)
            

            # mise a jour de l'affichage du panel sud ouest avec le texte encode selon Huffamen et son label indiquant le nombre de caractere 
            
            self.text_binary.insert(END, ''.join([ huffman[char] for char in text]))
            self.label_for_binary_text.config(text='Закодированный текст по Хаффману содержит : {} символов'.format(len(self.text_binary.get(1.0, 'end-1c'))))
            

            # surlignage des 2 premiers caracteres de Huffman pour aider a la comprehension de l'utilisateur

            char_1_huffman_len = len( huffman[ text[0] ] )
            char_2_huffman_len = len( huffman[ text[1] ] )

            self.text_binary.tag_add("huffman_1", "1.0", "1.{}".format(char_1_huffman_len))
            self.text_binary.tag_config("huffman_1", background="yellow")

            self.text_binary.tag_add("huffman_2", "1.{}".format(char_1_huffman_len), "1.{}".format(char_1_huffman_len+char_2_huffman_len))
            self.text_binary.tag_config("huffman_2", background="lightblue")


            # mise a jour de l'affichage du panel sud ouest avec le texte compresse (coversion du texte binaire en texte hexadecimal)

            self.text_compressed.insert(END, bin2hexa(self.text_binary.get(1.0, 'end-1c')))
            self.label_for_compressed_text.config(text='Сжатый текст: {}'.format(len(self.text_compressed.get(1.0, 'end-1c'))//2))

        else:
            # il a ete constate que certaines plateformes ne supportent pas les caracteres speciaux dans le champs texte !
            messagebox.showerror('Ошибка', 'Текст для сжатия не может быть пустым или содержать специальные символы')
            self.text.insert(END, "Напишите здесь текст для сжатия. Только символы ascii !")


# le module tkinter est utilise pour la realisation de l'interface graphique
root = Tk()
# mise en forme de la fenetre principale
root.config(bd=10)
root.option_add("*Font", "courier")
root.wm_title('Huffman')
root.minsize(width=666, height=600)
root.resizable(width=False, height=False)

# lancement de l'interface graprightque
app = Application(master=root)
app.mainloop()