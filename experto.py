import tkinter as tk
from PIL import Image, ImageTk
import os

def abrir_ventana():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Experto")

    # Poner la interfaz en pantalla completa
    root.attributes("-fullscreen", True)
    
    base_path = os.path.dirname(__file__)

    # Cargar y ajustar el tamaño de la imagen de fondo
    background_image_path = os.path.join(base_path, "fondos", "wp_interfaces.jpg")
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Crear un widget de etiqueta para la imagen de fondo
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Crear una etiqueta con el título en mayúsculas y con la fuente Times New Roman en negritas
    label = tk.Label(root, text="Menú Experto", font=("Times New Roman", 42, "bold"), bg="lightblue", fg="white", anchor="w")
    label.place(x=0, y=0, relwidth=1, height=150)  # Ajustar la posición y tamaño del título

    # Función para regresar a la ventana de entrar
    def regresar():
        import entrar
        entrar.abrir_ventana(root)

    # Función para abrir objeto.py
    def abrir_objeto():
        import objeto
        objeto.abrir_ventana_objeto(root)

    def abrir_sintoma():    
        import sintoma
        sintoma.abrir_ventana_sintoma(root)
        
    def abrir_cuadro_relacion():
        import cuadro_relacion
        cuadro_relacion.abrir_ventana_cuadro_relacion(root)
        
    # Crear botón "Regresar"
    icono_regresar_path = os.path.join(base_path, "iconos", "icono_regresar.png")
    icono_regresar = Image.open(icono_regresar_path)
    icono_regresar = icono_regresar.resize((25, 25), Image.LANCZOS)
    icono_regresar_photo = ImageTk.PhotoImage(icono_regresar)
    button_regresar = tk.Button(root, text="Regresar", font=("Times New Roman", 20, "bold"), width=150, height=50, bg="lightgray", fg="black", image=icono_regresar_photo, compound="left", padx=20, pady=10, command=regresar)
    button_regresar.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    # Cargar iconos para los nuevos botones
    icono_agregar_objeto_path = os.path.join(base_path, "iconos", "icono_agregar_objeto.png")
    icono_agregar_objeto = Image.open(icono_agregar_objeto_path)
    icono_agregar_objeto = icono_agregar_objeto.resize((50, 50), Image.LANCZOS)
    icono_agregar_objeto_photo = ImageTk.PhotoImage(icono_agregar_objeto)

    icono_agregar_sintoma_path = os.path.join(base_path, "iconos", "icono_sintoma.png")
    icono_agregar_sintoma = Image.open(icono_agregar_sintoma_path)
    icono_agregar_sintoma = icono_agregar_sintoma.resize((50, 50), Image.LANCZOS)
    icono_agregar_sintoma_photo = ImageTk.PhotoImage(icono_agregar_sintoma)

    icono_cuadro_relacion_path = os.path.join(base_path, "iconos", "icono_agregar_objeto.png")
    icono_cuadro_relacion = Image.open(icono_cuadro_relacion_path)
    icono_cuadro_relacion = icono_cuadro_relacion.resize((50, 50), Image.LANCZOS)
    icono_cuadro_relacion_photo = ImageTk.PhotoImage(icono_cuadro_relacion)

    # Crear botones "Agregar Objeto", "Agregar Sintoma" y "Cuadro-Relacion"
    button_agregar_objeto = tk.Button(root, text="Agregar Objeto", font=("Times New Roman", 20, "bold"), bg="lightgray", fg="black", image=icono_agregar_objeto_photo, compound="left", command=abrir_objeto)
    button_agregar_objeto.place(relx=0.5, rely=0.3, anchor="center")

    button_agregar_sintoma = tk.Button(root, text="Agregar Sintoma", font=("Times New Roman", 20, "bold"), bg="lightgray", fg="black", image=icono_agregar_sintoma_photo, compound="left", command=abrir_sintoma)
    button_agregar_sintoma.place(relx=0.5, rely=0.5, anchor="center")

    button_cuadro_relacion = tk.Button(root, text="Cuadro-Relacion", font=("Times New Roman", 20, "bold"), bg="lightgray", fg="black", image=icono_cuadro_relacion_photo, compound="left", command= abrir_cuadro_relacion)
    button_cuadro_relacion.place(relx=0.5, rely=0.7, anchor="center")

    # Iniciar el bucle principal de la interfaz
    root.mainloop()