"""
Aplicativo Tabulates Exiba
Desenvolvido por Alecsandro Melo
Email: aferreiramelo@gmail.com

Usabilidade: O aplicativo é usado para manter e consultar as medidas das várias tabuletas
da exibidoras Exiba Outdoor, medidas que podem ser utilizadas para produção local ou remota
de materiais como Lonados e Cartazes para Midia Outdoor

Versão: 0.2.5
Data: 20/06/2022 - 21:39
Build: 025
Codename: PítonAmarela

Não proíbo o uso do aplicativo, contudo copiar parte ou a totalidade desse código compõe crime de plágio
"""


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import StringVar
import sqlite3

AreaTotal = float()
AreaVisual = float()

class JanelaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.geometry('220x180+10+10')
        self.master.title('Exiba')
        self.master.iconbitmap('icone.ico')

        #Construção dos Elementos da Janela Princiapal
        self.LBLTitulo = tk.Label(self.master, text="Cadastro de Medidas Tabuletas")
        self.BTNConsulta = tk.Button(self.master, text="Consultar Placa", command=self.ABREConsulta)
        self.BTNCadastra = tk.Button(self.master, text="Cadastrar Placa", command=self.ABRECadastra)

        #Instancioando os Elementos
        self.LBLTitulo.place(x=25, y=100)
        self.BTNConsulta.place(x=12, y=130)
        self.BTNCadastra.place(x=112, y=130)

        self.imagem = tk.PhotoImage(file='logoexiba.png')
        self.IMG = tk.Label(image=self.imagem)
        self.IMG.place(x=30, y=3)

        #Barrinha
        self.LBLBarrinha = tk.Label(self.master, text="PoweredBy: Alecs Melo", font=("Arial", 5))
        self.LBLBarrinha.place(x=10, y=165)
        self.LBLVer = tk.Label(self.master, text="Ver.: 0.2.5", font=("Arial", 5))
        self.LBLVer.place(x=165, y=165)

    #Função dispara nova Janela no Botão Consulta
    def ABREConsulta(self):
        self.JanelaConsulta = tk.Toplevel(self.master)
        self.app = JANConsulta(self.JanelaConsulta)
        self.JanelaConsulta.resizable(0,0)

    #Função dispara nova Janela no Botão Cadastra
    def ABRECadastra(self):
        self.JanelaCadastra = tk.Toplevel(self.master)
        self.app = JANCadastra(self.JanelaCadastra)
        self.JanelaCadastra.resizable(0,0)


#Classe que Cria a Janela Consulta
class JANConsulta:
    def __init__(self, master):

        self.master = master
        self.master.geometry('350x200+230+10')
        self.master.title('Consulta Placa')
        self.master.iconbitmap('icone.ico')

        #Construção dos Elementos

        global LBLSelecione
        LBLSelecione = StringVar()
        LBLSelecione.set("<- Selecione uma Praça")

        self.LBL_CN_Titulo = tk.Label(self.master, text="Consulta de Placas", font=("Arial", 13))
        self.LBL_CN_InfoPraca = tk.Label(self.master, text="Digite a Praça: (JP/CG/PE)")
        self.LBL_CN_TAM_Papel = tk.Label(self.master, text="Tamanho para Papel")
        self.LBL_CN_TAM_Lona = tk.Label(self.master, text="Tamanho para Lonado")

        #Rótulo para Mostrar o Resulta da Pesquia e Exibir os Tamanhos
        self.LBL_CN_Mostra_Papel = tk.Label(self.master, text="00,00m", font=("Arial", 13))
        self.LBL_CN_Mostra_Lona = tk.Label(self.master, text="00,00m", font=("Arial", 13))
        self.LBL_CN_Selecione = tk.Label(self.master, textvariable=LBLSelecione, font=("Arial", 9), fg="red")

        #Aqui vai um pouco de lógica para pegar a listas de placas e as praças
        self.ListaPracas=["João Pessoa", "Campina Grande", "Caruaru"]


        #self.ENT_CN_Placa = ttk.Combobox(self.master, values=self.ListaPlacas) <- Antigo, Preservar por hora
        self.ENT_CN_Praca = ttk.Combobox(self.master, values=self.ListaPracas)
        self.ENT_CN_Praca.bind('<<ComboboxSelected>>', self.GetValorCombo)
        #self.ENT_CN_Praca.current(0)


        self.BTN_CN_Consulta = tk.Button(self.master, text="Consultar Placa", width=12, command=self.Conexao)
        self.BTN_CN_Limpar = tk.Button(self.master, text="Limpar Consulta", width=12, command=self.Limpar)
        self.BTN_CN_Area = tk.Button(self.master, text="Área Total", width=12, command=self.ABREArea)
        
        #Instanciando os Elementos
        self.LBL_CN_Titulo.place(x=105, y=3)
        self.LBL_CN_InfoPraca.place(x=10, y=40)
        self.LBL_CN_Selecione.place(x=165, y=65)
        self.LBL_CN_TAM_Papel.place(x=10, y=90)
        self.LBL_CN_TAM_Lona.place(x=175, y=90)

        #Mostra o Tamanho das Placas depois da consulta do BANCO
        self.LBL_CN_Mostra_Papel.place(x=10, y=105)
        self.LBL_CN_Mostra_Lona.place(x=175, y=105)
        
        #self.ENT_CN_Placa.place(x=10, y=65) <- Antigo preservar por hora
        self.ENT_CN_Praca.place(x=10, y=65)

        self.BTN_CN_Consulta.place(x=30, y=150)
        self.BTN_CN_Limpar.place(x=128, y=150)
        self.BTN_CN_Area.place(x=225, y=150)

    def Conexao(self):
        global AreaTotal, AreaVisual

        self.ENTPlaca = self.ENT_CN_Placa.get()
        self.ENTPraca = self.ENT_CN_Praca.get()

        self.conn = sqlite3.connect('DB_Exiba.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT med_papel, med_lona FROM Placas WHERE placa = ? AND praca = ?", (self.ENTPlaca, self.ENTPraca,))

        for i in self.cursor.fetchall():
            self.LBL_CN_Mostra_Papel['text'] = i[0] + "m"
            self.LBL_CN_Mostra_Lona['text'] = i[1] + "m"
            self.TTotalLocal = float(i[1])+0.50
            self.TVisualLocal = float(i[1])

            AreaTotal = format(self.TTotalLocal, '.2f') #Retorno do valor com Formação Especial para Metro
            AreaVisual = format(self.TVisualLocal, '.2f') #Retorno do valor com Formação Especial para Metro

        self.conn.commit()
        self.conn.close()

    #Pequeno Método para abrir a conexão em outros métodos
    def db_conecta(self):
        self.conn = sqlite3.connect('DB_Exiba.db')
        self.cursor = self.conn.cursor()

    #Pequeno Métado para fechar as conexão abertas pelo método db_conecta
    def db_desconecta(self):
        self.conn.commit()
        self.conn.close()

    #Limpa Labels com Medidas na Tela de Consulta
    def Limpar(self):
        self.LBL_CN_Mostra_Papel['text'] = ""
        self.LBL_CN_Mostra_Lona['text'] = ""

    #Chama Janela com Informaçãoes para o Comercial
    def ABREArea(self):
        self.JanelaArea = tk.Toplevel(self.master)
        self.app = JANAreaTotal(self.JanelaArea)
        self.JanelaArea.resizable(0,0)

    #Função Nova para Mostrar no Combobox das placas somente as placas da praca selecionada
    def GetValorCombo(self, event):

        global LBLSelecione
        LBLSelecione.set("")

        self.ValorCombo = event.widget.get()
        self.ListaPlacas = []

        #Faço uma pequena conexão para retornar os valores do banco de dados
        self.db_conecta() #Abre Conexão
        self.Lista= self.cursor.execute("SELECT placa FROM Placas WHERE praca = ?", (self.ValorCombo,))

        #Pega tudo que tá no cursor do select intera e coloca no novo ComboBox
        self.listagem = self.cursor.fetchall()
        for i in self.listagem:
            self.ListaPlacas.append(i[0])

        #Aqui fecho essa conexão
        self.db_desconecta() #Fecha Conexão
        self.LBL_CN_InfoPlaca = tk.Label(self.master, text="Digite a Placa: 000A+000B")
        self.ENT_CN_Placa = ttk.Combobox(self.master, values=self.ListaPlacas)
        self.ENT_CN_Placa.place(x=180, y=65)
        self.LBL_CN_InfoPlaca.place(x=180, y=40)

# Classe para criar um TopLevel para Exibir um texto pronto com as configs das placas
class JANAreaTotal:
    def __init__(self, master):
        global AreaTotal, AreaVisual

        self.master = master
        self.master.geometry('350x150+230+240')
        self.master.title('Área Total')
        self.master.iconbitmap('icone.ico')

        #Infomações que serão repassadas ao comercial
        self.ESPArea = "*Área Total:* " + str(AreaTotal) +"m" + " x 3.70m" + '\n'\
                       + "*Área Visual:* " + str(AreaVisual) + "m" +" x 3.48m" + '\n'\
                       + "*Acabamento:* Sem Acabamento" + '\n'\
                       + "*Material:* LonaFront 280g, 340g ou 380g" + '\n'\
                       + "*Especificação:* LonaFront Grande Formato" + '\n'\
                       + "*Observação:* Deixar sobra para estique"

        self.LBL_A_Lona = tk.Label(self.master, text="Especificações para Produção de Lona")
        self.LBL_A_Lona.place(x=10, y=10)

        self.Configs = tk.Text(self.master, width=41, height=6)
        self.Configs.place(x=10, y=40)
        self.Configs.insert(tk.END, self.ESPArea)


#Classe que Cria a Janela Consulta
class JANCadastra:
    def __init__(self, master):
        self.master = master
        self.master.geometry('350x200+230+10')
        self.master.title('Cadastra Placa')
        self.master.iconbitmap('icone.ico')

        #Construção dos Elemtnso da Janela Cadastra
        self.LBL_C_Titulo = tk.Label(self.master, text="Cadastro de Placas no Sistema", font=("Arial", 13))
        self.LBL_C_InfoPlaca = tk.Label(self.master, text="Digite a Placa: 000A + 000B")
        self.LBL_C_InfoPraca = tk.Label(self.master, text="Digite a Praça: (JP/CG/PE)")
        self.LBL_C_TAM_Papel = tk.Label(self.master, text="Tamanho para Papel")
        self.LBL_C_TAM_Lona = tk.Label(self.master, text="Tamanho para Lonado")

        self.ListaPracas = ["João Pessoa", "Campina Grande", "Caruaru"]

        self.ENT_C_Placa = tk.Entry(self.master, width=25)
        self.ENT_C_Praca = ttk.Combobox(self.master, values=self.ListaPracas, width=22)
        self.ENT_C_TAM_Papel = tk.Entry(self.master, width=25)
        self.ENT_C_TAM_Lonado = tk.Entry(self.master, width=25)

        self.BTN_C_Cadastrar = tk.Button(self.master, text="Cadastrar Placa", width=20, command=self.CADConexao)
        self.BTN_C_Atualizar = tk.Button(self.master, text="Atualizar Placa", width=20, command=self.CADAtualiza)

        #Instanciando os Elementos
        self.LBL_C_Titulo.place(x=60, y=3)
        self.LBL_C_InfoPlaca.place(x=10, y=40)
        self.LBL_C_InfoPraca.place(x=180, y=40)
        self.LBL_C_TAM_Papel.place(x=10, y=90)
        self.LBL_C_TAM_Lona.place(x=175, y=90)

        self.ENT_C_Placa.place(x=10, y=65)
        self.ENT_C_Praca.place(x=180, y=65)
        self.ENT_C_TAM_Papel.place(x=180, y=110)
        self.ENT_C_TAM_Lonado.place(x=10, y=110)

        self.BTN_C_Cadastrar.place(x=22, y=150)
        self.BTN_C_Atualizar.place(x=172, y=150)


    def CADConexao(self):
        self.conn = sqlite3.connect('DB_Exiba.db')
        self.cursor = self.conn.cursor()

        self.ENTPlc = self.ENT_C_Placa.get()
        self.ENTPrc = self.ENT_C_Praca.get()
        self.ENTTPapel = self.ENT_C_TAM_Papel.get()
        self.ENTTLona = self.ENT_C_TAM_Lonado.get()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Placas(
                                placa text,
                                praca text,
                                med_papel blob,
                                med_lona blob
                                )''')
    
        self.cursor.execute("INSERT INTO Placas VALUES (?,?,?,?)",(self.ENTPlc, self.ENTPrc, self.ENTTLona, self.ENTTPapel))
        messagebox.showinfo(title="Placa Salva", message="Nova Placa Cadastrada!")

           
        self.conn.commit()
        self.conn.close()

    #Método para Atualizar os tamanhos de determinada placa no banco de dados
    def CADAtualiza(self):
        self.conn = sqlite3.connect('DB_Exiba.db')
        self.cursor = self.conn.cursor()

        self.ENTPlc = self.ENT_C_Placa.get()
        self.ENTTPapel = self.ENT_C_TAM_Papel.get()
        self.ENTTLona = self.ENT_C_TAM_Lonado.get()

        self.cursor.execute("UPDATE Placas SET med_papel = ?,  med_lona = ? WHERE placa = ?",(self.ENTTLona, self.ENTTPapel, self.ENTPlc))
        messagebox.showinfo(title="Placa Atualizada", message="Placa " + self.ENTPlc + " foi atualizada")

        self.conn.commit()
        self.conn.close()
        



 

#Finalizando Tudo e Chamando o MainLoop       
def Principal():
    root = tk.Tk()
    app = JanelaPrincipal(root)
    root.resizable(0,0)
    root.mainloop()

if __name__ == "__main__":
    Principal()
        

