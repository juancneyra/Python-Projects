import sqlite3
from datetime import datetime


class Libreria:
    def __init__(self):
        self.conexion = Conexiones()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute("CREATE TABLE IF NOT EXISTS LIBROS (id_libro INTEGER PRIMARY KEY, titulo VARCHAR(30), autor VARCHAR(30), genero VARCHAR(30), isbn VARCHAR(13) NOT NULL, precio FLOAT NOT NULL,fecha_ultimo_precio VARCHAR(10), cantidadDisponibles INTEGER NOT NULL, UNIQUE(isbn))")
        self.conexion.miCursor.execute("CREATE TABLE IF NOT EXISTS HISTORICO_LIBROS (id_libro INTEGER PRIMARY KEY, titulo VARCHAR(30), autor VARCHAR(30), genero VARCHAR(30), isbn VARCHAR(13) NOT NULL, precio FLOAT NOT NULL,fecha_ultimo_precio VARCHAR(10), cantidadDisponibles INTEGER NOT NULL, UNIQUE(isbn))")
        self.conexion.miConexion.commit()

    def agregar_libro(self, titulo, autor, genero, precio, cantidadDisponibles, isbn):
        try:
            fecha = datetime.now().strftime("%Y-%m-%d")
            self.conexion.miCursor.execute("INSERT INTO LIBROS (titulo, autor, genero, precio, fecha_ultimo_precio, cantidadDisponibles, isbn) VALUES (?, ?, ?, ?, ?, ?, ?)", (titulo, autor, genero, precio, fecha, cantidadDisponibles, isbn))
            self.conexion.miConexion.commit()
            print("Libro agregado exitosamente")
        except:
            print("Error al agregar un libro")

    def modificar_libro(self, id, precio):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET precio = ? WHERE id_libro = ?", (precio, id))
            self.conexion.miConexion.commit()
            print("Libro modificado correctamente")
        except:
            print("Error al modificar un libro")

    def borrar_libro(self, id):
        try:
            self.conexion.miCursor.execute("DELETE FROM LIBROS WHERE id_libro = ?", (id))
            self.conexion.miConexion.commit()
            print("Libro borrado correctamente")
        except:
            print("Error al borrar un libro")

    def cargar_stock(self, id, cantidad):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET cantidadDisponibles = ? WHERE id_libro = ?", (cantidad, id))
            self.conexion.miConexion.commit()
            print("Stock actualizado correctamente")
        except:
            print("Error al actualizar stock")

    def listar_libros(self):
        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS")
            libros = self.conexion.miCursor.fetchall()
            print("ID | Nombre | AUTOR | GENERO | ISBN | PRECIO | FECHA ULTIMO PRECIO | STOCK |")
            for x in libros:
                print(x)
        except:
            print("No se pudo listar libros.")

    def cerrar_libreria(self):
        self.conexion.cerrarConexion()

    def registrar_venta(self, id_libro, cantidad):
        try:
            fecha = datetime.now().strftime("%Y-%m-%d")
            self.conexion.miCursor.execute("CREATE TABLE IF NOT EXISTS Ventas (id_venta INTEGER PRIMARY KEY, id_libro INTEGER, cantidad INTEGER, fecha DATE)")
            self.conexion.miConexion.commit()
            self.conexion.miCursor.execute("INSERT INTO Ventas (id_libro, cantidad, fecha) VALUES (?, ?, ?)", (id_libro, cantidad, fecha))
            self.conexion.miConexion.commit()
            self.conexion.miCursor.execute("UPDATE LIBROS SET cantidadDisponibles = cantidadDisponibles - ? WHERE id_libro = ?", (cantidad, id_libro))
            self.conexion.miConexion.commit()
            print("Venta registrada exitosamente")
            print(fecha)
        except:
            print("Error al registrar la venta")

    def actualizar_precios(self, porcentaje):
        try:
            fecha = datetime.now().strftime("%Y-%m-%d")
            self.conexion.miCursor.execute("INSERT INTO HISTORICO_LIBROS SELECT * FROM LIBROS")
            self.conexion.miConexion.commit()
            self.conexion.miCursor.execute("UPDATE LIBROS SET precio = precio * (1 + ? / 100), fecha_ultimo_precio = ?", (porcentaje, fecha))
            self.conexion.miConexion.commit()
            print("Precios actualizados correctamente")
            print(fecha)
        except:
            print("Error al actualizar los precios")

    def mostrar_registros_anteriores(self, fecha):
        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS WHERE fecha_ultimo_precio < ?", (fecha,))
            registros = self.conexion.miCursor.fetchall()
            print("Registros anteriores a la fecha especificada:")
            for registro in registros:
                print(registro)
        except:
            print("Error al mostrar los registros anteriores")

    def mostrar_autor(self,autor):
        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS WHERE autor = ?", (autor,))
            autores=self.conexion.miCursor.fetchall()
            print(f"Lista de libros según autor: {autor}")
            for autor in autores:
                print(autor)
        except:
            print("Error al mostrar la lista según autor.")


class Conexiones:
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("Libreria.db")
        self.miCursor = self.miConexion.cursor()

    def cerrarConexion(self):
        self.miConexion.close()


libreria = Libreria()

while True:
    print("Menu de opciones Libreria")
    print("1- Agregar libro")
    print("2- Modificar libro")
    print("3- Borrar un libro")
    print("4- Cargar disponibilidad")
    print("5- Listado de Libros")
    print("6- Ventas")
    print("7- Actualizar Precios")
    print("8- Listar libros por fecha")
    print("9- Listar libros según autor")
    print("0- Salir del menú")

    opcion = int(input("Por favor ingrese un número: "))

    if opcion == 1:
        titulo = input("Por favor ingrese el título del libro: ")
        autor = input("Por favor ingrese el autor del libro: ")
        genero = input("Por favor ingrese el genero del libro: ")
        isbn = str(input("Por favor ingrese el ISBN del libro: "))
        while len(isbn) != 13 or not(isbn.isnumeric()):
            print("El ISBN debe tener exactamente 13 digitos.")
            isbn = str(input("Ingrese el ISBN (13 digitos): "))
        precio = float(input("Por favor ingrese el precio del libro: "))
        cantidadDisponibles = int(input("Por favor ingrese la cantidad de unidades disponibles: "))
        libreria.agregar_libro(titulo, autor, genero, precio,cantidadDisponibles, isbn)
    elif opcion == 2:
        id = int(input("Por favor ingrese el id del libro a modificar: "))
        precio = float(input("Por favor ingrese el nuevo precio del libro: "))
        confirmacion = input("¿Está seguro que quiere modificar el libro? (Y o y)")
        if confirmacion == "Y" or confirmacion == "y":
            libreria.modificar_libro(id, precio)
        else:
            print("modificacion de libro cancelada")
    elif opcion == 3:
        id_libro_borrar = input("Ingrese id de libro a borrar: ")
        confirmacion = input("¿Está seguro que quiere borrar el libro? (Y o y)")
        if confirmacion == "Y" or confirmacion == "y":
            libreria.borrar_libro(id_libro_borrar)
        else:
            print("Eliminación de libro cancelada")
    elif opcion == 4:
        id_libro_borrar = input("Ingrese id de libro a modificar stock: ")
        cantidad_nueva = input("Ingrese el stock actual: ")
        libreria.cargar_stock(id_libro_borrar, cantidad_nueva)
    elif opcion == 5:
        libreria.listar_libros()
    elif opcion == 6:
        id_libro = int(input("Por favor ingrese el ID del libro vendido: "))
        cantidad = int(input("Por favor ingrese la cantidad vendida: "))
        libreria.registrar_venta(id_libro, cantidad)
    elif opcion == 7:
        porcentaje = float(input("Por favor ingrese el porcentaje de aumento de precios: "))
        libreria.actualizar_precios(porcentaje)
    elif opcion == 8:
        fecha = input("Por favor ingrese la fecha en formato YYYY-MM-DD: ")
        libreria.mostrar_registros_anteriores(fecha)
    elif opcion == 9:
        autor = input("Por favor ingrese el nombre del autor: ")
        libreria.mostrar_autor(autor)
    elif opcion == 0:
        libreria.cerrar_libreria()
        break
    else:
        print("Ingrese una opcion correcta")
