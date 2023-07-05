import PySimpleGUI as sg
from .añadir_texto import generar_meme
import json
import csv
from PIL import Image
import os
import io

sg.theme("Purple")

# Ruta del archivo CSV de configuración
path_csv_config = os.path.join("UnlpImage", "Assets", "configuracionCSV.csv")





def generarLista(data):
    """
    Genera una lista de radio buttons para cada template de meme disponible.

    Returns:
        list: Lista de elementos de la interfaz gráfica para los radio buttons.
    """
    lista = []
    for meme in data:
        lista.append([sg.Radio(meme['name'], 'memes', key=meme['image'], enable_events=True)])
    return lista

def buscarMapMeme(values, data):
    """
    Busca en el JSON la informacion perteneciente al meme seleccioando en el radio button.

    Args: 
        values (dict): Diccionario con los valores actuales de la interfaz gráfica.

    Returns:
        Dic: Template de meme seleccionado.
    
    """
    for meme in data:
        if values[meme['image']]:
            print(meme)
            return meme
    return None


def buscarImagen(values, data):
    """
    Busca el template de meme seleccionado según los valores de los radio buttons.

    Args:
        values (dict): Diccionario con los valores actuales de la interfaz gráfica.

    Returns:
        str: Nombre del template de meme seleccionado.
    """
    for meme in data:
        if values[meme['image']]:
            return meme['image']
    return None

def generarImagen(ruta):
    """
    Genera una miniatura de la imagen en la ruta especificada.

    Args:
        ruta (str): Ruta de la imagen.

    Returns:
        bytes: Contenido de la imagen en formato de bytes.
    """
    try:
        image = Image.open(ruta)
        image.thumbnail((200, 200))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        return bio.getvalue()
    except (FileNotFoundError, IOError) as e:
        print(f"Error al generar la imagen: {e}")
        return None

def layout(path_dir_memes, data):
    """
    Define la estructura del diseño de la ventana de la aplicación.

    Returns:
        list: Lista con la estructura del diseño de la ventana.
    """
    title = [
        [
            sg.Text(
                "Generador de memes", font=("Times New Roman", 20), justification="left"
            )
        ]
    ]
    volver = [
        [sg.Button("Volver", size=(15, 2), key="-VOLVER-")]
    ]
    return [
        [title,
        
            generarLista(data),
            sg.Image(
                data=generarImagen(os.path.join(path_dir_memes, '')),
                key="-IMAGEN-",
                pad=((100, 100), (0, 0))
            )
        ],
        [sg.Button("Mostrar miniatura", key="-MOSTRAR-IMAGEN-"), sg.Button("Seleccionar imagen", key="-SELECCIONAR-IMAGEN-")],
        [sg.Column(layout=volver, expand_x=True, element_justification="right", pad=((0, 0), (300, 0)))]
    ]

def run_meme(user):
    #Inicializamos unas variables utiles:
    # Leer la configuración del archivo CSV
    if os.path.exists(path_csv_config):
        with open(path_csv_config, 'r') as file:
                lector = csv.reader(file)
                next(lector)
                fila = next(lector)
                dir_meme = fila[2]
    else:
        sg.popup_error("No existe csv valido")
        print(f"Error al leer el archivo CSV de configuración")
        return 
    
    # Rutas de los archivos
    path_template_memes = os.path.join("UnlpImage", "Clases", "template_memes.json")
    path_dir_memes = os.path.normpath(dir_meme)

    # Cargar los datos del archivo JSON de templates de memes
    try:
        with open(path_template_memes, 'r') as file:
            data = json.load(file)
    except FileNotFoundError as e:
        print(f"Error al leer el archivo JSON de templates de memes: {e}")
        exit(1)


    """
    Ejecuta la aplicación principal del generador de memes.
    """
    window = sg.Window("Generador de MEME", layout(path_dir_memes, data), finalize=True, size=(600, 500), resizable=True)
    window.set_min_size((500, 400))
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "-MOSTRAR-IMAGEN-":
            nombre_meme = buscarImagen(values,data)
            if nombre_meme:
                ruta_imagen = os.path.join(path_dir_memes, nombre_meme)
                imagen_generada = generarImagen(ruta_imagen)
                if imagen_generada:
                    window["-IMAGEN-"].update(data=imagen_generada)
        elif event == "-SELECCIONAR-IMAGEN-":
            nombre_meme = buscarImagen(values, data)
            if nombre_meme:
                ruta_imagen = os.path.join(path_dir_memes, nombre_meme)
            info_meme = buscarMapMeme(values, data)
            print(ruta_imagen)
            window.close()
            generar_meme(info_meme, ruta_imagen, user)
        elif event == "-VOLVER-":
            break
    
    window.close()

if __name__ == "__main__":
    run_meme()
