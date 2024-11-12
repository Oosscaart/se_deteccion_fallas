import importlib
import tkinter as tk
from PIL import Image, ImageTk
import os

def abrir_ventana():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Usuario")

    # Poner la interfaz en pantalla completa
    root.attributes("-fullscreen", True)
    
    # Función para regresar a la ventana principal
    def regresar():
        import entrar
        entrar.abrir_ventana(root)
    
    def abrir_busqueda_sintoma():
        import busqueda_sintoma
        busqueda_sintoma.abrir_ventana_busqueda(root)
        
    base_path = os.path.dirname(__file__)

    # Cargar y ajustar el tamaño de la imagen de fondo
    background_image_path = os.path.join(base_path, "fondos", "wp_user_object.jpg")
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Crear un widget de etiqueta para la imagen de fondo
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Crear una etiqueta con el título en mayúsculas y con la fuente Times New Roman en negritas
    label = tk.Label(root, text="Menú Usuario", font=("Times New Roman", 42, "bold"), bg="lightblue", fg="white", anchor="w")
    label.place(x=0, y=0, relwidth=1, height=150)  # Ajustar la posición y tamaño del título

    # Cargar iconos
    icono_sintoma_entrar_path = os.path.join(base_path, "iconos", "icono_sintoma_entrar.png")
    icono_sintoma_entrar = Image.open(icono_sintoma_entrar_path)
    icono_sintoma_entrar = icono_sintoma_entrar.resize((50, 50), Image.LANCZOS)
    icono_sintoma_entrar_photo = ImageTk.PhotoImage(icono_sintoma_entrar)     

    icono_enfermedad_entrar_path = os.path.join(base_path, "iconos", "icono_enfermedad_entrar.png")
    icono_enfermedad_entrar = Image.open(icono_enfermedad_entrar_path)
    icono_enfermedad_entrar = icono_enfermedad_entrar.resize((50, 50), Image.LANCZOS)
    icono_enfermedad_entrar_photo = ImageTk.PhotoImage(icono_enfermedad_entrar)

    icono_regresar_path = os.path.join(base_path, "iconos", "icono_regresar.png")
    icono_regresar = Image.open(icono_regresar_path)
    icono_regresar = icono_regresar.resize((25, 25), Image.LANCZOS)
    icono_regresar_photo = ImageTk.PhotoImage(icono_regresar)

      # Crear botones "Entrar en sintoma" y "Entrar en enfermedad" con iconos y tamaño más grande
    button_sintoma_entrar = tk.Button(root, text=" Busqueda por Caracteristica", font=("Times New Roman", 30, "bold"), bg="white", fg="black", image=icono_sintoma_entrar_photo, compound="left", padx=20, pady=10, command=abrir_busqueda_sintoma)
    button_sintoma_entrar.place(relx=0.5, rely=0.4, anchor="center")

    button_enfermedad_entrar = tk.Button(root, text=" Busqueda por falla de computadora", font=("Times New Roman", 30, "bold"), bg="white", fg="black", image=icono_enfermedad_entrar_photo, compound="left", padx=20, pady=10)
    button_enfermedad_entrar.place(relx=0.5, rely=0.7, anchor="center")

    # Crear botón "Regresar"
    button_regresar = tk.Button(root, text=" Regresar", font=("Times New Roman", 20, "bold"), bg="white", fg="black", image=icono_regresar_photo, compound="left", padx=20, pady=10, command=regresar)
    button_regresar.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-30)



    # Iniciar el bucle principal de la interfaz
    root.mainloop()