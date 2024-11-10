import tkinter as tk
from PIL import Image, ImageTk
import os

# Define la ruta base relativa al archivo actual
base_path = os.path.dirname(__file__)

# Rutas relativas de las imágenes
ruta_imagen_fondo = os.path.join(base_path, "fondos", "wp_index.jpg")
ruta_imagen_autor1 = os.path.join(base_path, "imagenes", "oscar.jpeg")
ruta_imagen_autor2 = os.path.join(base_path, "imagenes", "jessica.jpg")
ruta_icono_regresar = os.path.join(base_path, "iconos", "icono_regresar.png")

def abrir_ventana(root, ruta_imagen_fondo):
    # Crear la ventana "Autores"
    ventana = tk.Toplevel(root)
    ventana.title("AUTORES DEL PROGRAMA")
    ventana.attributes("-fullscreen", True)
    
    # Cargar la imagen de fondo
    imagen_fondo = Image.open(ruta_imagen_fondo)
    imagen_fondo = imagen_fondo.resize((ventana.winfo_screenwidth(), ventana.winfo_screenheight()), Image.Resampling.LANCZOS)
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
    
    # Crear un Label para la imagen de fondo
    fondo = tk.Label(ventana, image=imagen_fondo)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Cargar y redimensionar la imagen del primer autor
    imagen_autor1 = Image.open(ruta_imagen_autor1)
    imagen_autor1 = imagen_autor1.resize((200, 200), Image.Resampling.LANCZOS)
    imagen_autor1 = ImageTk.PhotoImage(imagen_autor1)
    
    # Crear un Label para la imagen del primer autor
    label_autor1 = tk.Label(ventana, image=imagen_autor1, bg="white")
    label_autor1.place(x=50, y=150, anchor="nw")
    
    # Crear un Label para la información del primer autor
    texto_autor1 = tk.Label(ventana, text="Tapia Alejandro Oscar\nCalle Bugambilias 23\n7773441316\nOscar_tapia_0202@hotmail.com",
                            font=("Arial", 14), fg="black", bg="white", justify="left")
    texto_autor1.place(x=270, y=150, anchor="nw")
    
    # Cargar y redimensionar la imagen del segundo autor
    imagen_autor2 = Image.open(ruta_imagen_autor2)
    imagen_autor2 = imagen_autor2.resize((200, 200), Image.Resampling.LANCZOS)
    imagen_autor2 = ImageTk.PhotoImage(imagen_autor2)
    
    # Crear un Label para la imagen del segundo autor
    label_autor2 = tk.Label(ventana, image=imagen_autor2, bg="white")
    label_autor2.place(x=50, y=400, anchor="nw")
    
    # Crear un Label para la información del segundo autor
    texto_autor2 = tk.Label(ventana, text="Zagal Mercado Jessica Arleth\nTejalpa, Jiutepec Morelos\n7772114512\nJess_07@outlook.com",
                            font=("Arial", 14), fg="black", bg="white", justify="left")
    texto_autor2.place(x=270, y=400, anchor="nw")
    
    # Cargar y redimensionar el icono de regresar
    icono_regresar = Image.open(ruta_icono_regresar)
    icono_regresar = icono_regresar.resize((24, 24), Image.Resampling.LANCZOS)
    icono_regresar = ImageTk.PhotoImage(icono_regresar)

    # Función para regresar a la ventana "Acerca de"
    def regresar():
        ventana.destroy()

    # Crear el botón "Regresar" en la parte inferior derecha
    boton_regresar = tk.Button(ventana, text="Regresar", command=regresar, font=("Arial", 14), width=150, height=50, image=icono_regresar, compound="left")
    boton_regresar.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-10)

    # Ejecutar la ventana
    ventana.mainloop()
