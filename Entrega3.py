import random
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure  # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore
import cv2
import os
import numpy as np

def generar_carretera(longitud_carretera=20, paso=1):
    lista_puntos = [(0, 0)]  # Punto inicial
    puntos_visitados = set(lista_puntos)  # Usar un conjunto para verificar puntos visitados rápidamente

    while len(lista_puntos) < longitud_carretera + 1:  # Asegurar la longitud deseada
        x_actual, y_actual = lista_puntos[-1]

        posibles_puntos = [
            (x_actual + dx, y_actual + dy)
            for dx in range(-paso, paso + 1)
            for dy in range(-paso, paso + 1)
            if (dx != 0 or dy != 0) and (x_actual + dx, y_actual + dy) not in puntos_visitados
        ]

        if posibles_puntos:
            x_nuevo, y_nuevo = random.choice(posibles_puntos)
            lista_puntos.append((x_nuevo, y_nuevo))
            puntos_visitados.add((x_nuevo, y_nuevo))
        else:
            break

    # Asegurar que cada punto solo conecta a un punto y no apunta a más de uno
    nueva_lista_puntos = [lista_puntos[0]]
    for i in range(1, len(lista_puntos)):
        nuevo_punto = lista_puntos[i]
        if nuevo_punto not in nueva_lista_puntos:
            nueva_lista_puntos.append(nuevo_punto)

    return nueva_lista_puntos

def mostrar_en_ventana(carretera, collage, nombres):
    # Crear una ventana de tkinter
    root = tk.Tk()
    root.title("Visualización de Carretera y Collage")
    root.geometry("1000x1000")  # Ajustar tamaño de la ventana aquí

    # Crear una figura de matplotlib
    fig = Figure(figsize=(10, 12), dpi=100)

    # Subplot/gráfica para la carretera
    grafica1 = fig.add_subplot(211)
    x_puntos, y_puntos = zip(*carretera)
    grafica1.plot(x_puntos, y_puntos, marker='o')
    grafica1.set_xlabel('X')
    grafica1.set_ylabel('Y')
    grafica1.set_title('Camino de carretera procedural')
    grafica1.grid(True)

    # Subplot para el collage
    grafica2 = fig.add_subplot(212)
    grafica2.imshow(cv2.cvtColor(collage, cv2.COLOR_BGR2RGB))
    grafica2.axis('off')  # No mostrar ejes
    grafica2.set_title('Elementos de la zona')

    # Ajustar el espacio para nombres debajo de las imágenes
    collage_height = collage.shape[0]
    new_width = 280
    new_height = 300

    # Calcular la posición vertical para los textos
    text_y_pos = collage_height + 20 + len(nombres) * 20

    # Añadir nombres de las carpetas debajo de las imágenes
    for idx, nombre in enumerate(nombres):
        x_offset = idx * new_width + new_width / 2
        grafica2.text(x_offset, text_y_pos, nombre, ha='center', fontsize=12, color='black')

    # Ajustar el tamaño del subplot para dejar espacio para las etiquetas
    grafica2.set_ylim(text_y_pos + 30, -50)

    # Crear un canvas de tkinter y agregar la figura de matplotlib
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Botón para cerrar la ventana
    btn = ttk.Button(master=root, text="Cerrar", command=root.quit)
    btn.pack(side=tk.BOTTOM)

    # Ejecutar el bucle principal de tkinter
    tk.mainloop()

def generar_collage():
    # Directorio de entrada de las imágenes (se debe cambiar dependiendo de dónde esté guardada la carpeta)
    ubi_imagenes = "C:/Users/nicoc/OneDrive/Documentos/Entrega 3/Imagenes-Entrega-3"

    # Obtener la lista de carpetas en el directorio
    if not os.path.exists(ubi_imagenes):
        print(f"El directorio {ubi_imagenes} no existe.")
        return None, None

    folders_names = os.listdir(ubi_imagenes)
    print(folders_names)

    # Resolución deseada
    new_width = 300
    new_height = 300

    # Lista para almacenar las imágenes redimensionadas y sus nombres de carpeta
    images = []
    nombres = []

    for folder_name in folders_names:
        # Ruta completa de la carpeta de imágenes
        folder_path = os.path.join(ubi_imagenes, folder_name)

        # Verificar si la carpeta es un directorio
        if not os.path.isdir(folder_path):
            continue

        # Obtener la lista de nombres de archivos en la carpeta
        files_names = os.listdir(folder_path)

        # Verificar si hay imágenes en la carpeta
        if len(files_names) > 0:
            # Elegir una imagen aleatoria de la carpeta
            image_name = random.choice(files_names)
            image_path = os.path.join(folder_path, image_name)

            # Leer la imagen
            image = cv2.imread(image_path)

            # Verificar si la imagen se leyó correctamente
            if image is None:
                print(f"No se pudo leer la imagen: {image_path}")
                continue

            # Cambiar la resolución de la imagen
            resized_image = cv2.resize(image, (new_width, new_height))

            # Agregar la imagen redimensionada y su nombre de carpeta a las listas
            images.append(resized_image)
            nombres.append(folder_name)
        else:
            print(f"No se encontraron imágenes en la carpeta: {folder_path}")

    # Calcular el tamaño del collage
    num_images = len(images)
    if num_images > 0:
        collage_width = new_width * num_images
        collage_height = new_height

        # Crear una imagen vacía para el collage
        collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

        # Pegar cada imagen en el collage
        for idx, img in enumerate(images):
            x_offset = idx * new_width
            collage[0:new_height, x_offset:x_offset + new_width] = img

        return collage, nombres
    else:
        print("No se encontraron imágenes en las carpetas.")
        return None, None

# Generar carretera
carretera = generar_carretera(longitud_carretera=20, paso=2)

# Generar collage
collage, nombres = generar_collage()

# Verificar si el collage fue generado correctamente
if collage is not None:
    # Mostrar carretera y collage en una ventana
    mostrar_en_ventana(carretera, collage, nombres)
else:
    print("No se pudo generar el collage.")
