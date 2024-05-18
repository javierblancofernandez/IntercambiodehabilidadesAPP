import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        #self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE,password TEXT NOT NULL,email TEXT NOT NULL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS events ("+
                                "id INTEGER PRIMARY KEY AUTOINCREMENT,"+
                                "name TEXT NOT NULL,"+
                                "description TEXT NOT NULL"+
                              ")")
            
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def register_user(self, username, password, nombre, email, apellido, direccion,telefono, nif):
        cursor = self.conn.cursor()
        try:
            print('estoy en register')
##            cursor.execute("SELECT * FROM users WHERE username=?",(username,))
##            print(cursor.fetchall())
            cursor.execute("INSERT INTO usuarios (username, password, nombre, email, apellido, direccion,telefono, cif) VALUES (?, ?, ?, ?, ?, ? ,?,?)", (username, password, nombre, email, apellido, direccion, telefono,  nif))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")
            return False

    def login_user(self, username, password):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios ")
            user = cursor.fetchall()
            print(user)
            #return user is not None
            return user
        except sqlite3.IntegrityError:
            return False

        
    def create_personaservicio(self, name, email, biografia, habilidades):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO PersonaServicio (Nombre, Email, Biografia_Persona, Habilidades_Persona,Evaluación) VALUES (?, ?, ?, ?,?)", (name, email,biografia,habilidades,''))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")
            return False

    def create_servicio(self,name, descripcion, categoria, personaServicio,ubicacion,plazas):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO Servicios (NombreServicio, DescripcionServicio, CategoriaServicio, Persona_ofrece_servicio, UbicacionServicio, Plazas) VALUES (?, ?, ?, ?, ?, ?)", (name, descripcion, categoria, personaServicio,ubicacion,plazas))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")

    def update_servplaza(self,id,plazas):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE Servicios SET Plazas = ? WHERE id = ?", (plazas,id))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")

    def create_reserva(self,serviciores, personares,nif ,fechares, estadores):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO ReservaServicio (ServicioReservado, PersonaReserva, FechayHoraReserva, Estado_Reserva, nif) VALUES (?, ?, ?, ?, ?)", (serviciores, personares, fechares, estadores, nif))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")
        
    def listar_servicio(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Servicios")
            return cursor.fetchall()
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")   
        
    def list_events(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM events")
            return cursor.fetchall()
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")

    def buscar_reserva(self,personres,servres):
        cursor = self.conn.cursor()
        try:
            query = 'SELECT * FROM ReservaServicio WHERE PersonaReserva LIKE ? OR ServicioReservado LIKE ?'
            cursor.execute(query, ('%' + personres + '%', '%' + servres + '%'))
            return cursor.fetchall()
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")
    
    def buscar_email(self,nif):
        cursor = self.conn.cursor()
        try:
            print(f"este es el nif:{nif}")
            #query = 'SELECT * FROM usuarios WHERE cif = ?'
            cursor.execute(f"SELECT * FROM usuarios WHERE cif = {nif}")
            return cursor.fetchall()
        except sqlite3.IntegrityError as e:
            print(f"Error en la base de datos: {e}")        
    def close(self):
        self.conn.close()
