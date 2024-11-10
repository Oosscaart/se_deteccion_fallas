import tkinter as tk
from tkinter import Listbox, Scrollbar, Toplevel, filedialog, messagebox
from tkinter import simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import io
import os

def abrir_ventana_sintoma(root):
    # Cerrar la ventana actual
    root.destroy()

    # Crear una nueva ventana
    sintoma_root = tk.Tk()
    sintoma_root.title("Agregar Síntoma")

    # Poner la interfaz en pantalla completa
    sintoma_root.attributes("-fullscreen", True)

    # Crear un canvas para la imagen de fondo
    canvas = tk.Canvas(sintoma_root, highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)

    base_path = os.path.dirname(__file__)

    # Cargar y ajustar el tamaño de la imagen de fondo
    background_image_path = os.path.join(base_path, "fondos", "wp_features.jpg")
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((sintoma_root.winfo_screenwidth(), sintoma_root.winfo_screenheight()), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Colocar la imagen de fondo en el canvas
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    # Crear el texto del título en el canvas y centrarlo
    canvas.create_text(sintoma_root.winfo_screenwidth() / 2, 75, text="Agregar Síntoma", font=("Times New Roman", 42, "bold"), fill="white")

    # Variables para almacenar los datos
    nombre_var = tk.StringVar()
    imagen_path = ""

    # Función para regresar a la ventana de experto
    def regresar():
        sintoma_root.destroy()
        import experto
        experto.abrir_ventana()

    # Función para seleccionar una imagen
    def seleccionar_imagen(event=None):
        nonlocal imagen_path
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            imagen_path = file_path
            img = Image.open(file_path)
            img = img.resize((300, 300), Image.LANCZOS)
            img_photo = ImageTk.PhotoImage(img)
            canvas.create_image(sintoma_root.winfo_screenwidth() * 3 / 4, 400, image=img_photo, anchor="center", tags="imagen")
            canvas.image = img_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector

    # Función para mostrar el primer registro
    def funcion_inicio():
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, imagen FROM sintoma ORDER BY id ASC LIMIT 1")
            registro = cursor.fetchone()
            if registro:
                nombre_var.set(registro[0])
                imagen_blob = registro[1]
                imagen = Image.open(io.BytesIO(imagen_blob))
                imagen = imagen.resize((300, 300), Image.LANCZOS)
                imagen_photo = ImageTk.PhotoImage(imagen)
                canvas.create_image(sintoma_root.winfo_screenwidth() * 3 / 4, 400, image=imagen_photo, anchor="center", tags="imagen")
                canvas.image = imagen_photo
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    # Función para mostrar el registro anterior
    def funcion_atras():
        nombre_actual = nombre_var.get()
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, imagen FROM sintoma WHERE id < (SELECT id FROM sintoma WHERE nombre = %s) ORDER BY id DESC LIMIT 1", (nombre_actual,))
            registro = cursor.fetchone()
            if registro:
                nombre_var.set(registro[0])
                imagen_blob = registro[1]
                imagen = Image.open(io.BytesIO(imagen_blob))
                imagen = imagen.resize((300, 300), Image.LANCZOS)
                imagen_photo = ImageTk.PhotoImage(imagen)
                canvas.create_image(sintoma_root.winfo_screenwidth() * 3 / 4, 400, image=imagen_photo, anchor="center", tags="imagen")
                canvas.image = imagen_photo
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    # Función para mostrar el siguiente registro
    def funcion_siguiente():
        nombre_actual = nombre_var.get()
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, imagen FROM sintoma WHERE id > (SELECT id FROM sintoma WHERE nombre = %s) ORDER BY id ASC LIMIT 1", (nombre_actual,))
            registro = cursor.fetchone()
            if registro:
                nombre_var.set(registro[0])
                imagen_blob = registro[1]
                imagen = Image.open(io.BytesIO(imagen_blob))
                imagen = imagen.resize((300, 300), Image.LANCZOS)
                imagen_photo = ImageTk.PhotoImage(imagen)
                canvas.create_image(sintoma_root.winfo_screenwidth() * 3 / 4, 400, image=imagen_photo, anchor="center", tags="imagen")
                canvas.image = imagen_photo
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    # Función para mostrar el último registro
    def funcion_fin():
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, imagen FROM sintoma ORDER BY id DESC LIMIT 1")
            registro = cursor.fetchone()
            if registro:
                nombre_var.set(registro[0])
                imagen_blob = registro[1]
                imagen = Image.open(io.BytesIO(imagen_blob))
                imagen = imagen.resize((300, 300), Image.LANCZOS)
                imagen_photo = ImageTk.PhotoImage(imagen)
                canvas.create_image(sintoma_root.winfo_screenwidth() * 3 / 4, 400, image=imagen_photo, anchor="center", tags="imagen")
                canvas.image = imagen_photo
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    # Función para guardar los datos en la base de datos
    def guardar_datos():
        nombre = nombre_var.get()
        if not nombre or not imagen_path:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            
            # Verificar si el nombre ya existe
            cursor.execute("SELECT COUNT(*) FROM sintoma WHERE nombre = %s", (nombre,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "El nombre ya existe. Por favor, elija otro nombre.")
                return                
            
            with open(imagen_path, "rb") as file:
                imagen_blob = file.read()
            cursor.execute("INSERT INTO sintoma (nombre, imagen) VALUES (%s, %s)", (nombre, imagen_blob))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
            limpiar_campos()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

    # Función para limpiar los campos
    def limpiar_campos():
        nombre_var.set("")
        canvas.delete("imagen")

    def eliminar_datos():
        ventana_eliminar = tk.Toplevel(sintoma_root)
        ventana_eliminar.title("Eliminar Registro")
        ventana_eliminar.geometry("400x300")

        tk.Label(ventana_eliminar, text="Seleccione el registro a eliminar:").pack(pady=10)

        listbox = tk.Listbox(ventana_eliminar)
        listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        def cargar_registros():
            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="sistema_experto"
                )
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre FROM sintoma")
                registros = cursor.fetchall()
                for registro in registros:
                    listbox.insert(tk.END, registro[0])
                cursor.close()
                conexion.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

        cargar_registros()

        def eliminar_seleccionado():
            seleccion = listbox.get(listbox.curselection())
            if not seleccion:
                messagebox.showerror("Error", "Debe seleccionar un registro para eliminar.")
                return

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="sistema_experto"
                )
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM sintoma WHERE nombre = %s", (seleccion,))
                if cursor.rowcount == 0:
                    messagebox.showinfo("Información", "No se encontró ningún registro con ese nombre.")
                else:
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
                    listbox.delete(tk.ACTIVE)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar en la base de datos: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

        tk.Button(ventana_eliminar, text="Eliminar", command=eliminar_seleccionado).pack(pady=10)
                
    # Función para mostrar el menú de consultas
    def mostrar_menu_consultas():
        menu_consultas = Toplevel(sintoma_root)
        menu_consultas.title("Consultas")
        menu_consultas.geometry("300x200")

        def consulta_individual():
            menu_consultas.destroy()
            mostrar_consulta_individual()
        
        def consulta_general():
            menu_consultas.destroy()
            mostrar_consulta_general()

        tk.Button(menu_consultas, text="Consulta Individual", command=consulta_individual).pack(pady=10)
        tk.Button(menu_consultas, text="Consulta General", command=consulta_general).pack(pady=10)

    # Función para mostrar la consulta individual
    def mostrar_consulta_individual():
        consulta_individual_window = Toplevel(sintoma_root)
        consulta_individual_window.title("Consulta Individual")
        consulta_individual_window.geometry("400x300")

        tk.Label(consulta_individual_window, text="Seleccione el registro a consultar:").pack(pady=10)

        listbox = Listbox(consulta_individual_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM sintoma")
            registros = cursor.fetchall()
            for registro in registros:
                listbox.insert(tk.END, registro[0])
            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

        def mostrar_detalle():
            seleccion = listbox.get(listbox.curselection())
            mostrar_detalle_registro(seleccion)

        tk.Button(consulta_individual_window, text="Consultar", command=mostrar_detalle).pack(pady=10)

    # Función para mostrar el detalle de un registro
    def mostrar_detalle_registro(nombre):
        detalle_window = Toplevel(sintoma_root)
        detalle_window.title("Detalle del Registro")
        detalle_window.geometry("600x400")

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, imagen FROM sintoma WHERE nombre = %s", (nombre,))
            registro = cursor.fetchone()
            cursor.close()
            conexion.close()

            tk.Label(detalle_window, text=f"Nombre: {registro[0]}", font=("Arial", 16)).pack(pady=10)

            imagen_blob = registro[1]
            imagen = Image.open(io.BytesIO(imagen_blob))
            imagen = imagen.resize((300, 300), Image.LANCZOS)
            imagen_photo = ImageTk.PhotoImage(imagen)
            tk.Label(detalle_window, image=imagen_photo).pack(pady=10)
            detalle_window.image = imagen_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")  
              
    # Función para mostrar la consulta general
    def mostrar_consulta_general():
        consulta_general_window = Toplevel(sintoma_root)
        consulta_general_window.title("Consulta General")
        consulta_general_window.geometry("1000x800")

        # Crear un canvas y un frame para la barra de desplazamiento
        canvas = tk.Canvas(consulta_general_window)
        scrollbar = tk.Scrollbar(consulta_general_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Añadir títulos de columnas
        header_frame = tk.Frame(scrollable_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(header_frame, text="Nombre", font=("Arial", 18, "bold"), width=20, anchor="w").pack(side=tk.LEFT)
        tk.Label(header_frame, text="Imagen", font=("Arial", 18, "bold"), width=20, anchor="w").pack(side=tk.LEFT)

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, imagen FROM sintoma")
            registros = cursor.fetchall()
            cursor.close()
            conexion.close()

            for i, registro in enumerate(registros, start=1):
                frame = tk.Frame(scrollable_frame)
                frame.pack(fill=tk.X, padx=10, pady=5)

                tk.Label(frame, text=registro[0], font=("Arial", 18), width=20, anchor="w").pack(side=tk.LEFT)

                imagen_blob = registro[1]
                imagen = Image.open(io.BytesIO(imagen_blob))
                imagen = imagen.resize((100, 100), Image.LANCZOS)
                imagen_photo = ImageTk.PhotoImage(imagen)
                tk.Label(frame, image=imagen_photo).pack(side=tk.LEFT)
                frame.image = imagen_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector

                # Añadir una línea de separación entre registros
                separator = tk.Frame(scrollable_frame, height=2, bd=1, relief=tk.SUNKEN)
                separator.pack(fill=tk.X, padx=5, pady=5)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")      

    def modificar():
        ventana_modificar = tk.Toplevel(sintoma_root)
        ventana_modificar.title("Modificar Registro")
        ventana_modificar.attributes("-fullscreen", True)

        label = tk.Label(ventana_modificar, text="¿Qué registro desea modificar?", font=("Arial", 14))
        label.pack(pady=10)

        tree = ttk.Treeview(ventana_modificar, columns=("Nombre"), show='headings')
        tree.heading("Nombre", text="Nombre")
        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_registros():
            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="sistema_experto"
                )
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre FROM sintoma")
                registros = cursor.fetchall()
                for registro in registros:
                    tree.insert("", tk.END, values=registro)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al consultar en la base de datos: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

        cargar_registros()

        def modificar_registro():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Debe seleccionar un registro para modificar.")
                return

            nombre = tree.item(selected_item, 'values')[0]

            ventana_modificar_detalles = tk.Toplevel(ventana_modificar)
            ventana_modificar_detalles.title("Modificar Detalles")
            ventana_modificar_detalles.attributes("-fullscreen", True)

            label_nombre = tk.Label(ventana_modificar_detalles, text="Nombre", font=("Arial", 14))
            label_nombre.pack(pady=10)
            entry_nombre_modificar = tk.Entry(ventana_modificar_detalles, font=("Arial", 14))
            entry_nombre_modificar.pack(pady=10)

            label_imagen = tk.Label(ventana_modificar_detalles, text="Imagen", font=("Arial", 14))
            label_imagen.pack(pady=10)
            canvas_imagen_modificar = tk.Canvas(ventana_modificar_detalles, width=300, height=300)
            canvas_imagen_modificar.pack(pady=10)

            imagen_path_modificar = None

            def seleccionar_imagen_modificar():
                nonlocal imagen_path_modificar
                ventana_modificar_detalles.attributes("-disabled", True)
                imagen_path_modificar = filedialog.askopenfilename()
                ventana_modificar_detalles.attributes("-disabled", False)
                ventana_modificar_detalles.focus_force()
                if imagen_path_modificar:
                    imagen = Image.open(imagen_path_modificar)
                    imagen = imagen.resize((300, 300), Image.LANCZOS)
                    imagen_tk = ImageTk.PhotoImage(imagen)
                    canvas_imagen_modificar.create_image(0, 0, anchor="nw", image=imagen_tk)
                    canvas_imagen_modificar.imagen_tk = imagen_tk

            boton_seleccionar_imagen_modificar = tk.Button(ventana_modificar_detalles, text="Seleccionar Imagen", font=("Arial", 14), command=seleccionar_imagen_modificar)
            boton_seleccionar_imagen_modificar.pack(pady=10)

            def cargar_detalles():
                try:
                    conexion = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database="sistema_experto"
                    )
                    cursor = conexion.cursor()
                    cursor.execute("SELECT nombre, imagen FROM sintoma WHERE nombre = %s", (nombre,))
                    registro = cursor.fetchone()
                    if registro:
                        entry_nombre_modificar.insert(0, registro[0])
                        imagen_blob = registro[1]
                        if isinstance(imagen_blob, bytes):
                            imagen = Image.open(io.BytesIO(imagen_blob))
                            imagen = imagen.resize((300, 300), Image.LANCZOS)
                            imagen_tk = ImageTk.PhotoImage(imagen)
                            canvas_imagen_modificar.create_image(0, 0, anchor="nw", image=imagen_tk)
                            canvas_imagen_modificar.imagen_tk = imagen_tk
                        else:
                            messagebox.showerror("Error", "El campo de imagen no contiene datos binarios.")
                    else:
                        messagebox.showinfo("Información", "No se encontró el registro.")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error al consultar en la base de datos: {err}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

            cargar_detalles()

            def guardar_cambios():
                nuevo_nombre = entry_nombre_modificar.get()
                if not nuevo_nombre:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return

                try:
                    conexion = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database="sistema_experto"
                    )
                    cursor = conexion.cursor()
                    # Verifica si el nuevo nombre ya existe
                    cursor.execute("SELECT COUNT(*) FROM sintoma WHERE nombre = %s", (nuevo_nombre,))
                    if cursor.fetchone()[0] > 0 and nuevo_nombre != nombre:
                        messagebox.showerror("Error", "El nuevo nombre ya existe. Por favor, elija otro nombre.")
                        return
                    
                    if imagen_path_modificar:
                        with open(imagen_path_modificar, 'rb') as file:
                            binary_data = file.read()
                        cursor.execute("UPDATE sintoma SET nombre = %s, imagen = %s WHERE nombre = %s", (nuevo_nombre, binary_data, nombre))
                    else:
                        cursor.execute("UPDATE sintoma SET nombre = %s WHERE nombre = %s", (nuevo_nombre, nombre))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Registro modificado correctamente.")
                    ventana_modificar_detalles.destroy()
                    ventana_modificar.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error al modificar en la base de datos: {err}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

            boton_guardar_cambios = tk.Button(ventana_modificar_detalles, text="Guardar Cambios", font=("Arial", 14), command=guardar_cambios)
            boton_guardar_cambios.pack(pady=10)

        boton_modificar = tk.Button(ventana_modificar, text="Modificar", font=("Arial", 14), command=modificar_registro)
        boton_modificar.pack(pady=10)
    
        # Botón para cerrar la ventana
        boton_cerrar = tk.Button(ventana_modificar, text="Cerrar", font=("Arial", 14), command=ventana_modificar.destroy)
        boton_cerrar.pack(pady=10)
            
    # Crear el texto "Síntoma" en el canvas
    canvas.create_text(sintoma_root.winfo_screenwidth() / 4, 180, text="Síntoma:", font=("Times New Roman", 20, "bold"), fill="white", anchor="w")

    # Crear un cuadro de entrada para el nombre del síntoma
    entry_nombre = tk.Entry(sintoma_root, textvariable=nombre_var, font=("Times New Roman", 20), width=30)
    canvas.create_window(sintoma_root.winfo_screenwidth() / 4, 220, window=entry_nombre, anchor="w")

    # Crear el cuadro para mostrar la imagen con el texto "Seleccionar imagen"
    image_canvas = canvas.create_rectangle(sintoma_root.winfo_screenwidth() * 3 / 4 - 150, 250, sintoma_root.winfo_screenwidth() * 3 / 4 + 150, 550, fill="lightgray")
    canvas.create_text(sintoma_root.winfo_screenwidth() * 3 / 4, 400, text="Seleccionar imagen", font=("Times New Roman", 20, "bold"), fill="black")

    # Hacer que el cuadro de imagen sea clicable para seleccionar una imagen
    canvas.tag_bind(image_canvas, "<Button-1>", seleccionar_imagen)

    # Cargar las imágenes de los iconos
    icono_inicio_path = os.path.join(base_path, "iconos", "icono_inicio.png")
    icono_inicio = Image.open(icono_inicio_path)
    icono_inicio = icono_inicio.resize((25, 25), Image.LANCZOS)
    icono_inicio_photo = ImageTk.PhotoImage(icono_inicio)

    icono_atras_path = os.path.join(base_path, "iconos", "icono_atras.png")
    icono_atras = Image.open(icono_atras_path)
    icono_atras = icono_atras.resize((25, 25), Image.LANCZOS)
    icono_atras_photo = ImageTk.PhotoImage(icono_atras)

    icono_siguiente_path = os.path.join(base_path, "iconos", "icono_siguiente.png")
    icono_siguiente = Image.open(icono_siguiente_path)
    icono_siguiente = icono_siguiente.resize((25, 25), Image.LANCZOS)
    icono_siguiente_photo = ImageTk.PhotoImage(icono_siguiente)

    icono_fin_path = os.path.join(base_path, "iconos", "icono_fin.png")
    icono_fin = Image.open(icono_fin_path)
    icono_fin = icono_fin.resize((25, 25), Image.LANCZOS)
    icono_fin_photo = ImageTk.PhotoImage(icono_fin)

    # Crear los botones
    boton_inicio = tk.Button(sintoma_root, text="Inicio", font=("Arial", 16), image=icono_inicio_photo, compound="left", padx=20, pady=10, command=funcion_inicio)
    boton_inicio.place(relx=0.36, rely=0.80, anchor="center")

    boton_atras = tk.Button(sintoma_root, text="Atrás", font=("Arial", 16), image=icono_atras_photo, compound="left", padx=20, pady=10, command=funcion_atras)
    boton_atras.place(relx=0.48, rely=0.80, anchor="center")

    boton_siguiente = tk.Button(sintoma_root, text="Siguiente", font=("Arial", 16), image=icono_siguiente_photo, compound="left", padx=20, pady=10, command=funcion_siguiente)
    boton_siguiente.place(relx=0.60, rely=0.80, anchor="center")

    boton_fin = tk.Button(sintoma_root, text="Fin", font=("Arial", 16), image=icono_fin_photo, compound="left", padx=20, pady=10, command=funcion_fin)
    boton_fin.place(relx=0.72, rely=0.80, anchor="center")
    
    # Añadir los botones adicionales individualmente
    icono_altas_path = os.path.join(base_path, "iconos", "icono_altas.png")
    icono_altas = Image.open(icono_altas_path)
    icono_altas = icono_altas.resize((20, 20), Image.LANCZOS)
    icono_altas_photo = ImageTk.PhotoImage(icono_altas)
    boton_altas = tk.Button(sintoma_root, text="Altas", font=("Arial", 16), image=icono_altas_photo, compound="left", padx=20, pady=10, command=guardar_datos)
    boton_altas.place(relx=0.3, rely=0.9, anchor="center")

    icono_bajas_path = os.path.join(base_path, "iconos", "icono_bajas.png")
    icono_bajas = Image.open(icono_bajas_path)
    icono_bajas = icono_bajas.resize((25, 25), Image.LANCZOS)
    icono_bajas_photo = ImageTk.PhotoImage(icono_bajas)
    boton_bajas = tk.Button(sintoma_root, text="Bajas", font=("Arial", 16), image=icono_bajas_photo, compound="left", padx=20, pady=10, command=eliminar_datos)
    boton_bajas.place(relx=0.4, rely=0.9, anchor="center")

    icono_consultas_path = os.path.join(base_path, "iconos", "icono_consultas.png")
    icono_consultas = Image.open(icono_consultas_path)
    icono_consultas = icono_consultas.resize((25, 25), Image.LANCZOS)
    icono_consultas_photo = ImageTk.PhotoImage(icono_consultas)
    boton_consultas = tk.Button(sintoma_root, text="Consultas", font=("Arial", 16), image=icono_consultas_photo, compound="left", padx=20, pady=10, command=mostrar_menu_consultas)
    boton_consultas.place(relx=0.52, rely=0.9, anchor="center")

    icono_modificar_path = os.path.join(base_path, "iconos", "icono_modificar.png")
    icono_modificar = Image.open(icono_modificar_path)
    icono_modificar = icono_modificar.resize((25, 25), Image.LANCZOS)
    icono_modificar_photo = ImageTk.PhotoImage(icono_modificar)
    boton_modificar = tk.Button(sintoma_root, text="Modificar", font=("Arial", 16), image=icono_modificar_photo, compound="left", padx=20, pady=10, command=modificar)
    boton_modificar.place(relx=0.65, rely=0.9, anchor="center")
    
    icono_regresar_path = os.path.join(base_path, "iconos", "icono_regresar.png")
    icono_regresar = Image.open(icono_regresar_path)
    icono_regresar = icono_regresar.resize((25, 25), Image.LANCZOS)
    icono_regresar_photo = ImageTk.PhotoImage(icono_regresar)
    boton_salir = tk.Button(sintoma_root, text="Salir", font=("Arial", 16),image=icono_regresar_photo, compound="left", padx=20, pady=10, command=regresar)
    boton_salir.place(relx=0.76, rely=0.9, anchor="center")
    
    
    # Iniciar el bucle principal de la interfaz
    sintoma_root.mainloop()
    