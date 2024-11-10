import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import importlib
import os

def abrir_ventana(root):
    # Cerrar la ventana principal
    root.destroy()

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Interfaces")

    # Poner la interfaz en pantalla completa
    root.attributes("-fullscreen", True)
    
    # Configurar la ruta base relativa al archivo actual
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
    label = tk.Label(root, text="Interfaces", font=("Times New Roman", 42, "bold"), bg="white", fg="blue", anchor="w")
    label.place(x=0, y=0, relwidth=1, height=150)  # Ajustar la posición y tamaño del título

    # Cargar iconos
    icono_experto_path = os.path.join(base_path, "iconos", "icono_experto.png")
    icono_experto = Image.open(icono_experto_path)
    icono_experto = icono_experto.resize((50, 50), Image.LANCZOS)
    icono_experto_photo = ImageTk.PhotoImage(icono_experto)

    icono_usuario_path = os.path.join(base_path, "iconos", "icono_usuario.png")
    icono_usuario = Image.open(icono_usuario_path)
    icono_usuario = icono_usuario.resize((50, 50), Image.LANCZOS)
    icono_usuario_photo = ImageTk.PhotoImage(icono_usuario)

    icono_regresar_path = os.path.join(base_path, "iconos", "icono_regresar.png")
    icono_regresar = Image.open(icono_regresar_path)
    icono_regresar = icono_regresar.resize((25, 25), Image.LANCZOS)
    icono_regresar_photo = ImageTk.PhotoImage(icono_regresar)

    # Función para verificar la contraseña y abrir la interfaz experto.py
    def verificar_contraseña():
        # Crear una nueva ventana para la contraseña
        ventana_contraseña = tk.Toplevel(root)
        ventana_contraseña.title("Contraseña ")
        ventana_contraseña.geometry("300x150")
        ventana_contraseña.configure(bg="white")

        # Etiqueta y campo de entrada para la contraseña
        etiqueta = tk.Label(ventana_contraseña, text="Ingrese la contraseña:", font=("Times New Roman", 14), bg="white")
        etiqueta.pack(pady=10)
        entrada_contraseña = tk.Entry(ventana_contraseña, show='*', font=("Times New Roman", 14))
        entrada_contraseña.pack(pady=5)

        # Función para verificar la contraseña
        def verificar():
            if entrada_contraseña.get() == '':
                ventana_contraseña.destroy()
                root.destroy()
                import experto
                experto.abrir_ventana()
            else:
                messagebox.showerror("Error", "Contraseña incorrecta, intente de nuevo")
                entrada_contraseña.delete(0, tk.END)

        # Botón para enviar la contraseña
        boton_enviar = tk.Button(ventana_contraseña, text="Entrar", font=("Times New Roman", 14), command=verificar)
        boton_enviar.pack(pady=10)

    def abrir_usuario():
        import usuario
        root.destroy()
        usuario.abrir_ventana()

    # Crear botones "Experto" y "Usuario" con iconos y tamaño más grande
    button_experto = tk.Button(root, text=" Experto", font=("Times New Roman", 30, "bold"), bg="white", fg="black", image=icono_experto_photo, compound="left", padx=20, pady=10, command=verificar_contraseña)
    button_experto.place(relx=0.5, rely=0.4, anchor="center")

    button_usuario = tk.Button(root, text=" Usuario", font=("Times New Roman", 30, "bold"), bg="white", fg="black", image=icono_usuario_photo, compound="left", padx=20, pady=10, command=abrir_usuario)
    button_usuario.place(relx=0.5, rely=0.7, anchor="center")

    # Función para regresar a la ventana principal
    def regresar():
        root.destroy()
        main = importlib.import_module('main')
        main.main()

    # Crear botón "Regresar"
    button_regresar = tk.Button(root, text=" Regresar", font=("Times New Roman", 20, "bold"), bg="white", fg="black", image=icono_regresar_photo, compound="left", padx=20, pady=10, command=regresar)
    button_regresar.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-30)

    # Iniciar el bucle principal de la interfaz
    root.mainloop()