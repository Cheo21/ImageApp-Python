import PySimpleGUI as sg
import os
import io
import csv
import PIL
from PIL import Image, ImageTk, ImageOps, ImageDraw, Image
from .etiquetarimagen import path_csv #esto es para leer el csv de config
from .etiquetarimagen import encontrar_ruta
from .etiquetarimagen import existe_imagen
from .etiquetarimagen import obtener_fecha
from ..Clases.Usuario import Usuario as User
from ..Clases.log import añadir_log as AL
sg.theme("Purple")


if os.path.exists(os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),"Assets","configuracionCSV.csv")):
    ruta_csv = path_csv()
    print('existe el csv')
    print(ruta_csv)
else:
    ruta_csv = ""


def path_collage(ruta_csv):
    """
    Esta función lee lo que tiene el CSV en la segunda línea,para saber cual es el directorio de collage
    """
    ruta_csv = os.path.dirname(ruta_csv)
    with open (os.path.join(ruta_csv,'configuracionCSV.csv'), 'r' ,newline='',encoding="UTF-8") as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        contenido_csv = list(lector_csv)
        route = contenido_csv[1][1]
        print('ruta:')
        print(route)
    return route 

def guardar(aux1="",aux2="",aux3="",aux4=""):
    """
    Esta función recibe el nombre de las 4 variables,las asigna con un valor por defecto
    en el caso de que vengan vacías,y luego las agrega a la lista siempre que no estén vacías.
    Las 4 variables representan los nombres de las posibles 4 imágenes usadas.
    """
    imagenes = []
    if aux1 != "":
        imagenes.append(aux1)
    if aux2 != "":
        imagenes.append(aux2)
    if aux3 != "":
        imagenes.append(aux3)
    if aux4 != "":
        imagenes.append(aux4)
    return imagenes


def buscar_CSV(ruta):
    """
    Esta función busca si la imagen tiene etiquetas,es una copia de
    "buscar_imagen" en etiquetarimagen.py;solo que modificada para solamente
    recuperar las etiquetas de la imágen,y así chequear si tiene o no.
    """
    path_absoluto = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    path_absoluto = os.path.join(path_absoluto,"Assets")
    boolean=False
    with open(os.path.join(path_absoluto,'metadata.csv'), 'r', newline='',encoding="UTF-8") as archivo_csv: 
        datos_imagen_original = None    #Esto es un parche que cubre un caso que por algún motivo no debería pasar,pero puede pasar(?)
        lector_csv = csv.reader(archivo_csv)
        contenido_csv = list(lector_csv)
        for i, sublist in enumerate(contenido_csv):  
            if ruta in sublist:                  
                datos_imagen_original = sublist
                break
        if datos_imagen_original:
            etiqs = datos_imagen_original[7]
            if etiqs and etiqs != "No tiene":
                boolean=True
        else:
            etiqs=[]
        return boolean

def R_Image(ruta,dimensiones):
    """
    Esta función la copié de inicio,es literalmente la misma
    si la importaba me daba error de "import circular"
    Es para abrir imágenes.
    """
    img = Image.open(ruta)
    img.thumbnail(dimensiones)
    
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
def layout2():
    """
    Este es el layout de la segunda ventana,va a tener botones que se van a hacer
    visibles dependiendo de la plantilla elegida,y también previsualiza el collage
    """
    
    title =[[sg.Text("Generar collage",font=("Times New Roman",20),justification="left"),sg.Push(),sg.Button("Volver",size=(15,2) ,key="-volver-")],
            [sg.Text(''), sg.Push(),sg.Text('')],
            [sg.Text(''), sg.Push(),sg.Text('')]]
    layout =[[sg.FileBrowse('Seleccionar imagen 1',key="-IMG1-",initial_folder=ruta_csv,visible=False),sg.Button('Aceptar',key="-OK1-",visible=False)],
             [sg.FileBrowse('Seleccionar imagen 2',key="-IMG2-",initial_folder=ruta_csv,visible=False),sg.Button('Aceptar',key="-OK2-",visible=False)],
             [sg.FileBrowse('Seleccionar imagen 3',key="-IMG3-",initial_folder=ruta_csv,visible=False),sg.Button('Aceptar',key="-OK3-",visible=False)],
             [sg.FileBrowse('Seleccionar imagen 4',key="-IMG4-",initial_folder=ruta_csv,visible=False),sg.Button('Aceptar',key="-OK4-",visible=False)],

             [sg.Text("Ingrese Título",key="-titulo-",visible=False)],
             [sg.Input(size=(25, 1), key="-TITULO-",visible=False),sg.Button('Aceptar',key="-Acep-",visible=False)],

    ]
    previsual =[[sg.Image(key='-IMAGE-', size=(180,180),data="")],
                [sg.Button('Guardar',key='-GUARDAR-',font=("Helvetica",16))]]
    
    return [[title],
            [sg.Column(layout,justification="left"),sg.Push(), sg.Column(previsual,justification="right")]]

def layout():
    """
    Layout de la primera ventana,tiene los paths de las plantillas
    y tiene los botones que representan cada una de las 4 plantillas
    """
    path_absoluto = os.path.abspath(os.path.dirname(__file__))
    #print(path_absoluto)
    path_absoluto = os.path.abspath(os.path.dirname(path_absoluto))
    print(f"se va a imprimir {path_absoluto}")
    
    p1=os.path.join(path_absoluto,"Image","plantilla1.png")
    p2=os.path.join(path_absoluto,"Image","plantilla2.png")
    p3=os.path.join(path_absoluto,"Image","plantilla3.png")
    p4=os.path.join(path_absoluto,"Image","plantilla4.png")
    title =[[sg.Text("Elija una plantilla",font=("Times New Roman",20),justification="left"),sg.Push(),sg.Button("Volver",size=(15,2) ,key="-VOLVER-")]]
    layout =[ 
             [sg.Text(""),sg.Push(),sg.Text("")],
             [sg.Text(""),sg.Push(),sg.Text("")],
             [sg.Text(""),sg.Push(),sg.Text("")],
             [sg.Button(image_data=R_Image(p1,(100,100)),key="-plantilla1-"),
              sg.Button(image_data=R_Image(p2,(100,100)),key="-plantilla2-"),
              sg.Button(image_data=R_Image(p3,(100,100)),key="-plantilla3-"),
              sg.Button(image_data=R_Image(p4,(100,100)),key="-plantilla4-")], 
    ]
    #volver =[]   al final terminé moviendo el botón volver de lugar para que se parezca más a lo mostrado en el pdf del trabajo  
    return [[title],
            [sg.Column(layout=layout, expand_x=True, element_justification="center")]]
            #[sg.Column(layout=volver, expand_x=True, element_justification="right",pad=((0,0),(100,0)))]]


def run_collage(): 
    """
    "Primer bucle principal" esto ejecuta la primera
    ventana,la cual lleva a la segunda luego de elegir
    una plantilla
    """
    window = sg.Window("", layout(),finalize=True,resizable=True)
    window.set_min_size((500, 400))
    
    while True:
        event,values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        
        match event:
            case "-VOLVER-":
                window.close()
                break
            case "-plantilla1-":
                window.hide()
                plantilla=1
                run_Collage2(plantilla)
                window.un_hide()
            case "-plantilla2-":
                window.hide()
                plantilla=2
                run_Collage2(plantilla)
                window.un_hide()
            case "-plantilla3-":
                window.hide()
                plantilla=3
                run_Collage2(plantilla)
                window.un_hide()
            case "-plantilla4-":
                window.hide()
                plantilla=4
                run_Collage2(plantilla)
                window.un_hide()
    
    window.close()
def run_Collage2(plantilla):
    """
    Este es el bucle de eventos principal;el de la segunda ventana.
    crea la imágen antes de arrancar con los bucles y actualiza "-IMAGE-" para que la ventana
    arranque con un collage vacío,y después chequea que plantilla se eligió con un match
    para poder decidir que botones se van a mostrar,que representan la cantidad de 
    imágenes que se van a usar para el collage,y eso depende de la plantilla elegida
    En el bucle while,el programa chequea los eventos de las 4 imágenes. Dependiendo la plantilla
    elegida,con la variable "template" le paso a las distintas imágenes,los tamaños y 
    coordenadas a utilizar. Los botones que no se utilizen (por ej,imágen 4 en un collage
    de solamente 2 imágenes) tendrán vacío;que no afectan en nada al collage,pero a la 
    hora de guardarlo en el log,me encargué de que no se guarde el espacio vacío.
    """
    window = sg.Window("", layout2(),finalize=True,resizable=True)
    window.set_min_size((500, 400))
    collage = Image.new("RGB",(180,180))
    collage_tk = ImageTk.PhotoImage(collage)
    window["-IMAGE-"].update(data=collage_tk)
    window["-titulo-"].update(visible=True),window["-TITULO-"].update(visible=True),window["-Acep-"].update(visible=True)
    match plantilla:
            case 1 if plantilla ==1:
                window["-IMG1-"].update(visible=True),window["-IMG2-"].update(visible=True)
                window["-OK1-"].update(visible=True),window["-OK2-"].update(visible=True)
                template=[(90,180),(0,0),(90,0)]
            case 2 if plantilla ==2:
                window["-IMG1-"].update(visible=True),window["-IMG2-"].update(visible=True)
                window["-OK1-"].update(visible=True),window["-OK2-"].update(visible=True)
                template=[(180,90),(0,0),(0,90)]
            case 3 if plantilla ==3:
                window["-IMG1-"].update(visible=True),window["-IMG2-"].update(visible=True),window["-IMG3-"].update(visible=True),window["-IMG4-"].update(visible=True)
                window["-OK1-"].update(visible=True),window["-OK2-"].update(visible=True),window["-OK3-"].update(visible=True),window["-OK4-"].update(visible=True)
                template=[(90,90),(0,0),(90,0),(0,90),(90,90)]
            case 4 if plantilla ==4:
                window["-IMG1-"].update(visible=True),window["-IMG2-"].update(visible=True),window["-IMG3-"].update(visible=True)
                window["-OK1-"].update(visible=True),window["-OK2-"].update(visible=True),window["-OK3-"].update(visible=True)
                template=[(180,60),(0,0),(0,60),(0,120)]
    aux1=""
    aux2=""
    aux3=""
    aux4=""
    while True:
        event,values = window.read()
        print(event,values)
        if event == sg.WIN_CLOSED:
            break
        if event == "-volver-":
            window.close()
            break
        if event == "-OK1-":
            aux=values['-IMG1-']
            aux1=os.path.basename(aux)
            ruta = encontrar_ruta(aux)
            #print(ruta)
            existe = existe_imagen(ruta)
            if existe:
                b = buscar_CSV(ruta)
                if b:
                    aux= PIL.Image.open(aux)
                    aux=PIL.ImageOps.fit(aux,template[0])
                    collage.paste(aux,template[1])
                    collage_tk = ImageTk.PhotoImage(collage)
                    window["-IMAGE-"].update(data=collage_tk)
                else:
                    sg.popup('La imágen no está etiquetada')
            else:
                sg.popup('La imágen no se encuentra en el csv')    

        if event == "-OK2-":
            aux=values['-IMG2-']
            aux2=os.path.basename(aux)
            ruta = encontrar_ruta(aux)
            #print(ruta)
            existe = existe_imagen(ruta)
            if existe:
                b = buscar_CSV(ruta)
                if b:
                    aux= PIL.Image.open(aux)
                    aux=PIL.ImageOps.fit(aux,template[0])
                    collage.paste(aux,template[2])
                    collage_tk = ImageTk.PhotoImage(collage)
                    window["-IMAGE-"].update(data=collage_tk)
                else:
                    sg.popup('La imágen no está etiquetada')
            else:
                sg.popup('La imágen no se encuentra en el csv')  

        if event == "-OK3-":
            aux=values['-IMG3-']
            aux3=os.path.basename(aux)
            ruta = encontrar_ruta(aux)
            #print(ruta)
            existe = existe_imagen(ruta)
            if existe:
                b = buscar_CSV(ruta)
                if b:
                    aux= PIL.Image.open(aux)
                    aux=PIL.ImageOps.fit(aux,template[0])
                    collage.paste(aux,template[3])
                    collage_tk = ImageTk.PhotoImage(collage)
                    window["-IMAGE-"].update(data=collage_tk)
                else:
                    sg.popup('La imágen no está etiquetada')
            else:
                sg.popup('La imágen no se encuentra en el csv')

        if event == "-OK4-":
            aux=values['-IMG4-']
            aux4=os.path.basename(aux)
            ruta = encontrar_ruta(aux)
            #print(ruta)
            existe = existe_imagen(ruta)
            if existe:
                b = buscar_CSV(ruta)
                if b:
                    aux= PIL.Image.open(aux)
                    aux=PIL.ImageOps.fit(aux,template[0])
                    collage.paste(aux,template[4])
                    collage_tk = ImageTk.PhotoImage(collage)
                    window["-IMAGE-"].update(data=collage_tk)
                else:
                    sg.popup('La imágen no está etiquetada')
            else:
                sg.popup('La imágen no se encuentra en el csv')


        if event == '-Acep-':
            draw= PIL.ImageDraw.Draw(collage)
            draw.text((10,10),values['-TITULO-'])
            collage_tk = ImageTk.PhotoImage(collage)
            window["-IMAGE-"].update(data=collage_tk)


        if event == '-GUARDAR-':
            imagenes = guardar(aux1,aux2,aux3,aux4)
            imagenes_string = ';'.join(imagenes)
            ruta_Guardado = path_collage(ruta_csv)
            try:
                nombre_collage = sg.popup_get_text('Ingrese el nombre del collage', default_text='collage', title='Save Collage')
                nombre_archivo = os.path.join(ruta_Guardado,nombre_collage +'.jpg')
                collage.save(nombre_archivo)
                sg.popup("¡Collage guardado exitosamente!")
            except TypeError:
                sg.popup("No ingresó un nombre para el collage")
            fecha = obtener_fecha()
            AL(User.alias,'new_collage',fecha,imagenes_string,values['-TITULO-'])  

if __name__ == "__main__":
    run_collage()
