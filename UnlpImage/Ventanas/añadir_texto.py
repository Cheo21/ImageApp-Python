import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from ..Clases.log import añadir_log as AL
import io
import os

sg.theme("Purple")
path_absoluto = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def obtener_fecha():
    """
    Obtiene la fecha del instante en el que se ejecuta,para guardar
    la última modificación en el csv
    """
    timestamp = datetime.timestamp(datetime.now())
    fecha = int(timestamp)
    return fecha

#Esto es un potencial error
def guardar_imagen_modificada(imagen_modificada):

    ruta = sg.filedialog.asksaveasfilename(
    defaultextension='.png',
    filetypes=[('Archivos PNG', '*.png')]
    )
    try:
        imagen_modificada.save(ruta)
        print("Imagen modificada guardada exitosamente.")
    except (FileNotFoundError, IOError) as e:
        print(f"Error al guardar la imagen modificada: {e}")

def generar_imagen(image):
    """
    Genera una miniatura de la imagen en la ruta especificada.

    Args:
        ruta (objeto imagen): imagen.

    Returns:
        bytes: Contenido de la imagen en formato de bytes.
    """
    try:
        image.thumbnail((200,200))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        return bio.getvalue()
    except (FileNotFoundError, IOError) as e:
        print(f"Error al generar la imagen: {e}")
        return None

def obtener_fuentes_disponibles():
    lista_fuentes = []
    carpeta_fuentes = os.path.join(path_absoluto, "Assets", "fuentes")
    for archivo in os.listdir(carpeta_fuentes):
        ruta_fuente = os.path.join(carpeta_fuentes, archivo)
        try:
            fuente = ImageFont.truetype(ruta_fuente, size=1)
            nombre_fuente = fuente.getname()[0]
            print(nombre_fuente)
            if nombre_fuente not in lista_fuentes:
                lista_fuentes.append(nombre_fuente)
        except (OSError, IOError):
            continue
    return lista_fuentes

def guardar_texto(copia_imagen, texto, fuente_tamanio, ruta_fuente, text_box):
    draw = ImageDraw.Draw(copia_imagen)
    fuente = ImageFont.truetype(ruta_fuente, fuente_tamanio)
    pos_x = text_box["top_left_x"]
    pos_y = text_box["top_left_y"]
    draw.text((pos_x, pos_y), texto, font=fuente)


def tam_box(x1,y1,x2,y2):
    return(x2-x1, y2-y1)

def calcular_tamanio_fuente(draw, texto, path_fuente, box):
    print(f"Tupla de cordenadas del box: {box}")
    tam_contenedor = (box[2] - box[0], box[3] - box[1])
    print(f"El ancho del contenedor diponible: {tam_contenedor}")
    retorno = 0
    for tam in range(200, 5, -5):
        fuente = ImageFont.truetype(path_fuente, tam)
        box_texto = draw.textbbox((0, 0), texto, font=fuente)
        print(box_texto)
        tam_box_texto = tam_box(*box_texto)
        print(f"El ancho del contenedor actual con la fuente actual: {tam_box_texto}")
        if tam_box_texto[0] <= tam_contenedor[0] and tam_box_texto[1] <= tam_contenedor[1]:
            print(f"Entro y guardo el tamaño {tam}")
            retorno = tam
            break
    return retorno


def tomar_valores_inputs(values, data):
    valores = []
    text_boxes = data["text_boxes"]
    for i in range(len(text_boxes)):
        valores.append(values[f"-INPUT-TEXT-{i}-"])
    return valores

def tomar_valor_fuente(values):
    nombre_fuente = values["-FUENTE-SELECIONADA-"].split(":")[0].strip()
    carpeta_fuentes = os.path.join(path_absoluto, "Assets", "fuentes")
    print(f"ruta de la carpeta existe:{os.path.isdir(carpeta_fuentes)}")
    ruta_fuente = os.path.join(carpeta_fuentes, nombre_fuente + ".ttf")
    print(f"ruta de la fuente: {os.path.isfile(ruta_fuente)}")
    return ruta_fuente

def mostrar_previsualizacion_texto(imagen_original, data, values):
    copia_imagen = imagen_original.copy() 
    draw = ImageDraw.Draw(copia_imagen)
    textos = tomar_valores_inputs(values, data)
    #solo me esta capturando una sola letra y de un solo input
    print(f"Esto es los textos de los inputs: {textos}")
    fuente = tomar_valor_fuente(values)
    for texto, text_box in zip(textos, data["text_boxes"]):
        fuente_tamanio = calcular_tamanio_fuente(draw, texto, fuente, (text_box["top_left_x"],text_box["top_left_y"],text_box["bottom_right_x"],text_box["bottom_right_y"]))
        guardar_texto(copia_imagen, texto, fuente_tamanio, fuente, text_box)
    return copia_imagen, textos
        

def generar_inputs(data):
    lista = []
    text_boxes = data["text_boxes"]
    for i in range(len(text_boxes)):
        text_box = text_boxes[i]
        lista.append([sg.Text(f"Input {i+1}: "), sg.Input("", key=f"-INPUT-TEXT-{i}-")])
    
    lista.append(
        [sg.Text("Seleccione la fuente: "), sg.Combo(obtener_fuentes_disponibles(), key="-FUENTE-SELECIONADA-", default_value="Roboto")]
    )
    lista.append([sg.Button("Generar imagen", key="-GENERAR-IMAGEN-"), sg.Button("Guardar imagen", key="-GUARDAR-IMAGEN-",)])
    return lista



def layout(data):
    title =[
    [
        sg.Text(
            "Generador de Memes",font=("Times New Roman",20),justification="left"
        )
    ],
    generar_inputs(data),
    [sg.Image(
        data="",
        key="-IMAGEN-",
        pad=((100, 100), (0, 0))
    ), ]
    ]   
    volver =[
        [sg.Button("Volver",size=(15,2) ,key="-VOLVER-")]
    ]     
    return [
        title,
        [sg.Column(layout=volver, expand_x=True, element_justification="right",pad=((0,0),(300,0)))]]

def generar_meme(data, url, user):  
    #print(f"Esta es la que importa: {url}")
    window = sg.Window("Generador de MEME", layout(data),finalize=True,size=(600, 500), resizable=True)
    window.set_min_size((500, 400))
    imagen_modificada= ""
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "-GENERAR-IMAGEN-":
            textos = []
            imagen_original = Image.open(url)       
            imagen_modificada, textos = mostrar_previsualizacion_texto(imagen_original,data,values)
            if(imagen_modificada):
                 window["-IMAGEN-"].update(data=generar_imagen(imagen_modificada))
        if event == "-GUARDAR-IMAGEN-":
            imagen_original = Image.open(url)       
            imagen_modificada, textos = mostrar_previsualizacion_texto(imagen_original,data,values)
            if(imagen_modificada):
                 window["-IMAGEN-"].update(data=generar_imagen(imagen_modificada))
            guardar_imagen_modificada(imagen_modificada)
            sg.popup("Se guardo correctamente la imagen.")
            AL(user.alias,'new_meme', obtener_fecha() ,data["image"], ";".join(textos))
            break 
        elif event == "-VOLVER-":
            window.close()
            break
    
    window.close()


if __name__ == "__main__":
    generar_meme()


#Dudas / problemas: no me toma todos los inputs ademas que solo toma la ultima letra del primer input
#      