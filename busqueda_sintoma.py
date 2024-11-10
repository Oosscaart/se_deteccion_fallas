import tkinter as tk
from tkinter import simpledialog, messagebox, StringVar, OptionMenu, Listbox, Button
from PIL import Image, ImageTk
import importlib
import mysql.connector
import io

def abrir_ventana_busqueda(root):
    # Crear la ventana principal
    root.destroy()
    
    #Creamos una nueca ventana para la busqueda de sintomas
    buscar_sintoma_root = tk.Tk()
    buscar_sintoma_root.title("buscar sintoma")
    
    #Establecemos pantalla completa
    buscar_sintoma_root.attributes("-fullscreen", True)
    
    #Creamos una imagen de fondo
    canvas = tk.Canvas(buscar_sintoma_root, highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)
    
    #Cargamos y ajustamos el tamaño de la imagen de fondo
    background_image = Image.open(r"C:\Users\oscar\OneDrive\Escritorio\deteccion_fallas\Fondos\fondoSintoma.jpg")
    background_image = background_image.resize((buscar_sintoma_root.winfo_screenwidth(), buscar_sintoma_root.winfo_screenheight()), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    
    #Colocamos la imagen de fondo en el canvas
    canvas.create_image(0, 0, image=background_photo, anchor="nw")  
    
    #Crear el texto del titulo en el canvas y centrarlo
    canvas.create_text(buscar_sintoma_root.winfo_screenwidth() / 2, 75, text="Agregar Síntoma", font=("Times New Roman", 42, "bold"), fill="white")
    
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="sistema_experto"
    )
    
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, imagen FROM sintoma")
    sintomas = cursor.fetchall()
    conexion.close()
    
    # Crear el texto "Síntomas"
    canvas.create_text(buscar_sintoma_root.winfo_screenwidth() / 2 - 100, 150, text="Síntomas:", font=("Times New Roman", 24, "bold"), fill="white")
    
    # Crear el OptionMenu para los síntomas
    variable_sintoma = StringVar(buscar_sintoma_root)
    variable_sintoma.set(sintomas[0][0])  # Valor por defecto
    option_menu = OptionMenu(buscar_sintoma_root, variable_sintoma, *[s[0] for s in sintomas])
    option_menu.config(font=("Times New Roman", 18))
    option_menu.place(x=buscar_sintoma_root.winfo_screenwidth() / 2, y=130)
    
    # Función para mostrar la imagen del síntoma seleccionado
    def mostrar_imagen_sintoma(*args):
        sintoma_seleccionado = variable_sintoma.get()
        for sintoma in sintomas:
            if sintoma[0] == sintoma_seleccionado:
                imagen_bytes = sintoma[1]
                imagen = Image.open(io.BytesIO(imagen_bytes))
                imagen = imagen.resize((200, 200), Image.LANCZOS)
                imagen_photo = ImageTk.PhotoImage(imagen)
                canvas.create_image(buscar_sintoma_root.winfo_screenwidth() / 2 + 200, 130, image=imagen_photo, anchor="nw")
                canvas.image = imagen_photo  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
                break
    
    variable_sintoma.trace("w", mostrar_imagen_sintoma)
    mostrar_imagen_sintoma()
    
    # Crear Listbox para mostrar los síntomas añadidos
    listbox_sintomas = Listbox(buscar_sintoma_root, font=("Times New Roman", 18))
    listbox_sintomas.place(x=buscar_sintoma_root.winfo_screenwidth() / 2 - 100, y=300, width=300, height=200)
    
    # Función para añadir síntoma al Listbox
    def añadir_sintoma():
        sintoma_seleccionado = variable_sintoma.get()
        listbox_sintomas.insert(tk.END, sintoma_seleccionado)
    
    # Función para eliminar síntoma del Listbox
    def eliminar_sintoma():
        seleccion = listbox_sintomas.curselection()
        if seleccion:
            listbox_sintomas.delete(seleccion)
            
    def regresar():
        buscar_sintoma_root.destroy()
        import usuario
        usuario.abrir_ventana()
    
    # Botón para añadir síntoma
    boton_añadir = Button(buscar_sintoma_root, text="Añadir", font=("Times New Roman", 18), command=añadir_sintoma)
    boton_añadir.place(x=buscar_sintoma_root.winfo_screenwidth() / 2 - 100, y=520)
    
    # Botón para eliminar síntoma
    boton_eliminar = Button(buscar_sintoma_root, text="Eliminar", font=("Times New Roman", 18), command=eliminar_sintoma)
    boton_eliminar.place(x=buscar_sintoma_root.winfo_screenwidth() / 2 + 50, y=520)
    
    #boton regresar
    icono_regresar = Image.open(r"C:\Users\oscar\OneDrive\Escritorio\deteccion_fallas\iconos\icono_regresar.png")
    icono_regresar = icono_regresar.resize((25, 25), Image.LANCZOS)
    icono_regresar_photo = ImageTk.PhotoImage(icono_regresar)

    boton_salir = tk.Button(buscar_sintoma_root, text="Salir", font=("Arial", 16),image=icono_regresar_photo, compound="left", padx=20, pady=10, command=regresar)
    boton_salir.place(relx=0.76, rely=0.9, anchor="center")  
      
    buscar_sintoma_root.mainloop()