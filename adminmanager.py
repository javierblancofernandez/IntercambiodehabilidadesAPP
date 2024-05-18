import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import basededatos as bd
import sqlite3


##class AdminManagerApp:
class AdminManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Administrador Manager")
        self.bd = bd.DatabaseManager('Habilidades.sqlite')
        #self.cursor = self.bd.cursor()

        # Initialize event manager widgets here
        self.create_widgets()

    def create_widgets(self):
        conexion = sqlite3.connect("Habilidades.sqlite")
        global cursor
        cursor = conexion.cursor()
        Style(theme='minty')
        
        contienetablas = ttk.LabelFrame(
            self.master,
            text="Tablas en la BBDD",
            borderwidth=1,
            width=100,
            relief="ridge"
        )
        contienetablas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        for tabla in tablas:
            print(tabla)
            if(tabla[0]!= 'events' and tabla[0]!= 'sqlite_sequence' and tabla[0]!= 'EstadoReserva'):
                ttk.Button(contienetablas, text=tabla[0], width=10, command=lambda tabla=tabla[0]: self.seleccionaTabla(tabla)).pack(
                    padx=10, pady=10)
        global contieneformulario
        contieneformulario = ttk.LabelFrame(
            self.master,
            text="Formulario de inserción",
            borderwidth=1,
            width=100,
            relief="ridge"
        )
        contieneformulario.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        cursor.execute("PRAGMA table_info(productos)")
        columnas = cursor.fetchall()
        for columna in columnas:
            print('columna',columna)
            ttk.Label(contieneformulario, text=columna[1]).pack(padx=5, pady=5)
            ttk.Entry(contieneformulario).pack(padx=5, pady=5)

        contienedatos = ttk.LabelFrame(
            self.master,
            text="Datos en mi sistema",
            borderwidth=1,
            width=600,
            relief="ridge"
        )
        contienedatos.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        global arbol
        arbol = ttk.Treeview(contienedatos)
        arbol['columns'] = ("nombre", "apellidos",)
        arbol.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        arbol.heading("#0", text="Columna 0")
        arbol.heading("nombre", text="Nombre")
        arbol.heading("apellidos", text="Apellidos")
        arbol.column("#0", width=0 ,anchor="center",stretch=tk.NO)
        arbol.column("nombre", width=100,anchor="center")
        arbol.column("apellidos", width=100,anchor="center")

        arbol.insert('', 'end', values=("", ""))
        arbol.insert('', 'end', values=("", ""))
        arbol.insert('', 'end', values=("", ""))

        arbol.bind('<Button-1>', self.clickEnArbol)
        ttk.Button(contienedatos, text="Elimina el registro seleccionado", command=self.eliminaRegistro).grid(row=1, column=0,padx=5, pady=5,sticky="nsew")

    def seleccionaTabla(self,mitabla):
        global listacampos, tablaactual,columnas
        tablaactual = mitabla
##        print("Has pulsado la tabla de:", mitabla)
        for widget in contieneformulario.winfo_children():
            widget.destroy()
        cursor.execute(f"PRAGMA table_info({mitabla})")
        columnas = cursor.fetchall()
        listacampos = []
        for columna in columnas:
            print('columna',columna)
            if(columna[1]!='Estado_Reserva'):
                ttk.Label(contieneformulario, text=columna[1]).pack(padx=5, pady=5)
                listacampos.append(ttk.Entry(contieneformulario))
                listacampos[-1].pack(padx=5, pady=5)
            else:
                ttk.Label(contieneformulario, text=columna[1]).pack(padx=5, pady=5)
                listacampos.append(ttk.Combobox(contieneformulario, width = 27, values=["pendiente", "confirmada", "anulada", "completada","otro_día"]))
                listacampos[-1].pack(padx=5, pady=5)
        ttk.Button(contieneformulario, text="Insertar", command=self.insertaBaseDatos).pack(padx=5, pady=5)
        ttk.Button(contieneformulario, text="Actualizar", command=self.actualizaBaseDatos).pack(padx=5, pady=5)
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
##        print(listadocolumnas)
        arbol['columns'] = listadocolumnas
        #arbol['columna
        for una_columna in listadocolumnas:
            #print("***la columna",una_columna)
            arbol.heading(una_columna, text=una_columna)
            arbol.column(una_columna, width=100)
        cursor.execute(f"SELECT * FROM {mitabla}")
        registros = cursor.fetchall()
        for registro in registros:
            arbol.insert('', 'end', values=registro)

    def clickEnArbol(self,event):
        global identificador_seleccionado,elemento
        #print("Has hecho click en el arbol")
        elemento = arbol.identify('item', event.x, event.y)
        arbol.selection_set(elemento)
        print(elemento)
        valores = arbol.item(elemento, 'values')
##        print("estos son los campos:",listacampos)
        print(valores)
        #primero vaciamos
        for campo in range(0, len(listacampos)):
            listacampos[campo].delete(0,tk.END)
        # Insertamos los valores en los campos
        for campo, valor in zip(listacampos, valores):
            try:
                campo.insert(0, valor)
            except IndexError as e:
                print("Error al insertar en el campo:", e)
                messagebox.showerror("Error", f"Error al insertar en el campo: {e}")
        
        try:
            identificador_seleccionado = valores[0]
        except IndexError as e:
            print("Error al acceder al identificador seleccionado:", e)
            messagebox.showerror("Error", f"Error al acceder al identificador seleccionado: {e}")

    def eliminaRegistro(self):
        conexion = sqlite3.connect("Habilidades.sqlite")
        global tablaactual, identificador_seleccionado,cursor
        cursor = conexion.cursor()
##        print("Voy a eliminar el registro que está seleccionado")
##        print("La tabla seleccionada es:", tablaactual)
##        print("El identificador seleccionado es:", identificador_seleccionado)
        peticion = f"DELETE FROM {tablaactual} WHERE id = {identificador_seleccionado};"
        print(peticion)
        cursor.execute(peticion)
        conexion.commit()
        self.seleccionaTabla(tablaactual)
        
    def insertaBaseDatos(self):
        conexion = sqlite3.connect("Habilidades.sqlite")
        global cursor
        cursor = conexion.cursor()
        print("Insertamos en la base de datos")
        print("estos son los campos:",listacampos)
        peticion = "INSERT INTO " + tablaactual + " VALUES (NULL,"
        
        for campo in range(0, len(listacampos)):
            if campo != 0:
                peticion += "'" + listacampos[campo].get() + "',"
        peticion = peticion[:-1]
        peticion += ")"
        print(peticion)
        cursor.execute(peticion)
        conexion.commit()
        self.seleccionaTabla(tablaactual)
        
    def actualizaBaseDatos(self):
        conexion = sqlite3.connect("Habilidades.sqlite")
        global cursor
        cursor = conexion.cursor()
        print("Insertamos en la base de datos")
        print("estos son los campos:",listacampos)
            
        peticion = "UPDATE " + tablaactual + " SET "
        # Recorre cada tupla en columnas y agrega solo el segundo valor a la petición
        i = 1
        for columna in columnas:
            if str(columna[1])!='id':
                peticion +=  str(columna[1]) + "='"+listacampos[i].get()+"',"
                i = i+1
        peticion = peticion[:-1]  # Elimina la última coma
        peticion += " WHERE id="+listacampos[0].get()+";"

        print(peticion)
        cursor.execute(peticion)
        conexion.commit()
        self.seleccionaTabla(tablaactual)
        
def main():
    root = tk.Tk()
    app = AdminManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
