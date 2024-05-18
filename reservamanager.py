import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import basededatos as bd
import sqlite3

class ReservaManagerApp:
    def __init__(self,contieneformulario,contienedatos):
        self.master = contieneformulario
        #self.master.title("Servicios Manager")
        self.db = bd.DatabaseManager('Habilidades.sqlite')
        self.contienedatos = contienedatos
        self.create_widgets()

    def create_widgets(self):
        conexion = sqlite3.connect("Habilidades.sqlite")
        global cursor
        cursor = conexion.cursor()
##        contienedatos = ttk.LabelFrame(
##            self.master,
##            text="Datos en mi sistema",
##            borderwidth=1,
##            width=600,
##            relief="ridge"
##        )
##        contienedatos.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        global arbol
        arbol = ttk.Treeview(self.contienedatos)
        arbol['columns'] = ("nombre", "apellidos",)
        arbol.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        arbol.heading("#0", text="Columna 0")
        arbol.heading("nombre", text="Nombre")
        arbol.heading("apellidos", text="Apellidos")
        arbol.column("#0", width=0 ,anchor="center",stretch=tk.NO)
        arbol.column("nombre", width=100,anchor="center")
        arbol.column("apellidos", width=100,anchor="center")

        arbol.insert('', 'end', values=("Jose Vicente", "Carratala"))
        arbol.insert('', 'end', values=("Juan", "Garcia"))
        arbol.insert('', 'end', values=("Jorge", "Lopez"))

        arbol.bind('<Button-1>', self.clickEnArbol)
        #ttk.Button(self.contienedatos, text="Elimina el registro seleccionado", command=self.eliminaRegistro).grid(row=1, column=0,padx=5, pady=5,sticky="nsew")
        mitabla = "Servicios"
        # Vacío el arbol
        for elemento in arbol.get_children():
            arbol.delete(elemento)
        for columna in arbol['columns']:
            arbol.column(columna, width=0)
            arbol.heading(columna, text='')
        # ahora relleno el arbol con los datos que tocan
        cursor.execute(f"PRAGMA table_info({mitabla})")
        columnas = cursor.fetchall()
        listadocolumnas = [columna[1] for columna in columnas]
        print(listadocolumnas)
        arbol['columns'] = listadocolumnas
        #arbol['columna
        for una_columna in listadocolumnas:
            print("***la columan",una_columna)
            arbol.heading(una_columna, text=una_columna)
            arbol.column(una_columna, width=100)
        cursor.execute(f"SELECT * FROM {mitabla}")
        registros = cursor.fetchall()
        for registro in registros:
            arbol.insert('', 'end', values=registro)
       
        # Event List Frame
##        self.event_list_frame = ttk.Frame(self.master)
##        self.event_list_frame.grid(row=0, column=2, padx=10, pady=10)
##
##        self.event_list_label = ttk.Label(self.event_list_frame, text="Events:")
##        self.event_list_label.grid(row=0, column=2, sticky="w")
##
##        self.event_listbox = tk.Listbox(self.event_list_frame, width=50)
##        self.event_listbox.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
##
##        self.refresh_event_list()

        # Reserva Details Frame
        self.reserva_details_frame = ttk.Frame(self.master)
        self.reserva_details_frame.grid(row=0, column=1, padx=5, pady=0)

        self.reserva_details_label = ttk.Label(self.reserva_details_frame, text="Reserva :")
        self.reserva_details_label.grid(row=1, column=0, sticky="w")

        self.reserva_servres_label = ttk.Label(self.reserva_details_frame, text="Servicio Reservado:")
        self.reserva_servres_label.grid(row=2, column=0, sticky="w")
        self.reserva_servres_entry = ttk.Entry(self.reserva_details_frame, width=30)
        self.reserva_servres_entry.grid(row=2, column=1, padx=5, pady=5)

        self.reserva_persres_label = ttk.Label(self.reserva_details_frame, text="Persona Reserva:")
        self.reserva_persres_label.grid(row=3, column=0, sticky="w")
        self.reserva_persres_entry = ttk.Entry(self.reserva_details_frame, width=30)
        self.reserva_persres_entry.grid(row=3, column=1, padx=5, pady=5)

        self.reserva_nif_label = ttk.Label(self.reserva_details_frame, text="NIF :")
        self.reserva_nif_label.grid(row=4, column=0, sticky="w")
        self.reserva_nif_entry = ttk.Entry(self.reserva_details_frame, width=30)
        self.reserva_nif_entry.grid(row=4, column=1, padx=5, pady=5)        

        self.reserva_fechares_label = ttk.Label(self.reserva_details_frame, text="Fecha Reserva:")
        self.reserva_fechares_label.grid(row=5, column=0, sticky="w")
        self.reserva_fechares_entry = ttk.Entry(self.reserva_details_frame, width=30)
        self.reserva_fechares_entry.grid(row=5, column=1, padx=5, pady=5)

        self.reserva_estadores_label = ttk.Label(self.reserva_details_frame, text="Estado Reserva:")
        self.reserva_estadores_label.grid(row=6, column=0, sticky="w")
        ##self.reserva_estadores_entry = ttk.Entry(self.reserva_details_frame, width=30)
        self.reserva_estadores_entry = ttk.Combobox(self.reserva_details_frame, width = 28, values=["pendiente", "confirmada", "anulada", "completada","otro_día"])
        self.reserva_estadores_entry.grid(row=6, column=1, padx=5, pady=10)

        self.add_button = ttk.Button(self.reserva_details_frame, text="Add Reserva", command=self.add_reserva,width=20)
        self.add_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

    def add_reserva(self):
        servicios = self.db.listar_servicio()
        
        serviciores = self.reserva_servres_entry.get()
        personares = self.reserva_persres_entry.get()
        nifres = self.reserva_nif_entry.get()
        fechares = self.reserva_fechares_entry.get()
        estadores = "pendiente"


        for servicio in servicios:
            if serviciores in servicio:
                if servicio[-1] >0:
                    plazas = servicio[-1] -1
                    self.db.update_servplaza(servicio[0],plazas)
                    self.db.create_reserva(serviciores, personares, nifres, fechares, estadores)
                else:
                    messagebox.showinfo("Error", "No hay más plazas para este curso")

        messagebox.showinfo("Success", "Reserva efectuada satisfactoriamente")
        ##self.refresh_event_list()
        self.clear_entries()
        
    def clear_entries(self):
        self.reserva_servres_entry.delete(0, tk.END)
        self.reserva_persres_entry.delete(0, tk.END)
        self.reserva_fechares_entry.delete(0, tk.END)
        self.reserva_nif_entry.delete(0, tk.END)
        self.reserva_estadores_entry.delete(0, tk.END)
        

    def clickEnArbol(self,event):
        messagebox.showinfo("Success", "Registro satisfactorio")

    def eliminaRegistro(self,event):
        messagebox.showinfo("Success", "Registro satisfactorio")

def main():
    root = tk.Tk()
    app = ReservaManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
