import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import basededatos as bd
import pruebaeventos as pe
import serviciomanager as serv
import reservamanager as reserva
import mireservamanager as mireserva

class ControlManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu de Control")
        self.db = bd.DatabaseManager('Habilidades.sqlite')
        self.create_menu_layout()
            
    def create_menu_layout(self):
        ##menu_frame = ttk.Frame(self.master)
        contienetablas = ttk.LabelFrame(
            self.master,
            text="Elige tu opción:",
            borderwidth=1,
            width=100,
            relief="ridge"
        )
        contienetablas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        #menu_frame.pack(padx=20, pady=20)

        nombre = "PersonaServicio"
        nombre1= "Servicio"
        nombre2= "ReservaServicio"
        nombre3= "MiReserva"
        nombre1= "Servicio"
        #messagebox.showinfo("Información", f"Opening Events Page y el boton se llama {nombre}")

        events_button = ttk.Button(contienetablas, text="PersonaServicio", command=lambda nombre = "PersonaServicio":self.open_events_page(nombre),width=20)
        events_button.grid(row=0, column=0, padx=10, pady=10)
        events_button = ttk.Button(contienetablas, text="Servicio", command=lambda nombre1 = "Servicio":self.open_events_page(nombre1),width=20)
        events_button.grid(row=1, column=0, padx=10, pady=10)
        events_button = ttk.Button(contienetablas, text="Reserva", command=lambda nombre = "Reserva":self.open_events_page(nombre2),width=20)
        events_button.grid(row=2, column=0, padx=10, pady=10)
        events_button = ttk.Button(contienetablas, text="Buscar Reserva", command=lambda nombre = "MiReserva":self.open_events_page(nombre3),width=20)
        events_button.grid(row=3, column=0, padx=10, pady=10)
        global contieneformulario
        contieneformulario = ttk.LabelFrame(
            self.master,
            text="Formulario de inserción:",
            borderwidth=1,
            width=100,
            relief="ridge"
        )
        contieneformulario.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        global contienedatos
        contienedatos = ttk.LabelFrame(
            self.master,
            text="Datos en mi sistema",
            borderwidth=1,
            width=600,
            relief="ridge"
        )
        contienedatos.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
    def open_events_page(self,nombre):
        #Borramos los widgets que hay en los layouts internos
        for widget in contienedatos.winfo_children():
            #print('***widgetdatos',widget)
            widget.destroy()

        for widget in contieneformulario.winfo_children():
            #print('***widgetformulario',widget)
            widget.destroy()

        if nombre == "PersonaServicio":
            #messagebox.showinfo("Events", f"Rellena tus datos  y habilidades, para actualizar o borrar habla con el Administrador")
            ##self.master.withdraw()  # Hide authentication window
            ##root = tk.Tk()
            event_manager_app = pe.EventManagerApp(contieneformulario)
            #root.mainloop()
        elif nombre == "Servicio":
            #self.master.withdraw()
            #messagebox.showinfo("Events", f"Rellena los servicios que ofreces, para actualizar o borrar habla con el Administrador")
            servicio_manager_app = serv.ServicioManagerApp(contieneformulario)
        elif nombre == "ReservaServicio":
            #messagebox.showinfo("Events", f"Opening Events Page y el boton se llama {nombre}")
            reserva_manager_app = reserva.ReservaManagerApp(contieneformulario,contienedatos)
        elif nombre == "MiReserva":
            #messagebox.showinfo("Events", f"Opening Events Page y el boton se llama {nombre}")
            mireserva_manager_app = mireserva.MiReservaManagerApp(contieneformulario,contienedatos)
        else:
            messagebox.showerror("Error", "Algo esta psando")
def main():
    global root
    root = tk.Tk()
    app = ControlManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
