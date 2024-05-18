import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import basededatos as bd
import adminmanager as adm
import usuariologinBootstrap as uslogin

# Ventana de Registro de Usuario
class UserRegistrationApp:
    def __init__(self, master):
        self.master = master
        self.style = Style(theme='cosmo')
        self.master.title("Registro de Usuario")
        self.db = bd.DatabaseManager('Habilidades.sqlite')
        self.create_widgets()

    def create_widgets(self):
        self.username_label = ttk.Label(self.master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.master, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = ttk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.master, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.email_label = ttk.Label(self.master, text="Email:")
        self.email_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = ttk.Entry(self.master, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        self.nombre_label = ttk.Label(self.master, text="Nombre:")
        self.nombre_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = ttk.Entry(self.master, width=30)
        self.nombre_entry.grid(row=3, column=1, padx=5, pady=5)

        self.apellido_label = ttk.Label(self.master, text="Apellidos:")
        self.apellido_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.apellido_entry = ttk.Entry(self.master, width=30)
        self.apellido_entry.grid(row=4, column=1, padx=5, pady=5)

        self.direccion_label = ttk.Label(self.master, text="Dirección:")
        self.direccion_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.direccion_entry = ttk.Entry(self.master, width=30)
        self.direccion_entry.grid(row=5, column=1, padx=5, pady=5)

        self.telefono_label = ttk.Label(self.master, text="Teléfono:")
        self.telefono_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.telefono_entry = ttk.Entry(self.master, width=30)
        self.telefono_entry.grid(row=6, column=1, padx=5, pady=5)

        self.nif_label = ttk.Label(self.master, text="NIF:")
        self.nif_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.nif_entry = ttk.Entry(self.master, width=30)
        self.nif_entry.grid(row=7, column=1, padx=5, pady=5)

        self.register_button = ttk.Button(self.master, text="Registrar", command=self.register_user)
        self.register_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        nif = self.nif_entry.get()
        print('estoy en register')
        if username and password and email and nombre and apellido and direccion and nif and telefono:
            valor = self.db.register_user(username, password, email, nombre, apellido, direccion, telefono, nif)
            print(f'estoy en register{valor}')
            if valor:
                messagebox.showinfo("Registro Exitoso", "Usuario registrado exitosamente")
                self.master.withdraw()  # Hide authentication window
                root = tk.Tk()
                Style(theme='cosmo')
                userlogin_manager_app = uslogin.UserAuthenticationApp(root)
                root.mainloop()
                self.clear_entries()
        else:
            messagebox.showerror("Error", "Por favor complete todos los campos")

    def clear_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.lastname_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.nif_entry.delete(0, tk.END)


