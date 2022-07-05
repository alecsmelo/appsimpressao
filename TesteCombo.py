import tkinter as tk
from tkinter import ttk

lista = ["Coisa 1", "Coisa 2", "Coisa 3"]
lista1 = []

class JanelaPrincipal:

    def __init__(self, master):
        global lista, lista1

        self.master = master
        self.master.geometry("300x300")
        self.master.title("Janela")

        lista = ["Coisa 1", "Coisa 2", "Coisa 3"]
        self.CMB = ttk.Combobox(self.master, values=lista)
        self.CMB.place(x=10, y=10)
        self.CMB.bind('<<ComboboxSelected>>', self.NovoCombo)

        self.CMB2 = ttk.Combobox(self.master, values=lista1)
        self.CMB2.place(x=10, y=60)


        self.LBL = tk.Label(self.master, text=lista1)
        self.LBL.place(x=10, y=90)

    def NovoCombo(self, event):
        global lista1
        pega = event.widget.get()
        lista1 = pega
        print(lista1)



def principal():
    root = tk.Tk()
    app = JanelaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    principal()