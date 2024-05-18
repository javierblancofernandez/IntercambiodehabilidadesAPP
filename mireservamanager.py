import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import sqlite3
import basededatos as bd
# Librerias para mandar email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configuracionemail as config

class MiReservaManagerApp:
    def __init__(self,contieneformulario,contienedatos):
        self.master = contieneformulario
        #self.master.title("Servicios Manager")
        self.db = bd.DatabaseManager('Habilidades.sqlite')
        self.contienedatos = contienedatos
        self.create_widgets()

    def create_widgets(self):
        # Crear los widgets de búsqueda
        self.mireserva_details_frame = ttk.Frame(self.contienedatos)
        self.mireserva_details_frame.grid(row=0, column=1, padx=5, pady=0)
        
        self.label_personares = ttk.Label(self.mireserva_details_frame, text="Persona Reserva:")
        self.label_personares.grid(row=0, column=0, padx=(5,2), pady=5,sticky="e")
        self.entry_personares = ttk.Entry(self.mireserva_details_frame, width=30)
        self.entry_personares.grid(row=0, column=1, padx=(2,10), pady=5,sticky="w")

        self.label_serviciores = ttk.Label(self.mireserva_details_frame, text="Servicio Reservado:")
        self.label_serviciores.grid(row=1, column=0, padx=(10,2), pady=5,sticky="e")
        self.entry_serviciores = ttk.Entry(self.mireserva_details_frame,width=30)
        self.entry_serviciores.grid(row=1, column=1, padx=(2,5), pady=5,sticky="w")

        self.button_buscar = ttk.Button(self.mireserva_details_frame, text="Buscar", command=self.buscar)
        self.button_buscar.grid(row=2, column=0, columnspan=2, pady=10)

        # Crear el Treeview para mostrar los resultados
        self.tree = ttk.Treeview(self.mireserva_details_frame, columns=("id", "Servicio_Reservado", "Persona_Reserva", "Fecha_Reserva", "Estado_Reserva","nif"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("Servicio_Reservado", text="Servicio_Reservado")
        self.tree.heading("Persona_Reserva", text="Persona_Reserva")
        self.tree.heading("Fecha_Reserva", text="Fecha_Reserva")
        self.tree.heading("Estado_Reserva", text="Estado_Reserva")
        self.tree.heading("nif", text="NIF")
        self.tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_registro)

        # Ajustar el ancho de las columnas
        self.tree.column("id", width=50)  # Ancho de la columna ID
        self.tree.column("Servicio_Reservado", width=150)  # Ancho de la columna Servicio_Reservado
        self.tree.column("Persona_Reserva", width=150)  # Ancho de la columna Persona_Reserva
        self.tree.column("Fecha_Reserva", width=100)  # Ancho de la columna Fecha_Reserva
        self.tree.column("Estado_Reserva", width=100)  # Ancho de la columna Estado_Reserva
        self.tree.column("nif", width=100)  # Ancho de la columna NIF


        # Crear formulario Mi Reserva
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

        self.reserva_nifres_label = ttk.Label(self.reserva_details_frame, text="NIF:")
        self.reserva_nifres_label.grid(row=4, column=0, sticky="w")
        self.reserva_nifres_entry = ttk.Entry(self.reserva_details_frame, width=30)
        self.reserva_nifres_entry.grid(row=4, column=1, padx=5, pady=5)

        self.reserva_fechares_label = ttk.Label(self.reserva_details_frame, text="Fecha Reserva:")
        self.reserva_fechares_label.grid(row=5, column=0, sticky="w")
        self.reserva_fechares_entry = ttk.Entry(self.reserva_details_frame, width=30)
        self.reserva_fechares_entry.grid(row=5, column=1, padx=5, pady=5)

        self.reserva_estadores_label = ttk.Label(self.reserva_details_frame, text="Estado Reserva:")
        self.reserva_estadores_label.grid(row=6, column=0, sticky="w")
        ##self.reserva_estadores_entry = ttk.Entry(self.reserva_details_frame, width=30)
        self.reserva_estadores_entry = ttk.Combobox(self.reserva_details_frame, width = 28, values=["pendiente", "confirmada", "anulada", "completada","otro_día"])
        self.reserva_estadores_entry.grid(row=6, column=1, padx=5, pady=10)

        self.add_button = ttk.Button(self.reserva_details_frame, text="Mandar Mail", command=self.mandarMail,width=20)
        self.add_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

    def buscar(self):
        personres = self.entry_personares.get()
        servres = self.entry_serviciores.get()

        busqueda = self.db.buscar_reserva(personres,servres)

        # Limpiar el Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insertar los resultados en el Treeview
        for row in busqueda:
            self.tree.insert('', tk.END, values=row)

    def seleccionar_registro(self, event):
        # Cambiar el estado de todos los Entry a "normal"
        self.reserva_servres_entry.config(state="normal")
        self.reserva_persres_entry.config(state="normal")
        self.reserva_nifres_entry.config(state="normal")
        self.reserva_fechares_entry.config(state="normal")
        
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        self.reserva_servres_entry.delete(0, tk.END)
        self.reserva_persres_entry.delete(0, tk.END)
        self.reserva_nifres_entry.delete(0, tk.END)
        self.reserva_fechares_entry.delete(0, tk.END)
        self.reserva_estadores_entry.set("")
        if values:
            self.reserva_servres_entry.insert(0, values[1])
            self.reserva_persres_entry.insert(0, values[2])
            self.reserva_nifres_entry.insert(0, values[5])
            self.reserva_fechares_entry.insert(0, values[3])
            self.reserva_estadores_entry.set(values[4])
        # Cambiar el estado de todos los Entry a "readonly"
        self.reserva_servres_entry.config(state="readonly")
        self.reserva_persres_entry.config(state="readonly")
        self.reserva_nifres_entry.config(state="readonly")
        self.reserva_fechares_entry.config(state="readonly")
            
    def mandarMail(self):
        #Consigo los campos de reserva
        servicio = self.reserva_servres_entry.get()
        fechareserva = self.reserva_fechares_entry.get()
        nifres = self.reserva_nifres_entry.get()
        nifres = str(nifres)
        usuario = self.db.buscar_email(nifres)

        print(f"esto es lo que tiene usuario : {usuario}")
        
        destinatario = usuario[0][3]
        nombre = usuario[0][4]
        apellido = usuario[0][5]
        #mensaje para email
        mensaje = f'Este mensaje esta dirigido unica y exclusivamente al {nombre} {apellido} \n'
        mensaje += f'su reserva para el servicio {servicio} para el día {fechareserva} esta confirmada'
        mensaje +='si desea cambiarla tendrá que ponerese en contacto con el Administrador administrador@administrador.com'
        mensaje +='Un saludo'

        #Asunto Reserva
        asunto = f"Confirmación reserva {nombre} {apellido} Plataforma Habilidades APP"

        
        # Configurar los detalles del servidor SMTP
        servidor_smtp = config.SMTP_SERVER  # Aquí debes ingresar el servidor SMTP que estés utilizando
        puerto_smtp = config.SMTP_PORT  # Puerto del servidor SMTP (usualmente 587 para TLS)

        # Credenciales del remitente
        remitente = config.SENDER_EMAIL
        password = config.SENDER_PASSWORD

        # Crear el objeto mensaje
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = asunto

        # Añadir el cuerpo del mensaje
        msg.attach(MIMEText(mensaje, 'plain'))

        # Iniciar conexión con el servidor SMTP
        with smtplib.SMTP(host=servidor_smtp, port=puerto_smtp) as servidor:
            # Iniciar conexión segura (TLS)
            servidor.starttls()

            # Autenticar con el servidor SMTP
            servidor.login(remitente, password)

            # Enviar el correo electrónico
            servidor.send_message(msg)

        print("Correo enviado satisfactoriamente")
        messagebox.showinfo("Success", "El email con tu reserva ha sido enviado")
        
def main():
    root = tk.Tk()
    app = MiReservaManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
