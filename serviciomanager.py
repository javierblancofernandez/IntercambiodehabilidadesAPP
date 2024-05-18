import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import basededatos as bd

class ServicioManagerApp:
    def __init__(self, contieneformulario):
        self.master = contieneformulario
        #self.master.title("Servicios Manager")
        self.db = bd.DatabaseManager('Habilidades.sqlite')

        self.create_widgets()

    def create_widgets(self):
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

        # Event Details Frame
        self.servicio_details_frame = ttk.Frame(self.master)
        self.servicio_details_frame.grid(row=0, column=1, padx=5, pady=0)

        self.servicio_details_label = ttk.Label(self.servicio_details_frame, text="Servicio Ofrecido:")
        self.servicio_details_label.grid(row=1, column=0, sticky="w")

        self.servicio_nombre_label = ttk.Label(self.servicio_details_frame, text="Nombre Servicio:")
        self.servicio_nombre_label.grid(row=2, column=0, sticky="w")
        self.servicio_nombre_entry = ttk.Entry(self.servicio_details_frame, width=30)
        self.servicio_nombre_entry.grid(row=2, column=1, padx=5, pady=5)

        self.servicio_descrip_label = ttk.Label(self.servicio_details_frame, text="Descripción:")
        self.servicio_descrip_label.grid(row=3, column=0, sticky="w")
        self.servicio_descrip_entry = ttk.Entry(self.servicio_details_frame, width=30)
        self.servicio_descrip_entry.grid(row=3, column=1, padx=5, pady=5)

        self.servicio_categoria_label = ttk.Label(self.servicio_details_frame, text="Categoría:")
        self.servicio_categoria_label.grid(row=4, column=0, sticky="w")
        self.servicio_categoria_entry = ttk.Entry(self.servicio_details_frame, width=30)
        self.servicio_categoria_entry.grid(row=4, column=1, padx=5, pady=5)

        self.servicio_personaServ_label = ttk.Label(self.servicio_details_frame, text="Persona ofrece servicio:")
        self.servicio_personaServ_label.grid(row=5, column=0, sticky="w")
        self.servicio_personaServ_entry = ttk.Entry(self.servicio_details_frame, width=30)
        self.servicio_personaServ_entry.grid(row=5, column=1, padx=5, pady=5)

        self.servicio_ubicacion_label = ttk.Label(self.servicio_details_frame, text="Ubicación:")
        self.servicio_ubicacion_label.grid(row=6, column=0, sticky="w")
        self.servicio_ubicacion_entry = ttk.Entry(self.servicio_details_frame, width=30)
        self.servicio_ubicacion_entry.grid(row=6, column=1, padx=5, pady=5)

        self.servicio_plazas_label = ttk.Label(self.servicio_details_frame, text="Plazas:")
        self.servicio_plazas_label.grid(row=7, column=0, sticky="w")
        self.servicio_plazas_entry = ttk.Entry(self.servicio_details_frame, width=30)
        self.servicio_plazas_entry.grid(row=7, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.servicio_details_frame, text="Add Servicio", command=self.add_servicio)
        self.add_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

    def add_servicio(self):

        name = self.servicio_nombre_entry.get()
        descripcion = self.servicio_descrip_entry.get()
        categoria = self.servicio_categoria_entry.get()
        personaServicio = self.servicio_personaServ_entry.get()
        ubicacion = self.servicio_ubicacion_entry.get()
        plazas = self.servicio_plazas_entry.get()
            
        self.db.create_servicio(name, descripcion, categoria, personaServicio,ubicacion,plazas)
        messagebox.showinfo("Success", "Registro satisfactorio")
        ##self.refresh_event_list()
        self.clear_entries()
        
    def clear_entries(self):
        self.servicio_nombre_entry.delete(0, tk.END)
        self.servicio_descrip_entry.delete(0, tk.END)
        self.servicio_categoria_entry.delete(0, tk.END)
        self.servicio_personaServ_entry.delete(0, tk.END)
        self.servicio_ubicacion_entry.delete(0, tk.END)
        self.servicio_plazas_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = ServicioManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
