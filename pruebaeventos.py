import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import basededatos as bd

class EventManagerApp:
    def __init__(self, master):
        self.master = master
        #self.master.title("Persona Servicio Manager")
        self.db = bd.DatabaseManager('Habilidades.sqlite')
        self.event_manager = EventManager()

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
        self.event_details_frame = ttk.Frame(self.master)
        self.event_details_frame.grid(row=0, column=1, padx=5, pady=0)

        self.event_details_label = ttk.Label(self.event_details_frame, text="Persona Servicio:")
        self.event_details_label.grid(row=1, column=0, sticky="w")

        self.event_name_label = ttk.Label(self.event_details_frame, text="Nombre completo:")
        self.event_name_label.grid(row=2, column=0, sticky="w")
        self.event_name_entry = ttk.Entry(self.event_details_frame, width=30)
        self.event_name_entry.grid(row=2, column=1, padx=5, pady=5)

        self.event_email_label = ttk.Label(self.event_details_frame, text="Email:")
        self.event_email_label.grid(row=3, column=0, sticky="w")
        self.event_email_entry = ttk.Entry(self.event_details_frame, width=30)
        self.event_email_entry.grid(row=3, column=1, padx=5, pady=5)

        self.event_biografia_label = ttk.Label(self.event_details_frame, text="Biografia:")
        self.event_biografia_label.grid(row=4, column=0, sticky="w")
        self.event_biografia_entry = ttk.Entry(self.event_details_frame, width=30)
        self.event_biografia_entry.grid(row=4, column=1, padx=5, pady=5)

        self.event_habilidades_label = ttk.Label(self.event_details_frame, text="Habilidades:")
        self.event_habilidades_label.grid(row=5, column=0, sticky="w")
        self.event_habilidades_entry = ttk.Entry(self.event_details_frame, width=30)
        self.event_habilidades_entry.grid(row=5, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.event_details_frame, text="Add Persona", command=self.add_event)
        self.add_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def refresh_event_list(self):
        self.event_listbox.delete(0, tk.END)
        for event in self.event_manager.list_events():
            self.event_listbox.insert(tk.END, event.name)

    def add_event(self):
        name = self.event_name_entry.get()
        email = self.event_email_entry.get()
        biografia = self.event_biografia_entry.get()
        habilidades = self.event_habilidades_entry.get()
        self.db.create_personaservicio(name, email, biografia, habilidades)
        messagebox.showinfo("Success", "Registro satisfactorio")
        ##self.refresh_event_list()
        self.clear_entries()
    def clear_entries(self):
        self.event_name_entry.delete(0, tk.END)
        self.event_email_entry.delete(0, tk.END)
        self.event_biografia_entry.delete(0, tk.END)
        self.event_habilidades_entry.delete(0, tk.END)

class EventManager:
    def __init__(self):
        self.events = []

    def create_event(self, name, description):
        event = Event(name, description)
        self.events.append(event)

    def list_events(self):
        return self.events

class Event:
    def __init__(self, name, description):
        self.name = name
        self.description = description

def main():
    root = tk.Tk()
    app = EventManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
