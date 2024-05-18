import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import basededatos as bd
import pruebaeventos as pe
import controlmanager as cm
import adminmanager as adm
import pruebaregistro as pr
import sqlite3

# Usuario-Registro APP
class UserAuthenticationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("User Authentication")
        Style(theme='cosmo')
        self.db = bd.DatabaseManager('Habilidades.sqlite')
        self.create_widgets()

    def create_widgets(self):
        self.style = Style(theme='cosmo')  # Change theme as needed
        self.username_label = ttk.Label(self.master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.master, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = ttk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.master, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

##        self.email_label = ttk.Label(self.master, text="Email:")
##        self.email_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
##        self.email_entry = ttk.Entry(self.master, width=30)
##        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        self.register_button = ttk.Button(self.master, text="Register", command=self.register_user)
        self.register_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.login_button = ttk.Button(self.master, text="Login", command=self.login_user)
        self.login_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def register_user(self):
        self.master.withdraw()  # Hide authentication window
        root = tk.Tk()
        userregistration_manager_app = pr.UserRegistrationApp(root)
        root.mainloop()
        
##        username = self.username_entry.get()
##        password = self.password_entry.get()
##        email = self.email_entry.get()
##        if username and password and email:
##            if self.db.register_user(username, password, email):
##                messagebox.showinfo("Success", "Registro satisfactorio")
##                self.clear_entries()
##        else:
##            messagebox.showerror("Error", "Por favor rellena todos los campos")

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # si el usuario es administrador entra a la parte de Administrador
        if username=='administrador' and password == 'administrador':
            user = self.db.login_user(username, password)
            print("***user:",user)
            if user:
                messagebox.showinfo("Success", "Login Administrador satistactorio")
                self.clear_entries()
                self.open_admin_manager()
        elif username and password:
            user = self.db.login_user(username, password)
            print("***user:",user)
            if user:
                messagebox.showinfo("Success", "Login satisfactorio")
                self.clear_entries()
                self.open_menucontrol_manager()
            else:
                messagebox.showerror("Error", "Invalido username o password")    
        else:
            messagebox.showerror("Error", "Por favor, introduzca su username y password")

    # Borrar los campos Entry
    def clear_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        #self.email_entry.delete(0, tk.END)
        
    # Acceder a AdminManagerApp
    def open_admin_manager(self):
        self.master.withdraw()  # Hide authentication window
        root = tk.Tk()
        root.geometry("1000x500")
        root.columnconfigure(0, minsize=100)
        root.columnconfigure(1, minsize=100)
        root.columnconfigure(2, minsize=600)
        root.rowconfigure(0, weight=1)
        admin_manager_app = adm.AdminManagerApp(root)
        root.mainloop()
        
    # Acceder a ControlManager
    def open_menucontrol_manager(self):
        self.master.withdraw()  # Hide authentication window
        root = tk.Tk()
        control_manager_app = cm.ControlManagerApp(root)
        root.mainloop()
          
def main():
    root = tk.Tk()
    user_auth_app = UserAuthenticationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

