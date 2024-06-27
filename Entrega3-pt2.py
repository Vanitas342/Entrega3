import random
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
import os
import numpy as np

# Genera una lista de puntos para crear una carretera procedural
def generar_carretera_alt(longitud_carretera=20, paso=1):
    lista_puntos = [(0, 0)]  # Punto inicial
    puntos_visitados = {(0, 0)}  # Conjunto de puntos ya visitados

    # Direcciones posibles para moverse desde un punto
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    while len(lista_puntos) < longitud_carretera + 1:
        x_actual, y_actual = lista_puntos[-1]

        # Generar una lista de puntos posibles a moverse
        posibles_puntos = [
            (x_actual + dx * paso, y_actual + dy * paso)
            for dx, dy in direcciones
            if (x_actual + dx * paso, y_actual + dy * paso) not in puntos_visitados
        ]

        if posibles_puntos:
            # Elegir aleatoriamente un punto nuevo y agregarlo a la lista
            x_nuevo, y_nuevo = random.choice(posibles_puntos)
            lista_puntos.append((x_nuevo, y_nuevo))
            puntos_visitados.add((x_nuevo, y_nuevo))
        else:
            break  # Si no hay puntos posibles, salir del bucle

    return lista_puntos

# Muestra la carretera y el collage en una ventana de Tkinter
def mostrar_en_ventana_alt(carretera, collage, nombres):
    root = tk.Tk()
    root.title("Visualización de Carretera y Collage")
    root.geometry("1000x1000")

    fig = Figure(figsize=(10, 12), dpi=100)

    # Subplot para la carretera
    grafica1 = fig.add_subplot(211)
    x_puntos, y_puntos = zip(*carretera)
    
    # Dibujar la carretera
    grafica1.plot(x_puntos, y_puntos, color='black', linewidth=15)  # Línea gruesa para la carretera
    grafica1.plot(x_puntos[0], y_puntos[0], marker='o', color='red', markersize=10)  # Punto inicial en rojo
    
    # Añadir líneas centrales blancas para la carretera
    for i in range(len(x_puntos) - 1):
        x_mid = (x_puntos[i] + x_puntos[i + 1]) / 2
        y_mid = (y_puntos[i] + y_puntos[i + 1]) / 2
        grafica1.plot([x_puntos[i], x_mid], [y_puntos[i], y_mid], color='white', linewidth=5, linestyle='dashed')

    grafica1.set_xlabel('X')
    grafica1.set_ylabel('Y')
    grafica1.set_title('Camino de carretera procedural')
    grafica1.grid(True)

    # Subplot para el collage
    grafica2 = fig.add_subplot(212)
    grafica2.imshow(cv2.cvtColor(collage, cv2.COLOR_BGR2RGB))
    grafica2.axis('off')
    grafica2.set_title('Elementos de la zona')

    collage_height = collage.shape[0]
    new_width = 280

    # Añadir nombres de carpetas debajo del collage
    for idx, nombre in enumerate(nombres):
        x_offset = idx * new_width + new_width / 2
        grafica2.text(x_offset, collage_height + 20, nombre, ha='center', fontsize=12, color='black')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    btn = ttk.Button(master=root, text="Cerrar", command=root.quit)
    btn.pack(side=tk.BOTTOM)

    tk.mainloop()

# Genera un collage de imágenes a partir de un directorio dado (se debe cambiar dependiendo de dónde esté guardada la carpeta)
def generar_collage_alt():
    ubi_imagenes = "C:/Users/nicoc/OneDrive/Documentos/Entrega 3/Imagenes Entrega 3"

    if not os.path.exists(ubi_imagenes):
        print(f"El directorio {ubi_imagenes} no existe.")
        return None, None

    folders_names = os.listdir(ubi_imagenes)

    new_width, new_height = 300, 300

    images = []
    nombres = []

    # Procesa cada carpeta en el directorio
    for folder_name in folders_names:
        folder_path = os.path.join(ubi_imagenes, folder_name)
        if not os.path.isdir(folder_path):
            continue

        files_names = os.listdir(folder_path)
        if files_names:
            # Selecciona una imagen aleatoria de la carpeta
            image_path = os.path.join(folder_path, random.choice(files_names))
            image = cv2.imread(image_path)
            if image is not None:
                # Redimensiona la imagen y la añade a la lista
                resized_image = cv2.resize(image, (new_width, new_height))
                images.append(resized_image)
                nombres.append(folder_name)
            else:
                print(f"No se pudo leer la imagen: {image_path}")

    if images:
        # Crea un collage horizontal a partir de las imágenes
        collage = np.hstack(images)
        return collage, nombres
    else:
        print("No se encontraron imágenes en las carpetas.")
        return None, None

# Generar carretera
carretera_alt = generar_carretera_alt(longitud_carretera=20, paso=2)

# Generar collage
collage_alt, nombres_alt = generar_collage_alt()

# Verificar si el collage fue generado correctamente
if collage_alt is not None:
    mostrar_en_ventana_alt(carretera_alt, collage_alt, nombres_alt)
else:
    print("No se pudo generar el collage.")
