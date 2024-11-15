import tkinter as tk
from tkinter import simpledialog, messagebox, StringVar, OptionMenu, Listbox, Button
from PIL import Image, ImageTk
import mysql.connector
import io
import os

def abrir_ventana_busqueda(root):
    # Crear la ventana principal
    root.destroy()
    
    # Creamos una nueva ventana para la búsqueda de características
    buscar_caracteristica_root = tk.Tk()
    buscar_caracteristica_root.title("Buscar Característica")
    
    # Establecemos pantalla completa
    buscar_caracteristica_root.attributes("-fullscreen", True)
    
    # Creamos una imagen de fondo
    canvas = tk.Canvas(buscar_caracteristica_root, highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)
    
    # Define la ruta base relativa al archivo actual
    base_path = os.path.dirname(__file__)

    # Ruta relativa para la imagen de fondo
    background_image_path = os.path.join(base_path, "fondos", "wp_table_relationship.jpg")
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((buscar_caracteristica_root.winfo_screenwidth(), buscar_caracteristica_root.winfo_screenheight()), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Colocamos la imagen de fondo en el canvas
    canvas.create_image(0, 0, image=background_photo, anchor="nw")  
    
    # Crear el texto del título en el canvas y centrarlo
    canvas.create_text(buscar_caracteristica_root.winfo_screenwidth() / 2, 75, text="Agregar Característica", font=("Times New Roman", 42, "bold"), fill="white")
    
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="sistema_experto"
    )
    
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, imagen, bandera FROM caracteristicas")
    caracteristicas = cursor.fetchall()
    conexion.close()
    
    # Crear el texto "Características"
    canvas.create_text(buscar_caracteristica_root.winfo_screenwidth() / 2 - 200, 150, text="Características:", font=("Times New Roman", 24, "bold"), fill="white")
    
    # Crear el OptionMenu para las características
    variable_caracteristica = StringVar(buscar_caracteristica_root)
    variable_caracteristica.set(caracteristicas[0][0])  # Valor por defecto
    option_menu = OptionMenu(buscar_caracteristica_root, variable_caracteristica, *[c[0] for c in caracteristicas])
    option_menu.config(font=("Times New Roman", 18))
    option_menu.place(x=buscar_caracteristica_root.winfo_screenwidth() / 2 - 100, y=130)
    
    # Función para mostrar la imagen de la característica seleccionada
    def mostrar_imagen_caracteristica(*args):
        caracteristica_seleccionada = variable_caracteristica.get()
        for caracteristica in caracteristicas:
            if caracteristica[0] == caracteristica_seleccionada:
                imagen_bytes = caracteristica[1]
                imagen = Image.open(io.BytesIO(imagen_bytes))
                imagen = imagen.resize((200, 200), Image.LANCZOS)
                imagen_photo = ImageTk.PhotoImage(imagen)
                canvas.create_image(buscar_caracteristica_root.winfo_screenwidth() / 2 + 200, 130, image=imagen_photo, anchor="nw")
                canvas.image = imagen_photo  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
                break
    
    variable_caracteristica.trace("w", mostrar_imagen_caracteristica)
    mostrar_imagen_caracteristica()
    
    # Crear Listbox para mostrar las características añadidas
    listbox_caracteristicas = Listbox(buscar_caracteristica_root, font=("Times New Roman", 18))
    listbox_caracteristicas.place(x=buscar_caracteristica_root.winfo_screenwidth() / 2 - 100, y=350, width=300, height=200)
    
    # Función para añadir característica al Listbox
    def añadir_caracteristica():
        caracteristica_seleccionada = variable_caracteristica.get()
        listbox_caracteristicas.insert(tk.END, caracteristica_seleccionada)
    
    # Función para eliminar característica del Listbox
    def eliminar_caracteristica():
        seleccion = listbox_caracteristicas.curselection()
        if seleccion:
            listbox_caracteristicas.delete(seleccion)
            
    def regresar():
        buscar_caracteristica_root.destroy()
        import usuario
        usuario.abrir_ventana()

    # Botón para añadir característica
    boton_añadir = Button(buscar_caracteristica_root, text="Añadir", font=("Times New Roman", 18), command=añadir_caracteristica)
    boton_añadir.place(x=buscar_caracteristica_root.winfo_screenwidth() / 2 + 210, y=350)
    
    # Botón para eliminar característica
    boton_eliminar = Button(buscar_caracteristica_root, text="Eliminar", font=("Times New Roman", 18), command=eliminar_caracteristica)
    boton_eliminar.place(x=buscar_caracteristica_root.winfo_screenwidth() / 2 + 210, y=400)
    
    # Función para realizar la inferencia
    def inferir():
        # Obtener las características seleccionadas
        seleccionadas = listbox_caracteristicas.get(0, tk.END)
        
        # Conectar a la base de datos para obtener los datos de fallas y características
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="sistema_experto"
        )
        
        cursor = conexion.cursor()
        
        # Obtener las fallas y sus características con los pesos
        cursor.execute("""
            SELECT f.id, f.nombre, f.suma, c.nombre, cf.peso
            FROM fallas_computadora f
            JOIN caracteristicas_fallas_computadora cf ON f.id = cf.id_fallas_computadora
            JOIN caracteristicas c ON c.id = cf.id_caracteristicas
        """)
        fallas_y_caracteristicas = cursor.fetchall()
        
        # Calcular la suma de los pesos de las características seleccionadas
        fallas_porcentaje = {}
        for id_falla, nombre_falla, suma_falla, nombre_caracteristica, peso in fallas_y_caracteristicas:
            if nombre_caracteristica in seleccionadas:
                if id_falla not in fallas_porcentaje:
                    fallas_porcentaje[id_falla] = {'nombre': nombre_falla, 'peso_total': 0, 'suma_falla': suma_falla}
                fallas_porcentaje[id_falla]['peso_total'] += peso
        
        # Calcular el porcentaje para cada falla y redondearlo
        resultados = []
        for id_falla, data in fallas_porcentaje.items():
            porcentaje = (data['peso_total'] / data['suma_falla']) * 100
            # Redondear el porcentaje hacia arriba si es mayor a .5, hacia abajo si es 0.5 o inferior
            porcentaje_redondeado = int(porcentaje) if porcentaje % 1 <= 0.5 else int(porcentaje) + 1
            resultados.append((data['nombre'], porcentaje_redondeado))
        
        # Mostrar los resultados en un cuadro de mensaje
        resultados.sort(key=lambda x: x[1], reverse=True)  # Ordenar por porcentaje descendente
        mensaje = "Posibles fallas:\n"
        for nombre_falla, porcentaje in resultados:
            mensaje += f"{nombre_falla}: {porcentaje}%\n"
        
        messagebox.showinfo("Resultados de la inferencia", mensaje)
        
        conexion.close()

    # Botón Inferir
    boton_inferir = Button(buscar_caracteristica_root, text="Inferir", font=("Times New Roman", 18), command=inferir)
    boton_inferir.place(x=buscar_caracteristica_root.winfo_screenwidth() / 2 - 100, y=570)
    
    # Botón regresar
    icono_regresar_path = os.path.join(base_path, "iconos", "icono_regresar.png")
    icono_regresar = Image.open(icono_regresar_path)
    icono_regresar = icono_regresar.resize((25, 25), Image.LANCZOS)
    icono_regresar_photo = ImageTk.PhotoImage(icono_regresar)

    boton_salir = tk.Button(buscar_caracteristica_root, text="Salir", font=("Arial", 16), image=icono_regresar_photo, compound="left", padx=20, pady=10, command=regresar)
    boton_salir.place(relx=0.76, rely=0.9, anchor="center")  
    
    buscar_caracteristica_root.mainloop()
