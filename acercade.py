import tkinter as tk
from PIL import Image, ImageTk

# Ruta de las imágenes
ruta_imagen_fondo = "C:\\Users\\oscar\\OneDrive\\Escritorio\\deteccion_fallas\\fondos\\fondoExperto.jpg"
ruta_icono_regresar = "C:\\Users\\oscar\\OneDrive\\Escritorio\\deteccion_fallas\\iconos\\icono_regresar.png"
ruta_icono_autores = "C:\\Users\\oscar\\OneDrive\\Escritorio\\deteccion_fallas\\iconos\\icono_autores.png"
ruta_imagen = "C:\\Users\\oscar\\OneDrive\\Escritorio\\deteccion_fallas\\imagenes\\sistema_experto.jpg"

def abrir_ventana(root, ruta_imagen_fondo):
    # Crear la ventana "Acerca de"
    ventana = tk.Toplevel(root)
    ventana.title("Acerca del sistema")
    ventana.attributes("-fullscreen", True)

    # Cargar la imagen de fondo
    imagen_fondo = Image.open(ruta_imagen_fondo)
    imagen_fondo = imagen_fondo.resize((ventana.winfo_screenwidth(), ventana.winfo_screenheight()), Image.Resampling.LANCZOS)
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
    
    # Crear un Label para la imagen de fondo
    fondo = tk.Label(ventana, image=imagen_fondo)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Cargar y redimensionar la imagen
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((300, 300), Image.Resampling.LANCZOS)  # Redimensionar la imagen a 300x300
    imagen = ImageTk.PhotoImage(imagen)
    
    # Crear un Label para la imagen
    label_imagen = tk.Label(ventana, image=imagen, bg="white")
    label_imagen.place(relx=0.5, y=200, anchor="n")  # Ajusta el espacio vertical

    # Crear un Label para el título
    titulo = tk.Label(ventana, text="ACERCA DEL SISTEMA", font=("Arial", 52), fg="blue", bg="white")
    titulo.place(relx=0.5, y=50, anchor="n")
    
    # Crear un Label para el texto, alineado a la izquierda
    texto = tk.Label(ventana, text="Version 1.\nEste es un sistema experto para uso exclusivo de los alumnos del Tecnológico\n"
                                                " de Zacatepec de la materia de Inteligencia Artificial de la carrera de\n" 
                                                " Ingeniería en Sistemas Computacionales.",
                     font=("Arial", 28), fg="black", bg="white", justify="left", anchor="w")
    texto.place(relx=0.1, y=550, anchor="nw")  # Ajusta la posición y alineación del texto

    # Cargar y redimensionar los iconos
    icono_regresar = Image.open(ruta_icono_regresar)
    icono_regresar = icono_regresar.resize((24, 24), Image.Resampling.LANCZOS)
    icono_regresar = ImageTk.PhotoImage(icono_regresar)

    icono_autores = Image.open(ruta_icono_autores)
    icono_autores = icono_autores.resize((24, 24), Image.Resampling.LANCZOS)
    icono_autores = ImageTk.PhotoImage(icono_autores)

    # Función para regresar a la ventana principal
    def regresar():
        ventana.destroy()

    # Función para abrir la ventana de autores
    def abrir_autores():
        import autores
        autores.abrir_ventana(ventana, ruta_imagen_fondo)

    # Crear el botón "Regresar" en la parte inferior derecha
    boton_regresar = tk.Button(ventana, text="Regresar", command=regresar, font=("Arial", 14), width=150, height=50, image=icono_regresar, compound="left")
    boton_regresar.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-10)
    
    # Crear el botón "Autores" en la parte inferior derecha, justo encima del botón "Regresar"
    boton_autores = tk.Button(ventana, text="Autores", command=abrir_autores, font=("Arial", 14), width=150, height=50, image=icono_autores, compound="left")
    boton_autores.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-70)

    # Ejecutar la ventana
    ventana.mainloop()
