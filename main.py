import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import os

# Define la ruta base relativa al archivo actual
base_path = os.path.dirname(__file__)

# Rutas de las imágenes usando rutas relativas
ruta_imagenes = {
    "fondo": os.path.join(base_path, "fondos", "wp_index.jpg"),
    "icono_acercade": os.path.join(base_path, "iconos", "icono_acercade.png"),  # Icono para abrir la ventana de "Acerca de"
    "icono_entrar": os.path.join(base_path, "iconos", "icono_entrar.png"),      # Icono para abrir la ventana de "Entrar"
    "icono_cuadro_relacion": os.path.join(base_path, "iconos", "icono_cuadro.png"),
    "icono_salir": os.path.join(base_path, "iconos", "icono_salir.png"),
    "logo": os.path.join(base_path, "imagenes", "logo.png"),
    "logo2": os.path.join(base_path, "imagenes", "itz.png")
}

def cargar_imagen(ruta, size):
    imagen = Image.open(ruta)
    imagen = imagen.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(imagen)

# Función para abrir la ventana "Acerca de"
def acerca_de():
    import acercade  # Importar el módulo para abrir la nueva ventana
    acercade.abrir_ventana(root, ruta_imagenes["fondo"])  # Llamar la función para abrir la nueva ventana
    
def abrir_busqueda_sintoma():
    import busqueda_sintoma
    busqueda_sintoma.abrir_ventana_busqueda(root)

# Crear la ventana principal
root = tk.Tk()
root.title("Tituto")

# Establecer la ventana en pantalla completa
root.attributes("-fullscreen", True)

# Cargar la imagen de fondo usando PIL
imagen_fondo = cargar_imagen(ruta_imagenes["fondo"], (root.winfo_screenwidth(), root.winfo_screenheight()))

# Crear un Canvas para la imagen de fondo y el texto
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill="both", expand=True)

# Mostrar la imagen de fondo en el Canvas
canvas.create_image(0, 0, image=imagen_fondo, anchor="nw")

# Cargar y colocar las imágenes en el Canvas
imagen_izquierda = cargar_imagen(ruta_imagenes["logo"], (304, 183))
canvas.create_image(0, 0, image=imagen_izquierda, anchor="nw")

imagen_derecha = cargar_imagen(ruta_imagenes["logo2"], (200, 200))
canvas.create_image(root.winfo_screenwidth() - 0, 0, image=imagen_derecha, anchor="ne")

# Mantener referencias a las imágenes para evitar que sean recolectadas por el recolector de basura
root.imagen_fondo = imagen_fondo
root.imagen_izquierda = imagen_izquierda
root.imagen_derecha = imagen_derecha

# Añadir texto al Canvas
canvas.create_text(root.winfo_screenwidth() // 2, 90, text="JESSICA LA MEJOR DEL MUNDO", font=("Times New Roman", 62, "bold"), fill="darkblue")
canvas.create_text(root.winfo_screenwidth() // 2, 260, text="I . T . Z", font=("Times New Roman", 48, "bold"), fill="black")
canvas.create_text(root.winfo_screenwidth() // 2, 430, text="S.E para detección de\n     fallas tecnicas",font=("Times New Roman", 56, "bold"), fill="darkred")
canvas.create_text(root.winfo_screenwidth() // 2, 600, text="Tapia Alejandro Oscar", font=("Times New Roman", 48, "bold"), fill="black")

# Cargar y redimensionar los iconos
icono_acercade = cargar_imagen(ruta_imagenes["icono_acercade"], (24, 24))
icono_entrar = cargar_imagen(ruta_imagenes["icono_entrar"], (24, 24))
icono_salir = cargar_imagen(ruta_imagenes["icono_salir"], (24, 24))
icono_cuadro_relacion = cargar_imagen(ruta_imagenes["icono_cuadro_relacion"], (24, 24))

# Mantener referencias a los iconos para evitar que sean recolectados por el recolector de basura
root.icono_acercade = icono_acercade
root.icono_entrar = icono_entrar
root.icono_salir = icono_salir

# Función para salir de la aplicación
def salir():
    root.quit()

# Función para el botón "Entrar"
def entrar():
    import entrar  # Importar el módulo para abrir la nueva ventana
    entrar.abrir_ventana(root)  # Llamar la función para abrir la nueva ventana

# Crear botones con iconos
boton_salir = tk.Button(root, text=" Salir", command=salir, font=("Arial", 14), width=150, height=50, image=icono_salir, compound="left", bg="white", fg="black")
boton_salir.place(relx=0, rely=0.98, anchor="sw", x=20, y=-20)

boton_acerca_de = tk.Button(root, text=" Acerca de", command=acerca_de, font=("Arial", 14), width=150, height=50, image=icono_acercade, compound="left", bg="white", fg="black")
boton_acerca_de.place(relx=1.0, rely=0.95, anchor="se", x=-20, y=-60)

boton_entrar = tk.Button(root, text=" Entrar", command=entrar, font=("Arial", 14), width=150, height=50, image=icono_entrar, compound="left", bg="white", fg="black")
boton_entrar.place(relx=1.0, rely=0.98, anchor="se", x=-20, y=-10)

boton_objeto = tk.Button(root, text="Cuadro_relacion", command=abrir_busqueda_sintoma, font=("Arial", 14), width=150, height=50, image=icono_cuadro_relacion, compound="left", bg="white", fg="black")
boton_objeto.place(relx=1.0, rely=0.8, anchor="se", x=-20, y=-10)


root.mainloop()