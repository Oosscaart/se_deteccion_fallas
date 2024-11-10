import tkinter as tk
from tkinter import OptionMenu, StringVar, Label, Entry, Listbox, Scrollbar, END, messagebox
from PIL import Image, ImageTk
import mysql.connector
import io
import os

def abrir_ventana_cuadro_relacion(root):
    # Cierra la ventana actual
    root.destroy()

    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="sistema_experto"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, imagen FROM objeto")
    enfermedades = cursor.fetchall()
    cursor.execute("SELECT id, nombre FROM sintoma")
    sintomas = cursor.fetchall()
    conexion.close()

    # Crea la nueva ventana
    cuadro_relacion_root = tk.Tk()
    cuadro_relacion_root.title("Cuadro Relacion")
    
    # Pantalla completa
    cuadro_relacion_root.attributes("-fullscreen", True)
    
    # Crea el canvas para la imagen de fondo
    canvas = tk.Canvas(cuadro_relacion_root, highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)
    
    base_path = os.path.dirname(__file__)
    
    # Cargar y ajustar el tamaño de la imagen de fondo
    background_image_path = os.path.join(base_path, "fondos", "wp_table_relationship.jpg")
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((cuadro_relacion_root.winfo_screenwidth(), cuadro_relacion_root.winfo_screenheight()), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Colocar la imagen de fondo en el canvas
    canvas.create_image(0, 0, image=background_photo, anchor="nw")
    
    # Crear el texto del título en el canvas y centrarlo
    canvas.create_text(cuadro_relacion_root.winfo_screenwidth() / 2, 75, text="Cuadro Relacion", font=("Times New Roman", 42, "bold"), fill="white")
    
    def regresar():
        cuadro_relacion_root.destroy()
        import experto
        experto.abrir_ventana()
        
    # Crear el botón de regresar
    boton_regresar = tk.Button(cuadro_relacion_root, text="Regresar", command=regresar)
    boton_regresar.place(x=cuadro_relacion_root.winfo_screenwidth() - 150, y=cuadro_relacion_root.winfo_screenheight() - 50)
    
    # Crear el texto "Enfermedad" y centrarlo
    canvas.create_text(250, 150, text="Enfermedad:", font=("Times New Roman", 24, "bold"), fill="white")
    
    # Crear el OptionMenu para mostrar las enfermedades
    enfermedad_var = StringVar(cuadro_relacion_root)
    enfermedad_var.set("Selecciona una enfermedad")
    option_menu = OptionMenu(cuadro_relacion_root, enfermedad_var, *[enfermedad[1] for enfermedad in enfermedades])
    option_menu.place(x=350, y=140)
    
    # Crear el Label para mostrar la imagen de la enfermedad y centrarla
    imagen_label = Label(cuadro_relacion_root)
    imagen_label.place(x=cuadro_relacion_root.winfo_screenwidth()//2 - 150, y=140, width=300, height=300)
    
    def mostrar_imagen(*args):
        enfermedad_seleccionada = enfermedad_var.get()
        for enfermedad in enfermedades:
            if enfermedad[1] == enfermedad_seleccionada:
                imagen_datos = enfermedad[2]
                imagen = Image.open(io.BytesIO(imagen_datos))
                imagen = imagen.resize((300, 300), Image.LANCZOS)
                imagen_photo = ImageTk.PhotoImage(imagen)
                imagen_label.config(image=imagen_photo)
                imagen_label.image = imagen_photo
                break
        cargar_registros()

    enfermedad_var.trace("w", mostrar_imagen)
    
    # Crear el texto "Sintoma" y centrarlo
    canvas.create_text(250, 200, text="Sintoma:", font=("Times New Roman", 24, "bold"), fill="white")
    
    # Crear el OptionMenu para mostrar los síntomas
    sintoma_var = StringVar(cuadro_relacion_root)
    sintoma_var.set("Selecciona un sintoma")
    option_menu_sintoma = OptionMenu(cuadro_relacion_root, sintoma_var, *[sintoma[1] for sintoma in sintomas])
    option_menu_sintoma.place(x=350, y=190)
    
    # Crear el texto "Peso %" y centrarlo
    canvas.create_text(250, 250, text="Peso %:", font=("Times New Roman", 24, "bold"), fill="white")
    
    # Crear el Entry para ingresar el peso y centrarlo
    peso_entry = Entry(cuadro_relacion_root)
    peso_entry.place(x=350, y=240)
    
    # Crear el título "Síntomas por añadir"
    canvas.create_text(290, 480, text="Síntomas por añadir:", font=("Times New Roman", 24, "bold"), fill="white")

    # Crear el Listbox para mostrar los registros añadidos (nuevos) y centrarlo
    listbox_frame_nuevos = tk.Frame(cuadro_relacion_root)
    listbox_frame_nuevos.place(x=150, y=500, width=500, height=200)
    scrollbar_nuevos = Scrollbar(listbox_frame_nuevos)
    scrollbar_nuevos.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_nuevos = Listbox(listbox_frame_nuevos, yscrollcommand=scrollbar_nuevos.set)
    listbox_nuevos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_nuevos.config(command=listbox_nuevos.yview)
    
    # Crear el título "Registros hechos"
    canvas.create_text(870, 480, text="Registros hechos:", font=("Times New Roman", 24, "bold"), fill="white")

    # Crear el Listbox para mostrar los registros existentes y centrarlo
    listbox_frame_existentes = tk.Frame(cuadro_relacion_root)
    listbox_frame_existentes.place(x=750, y=500, width=500, height=200)
    scrollbar_existentes = Scrollbar(listbox_frame_existentes)
    scrollbar_existentes.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_existentes = Listbox(listbox_frame_existentes, yscrollcommand=scrollbar_existentes.set)
    listbox_existentes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_existentes.config(command=listbox_existentes.yview)
    
    def cargar_registros():
        listbox_existentes.delete(0, END)
        enfermedad_seleccionada = enfermedad_var.get()
        if enfermedad_seleccionada:
            try:
                enfermedad_id = next(enfermedad[0] for enfermedad in enfermedades if enfermedad[1] == enfermedad_seleccionada)
            except StopIteration:
                return
        
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT s.nombre, es.peso FROM enfermedad_sintoma es JOIN sintoma s ON es.id_sintoma = s.id WHERE es.id_enfermedad = %s", (enfermedad_id,))
            registros = cursor.fetchall()
            for registro in registros:
                listbox_existentes.insert(END, f"{enfermedad_seleccionada} - {registro[0]} - {registro[1]}%")
            conexion.close()
    
    def anadir_registro():
        enfermedad_seleccionada = enfermedad_var.get()
        sintoma_seleccionado = sintoma_var.get()
        peso = peso_entry.get()
        if enfermedad_seleccionada and sintoma_seleccionado and peso:
            listbox_nuevos.insert(END, f"{enfermedad_seleccionada} - {sintoma_seleccionado} - {peso}%")
            sintoma_var.set("Selecciona un sintoma")
            peso_entry.delete(0, END)
            option_menu.config(state="disabled")
    
    def borrar_registro():
        seleccion_nuevos = listbox_nuevos.curselection()
        if seleccion_nuevos:
            listbox_nuevos.delete(seleccion_nuevos)
        seleccion_existentes = listbox_existentes.curselection()
        if seleccion_existentes:
            listbox_existentes.delete(seleccion_existentes)

    # Botón para borrar registros ya guardados en la base de datos
    def borrar_registro_guardado():
        seleccion_existentes = listbox_existentes.curselection()
        
        if seleccion_existentes:
            try:
                # Obtener el registro seleccionado
                registro_seleccionado = listbox_existentes.get(seleccion_existentes)
                enfermedad_seleccionada, sintoma_seleccionado, peso = registro_seleccionado.split(" - ")
                peso = float(peso.replace("%", ""))  # Convertir el peso a número flotante (float)

                # Obtener el ID de la enfermedad y del síntoma
                enfermedad_id = next(enfermedad[0] for enfermedad in enfermedades if enfermedad[1] == enfermedad_seleccionada)
                sintoma_id = next(sintoma[0] for sintoma in sintomas if sintoma[1] == sintoma_seleccionado)
                
                # Conectar a la base de datos
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="sistema_experto"
                )
                cursor = conexion.cursor()

                # Eliminar el registro de la tabla "enfermedad_sintoma"
                cursor.execute("DELETE FROM enfermedad_sintoma WHERE id_enfermedad = %s AND id_sintoma = %s", (enfermedad_id, sintoma_id))
                conexion.commit()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", "Registro guardado eliminado correctamente de la base de datos.")
                
                # Actualizar el Listbox eliminando el registro
                listbox_existentes.delete(seleccion_existentes)

                # Actualizar la suma de los pesos en la tabla "objeto"
                cursor.execute("SELECT SUM(peso) FROM enfermedad_sintoma WHERE id_enfermedad = %s", (enfermedad_id,))
                suma_pesos = cursor.fetchone()[0] or 0.0  # Si no hay más registros, suma será 0.0
                cursor.execute("UPDATE objeto SET suma = %s WHERE id = %s", (suma_pesos, enfermedad_id))
                conexion.commit()

                conexion.close()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el registro guardado: {e}")
        
        else:
            messagebox.showwarning("Advertencia", "Por favor selecciona un registro guardado para borrar.")

    def guardar_registros():
        enfermedad_seleccionada = enfermedad_var.get()
        
        # Verificar si la enfermedad seleccionada es válida
        if enfermedad_seleccionada == "Selecciona una enfermedad":
            messagebox.showerror("Error", "Por favor selecciona una enfermedad válida.")
            return
        
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_experto"
            )
            cursor = conexion.cursor()

            # Recorrer y guardar los registros añadidos en la lista
            for i in range(listbox_nuevos.size()):
                registro = listbox_nuevos.get(i).split(" - ")
                enfermedad_id = next(enfermedad[0] for enfermedad in enfermedades if enfermedad[1] == registro[0])
                sintoma_id = next(sintoma[0] for sintoma in sintomas if sintoma[1] == registro[1])
                peso = int(registro[2][:-1])  # Eliminar el símbolo '%' al convertir a entero
                
                # Verificar si el registro ya existe
                cursor.execute("SELECT * FROM enfermedad_sintoma WHERE id_enfermedad = %s AND id_sintoma = %s", (enfermedad_id, sintoma_id))
                if cursor.fetchone() is None:
                    # Insertar nuevo registro si no existe
                    cursor.execute("INSERT INTO enfermedad_sintoma (id_enfermedad, id_sintoma, peso) VALUES (%s, %s, %s)", (enfermedad_id, sintoma_id, peso))
            
            # Actualizar la tabla "objeto" con la suma de los pesos
            cursor.execute("SELECT SUM(peso) FROM enfermedad_sintoma WHERE id_enfermedad = %s", (enfermedad_id,))
            suma_pesos = cursor.fetchone()[0]
            
            # Actualizar la columna "suma" en la tabla "objeto" con el valor total de los pesos
            cursor.execute("UPDATE objeto SET suma = %s WHERE id = %s", (suma_pesos, enfermedad_id))
            
            conexion.commit()
            messagebox.showinfo("Éxito", "Registros guardados exitosamente.")
            
            # Limpiar los campos después de guardar
            enfermedad_var.set("Selecciona una enfermedad")
            sintoma_var.set("Selecciona un sintoma")
            peso_entry.delete(0, END)
            listbox_nuevos.delete(0, END)
            listbox_existentes.delete(0, END)
            
            # Limpiar la imagen de la enfermedad seleccionada
            imagen_label.config(image="")
            imagen_label.image = None  # Eliminar referencia a la imagen
            
            # Habilitar nuevamente el menú de selección de enfermedades
            option_menu.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        
        finally:
            conexion.close()


    # Botones para Añadir, Borrar y Guardar
    boton_anadir = tk.Button(cuadro_relacion_root, text="Añadir", command=anadir_registro)
    boton_anadir.place(x=300, y=300)

    boton_borrar = tk.Button(cuadro_relacion_root, text="Borrar", command=borrar_registro)
    boton_borrar.place(x=365, y=765)

    boton_guardar = tk.Button(cuadro_relacion_root, text="Guardar", command=guardar_registros)
    boton_guardar.place(x=152, y=765)
    
    # Crear el botón "Borrar registro guardado" y colocarlo en la interfaz
    boton_borrar_guardado = tk.Button(cuadro_relacion_root, text="Borrar registro guardado", command=borrar_registro_guardado)
    boton_borrar_guardado.place(x=870, y=765)

    # Botón para cancelar la operación
    def cancelar():
        enfermedad_seleccionada = enfermedad_var.get()
        
        # Verificar si la enfermedad seleccionada es válida antes de continuar
        if enfermedad_seleccionada == "Selecciona una enfermedad":
            messagebox.showerror("Error", "No hay nada que cancelar, por favor selecciona una enfermedad válida.")
            return
        
        # Restablecer los campos a su valor inicial
        enfermedad_var.set("Selecciona una enfermedad")
        sintoma_var.set("Selecciona un sintoma")
        peso_entry.delete(0, END)
        listbox_nuevos.delete(0, END)
        
        # Limpiar la imagen de la enfermedad seleccionada
        imagen_label.config(image="")
        imagen_label.image = None  # Eliminar referencia a la imagen
        
        # Habilitar nuevamente la selección de enfermedad
        option_menu.config(state="normal")


    boton_cancelar = tk.Button(cuadro_relacion_root, text="Cancelar", command=cancelar)
    boton_cancelar.place(x=590, y=765)

    cuadro_relacion_root.mainloop()
