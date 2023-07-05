import PySimpleGUI as sg
import os
import csv
from ..Clases.Usuario import Usuario as User
from ..Clases.log import añadir_log as AL
from .etiquetarimagen import obtener_fecha as OF

ruta_completa = os.path.abspath(os.path.dirname(__file__)) # El path absoluto,del path de la carpeta que contiene a este archivo
#print(ruta_completa) #Esto para saber si funca
ruta_unlp = os.path.abspath(os.path.dirname(ruta_completa))
#print(ruta_completa)
ruta_completa = os.path.join(ruta_unlp,"Assets","configuracionCSV.csv") # Uno eso con el nombre del csv
#print(ruta_completa)


def guardar_configuracion(values):
    """
    Esta función debería abrir el archivo y escribir la data
    """
    with open(ruta_completa,mode='w', newline='') as arch:
        escribir = csv.writer(arch)          
        escribir.writerow(['image-repo', 'collage-dir', 'meme-dir'])
        escribir.writerow([values['-REPO-IMAGEN-'], values['-DIRE-COLLAGE-'], values['-DIRE-MEMES-']])

def imprimir():
    """
    Módulo para leer el archivo e imprimirlo nada más,para comprobar si funciona bien
    """
    with open(ruta_completa, mode='r') as archivo:
        lector_csv = csv.reader(archivo, delimiter=',')  
        for linea in lector_csv:
            print(linea)

def layout():
    """
    El layout,separado en 3 layouts distintos 
    """
    title = [[sg.Text('Configuración', font=("Helvetica", 18), justification="left"), sg.Push(), sg.Button('Volver',key='-SALIR-', font= ("Helvetica", 18))]]

    layout = [
              [sg.Text(''), sg.Push(), sg.Text('Repositorio de imágenes'), sg.Push(), sg.Text('')],
              [sg.Text(''), sg.Push(), sg.In(size=(45,1), enable_events=True, key='-REPO-IMAGEN-'), sg.FolderBrowse('Seleccionar',initial_folder=ruta_unlp)],
              [sg.Text(''), sg.Push(), sg.Text('Directorio de collage'), sg.Push(), sg.Text('')],
              [sg.Text(''), sg.Push(), sg.In(size=(45,1), enable_events=True, key='-DIRE-COLLAGE-'), sg.FolderBrowse('Seleccionar',initial_folder=ruta_unlp)],
              [sg.Text(''), sg.Push(), sg.Text('Directorio de memes'), sg.Push(), sg.Text('')],
              [sg.Text(''), sg.Push(), sg.In(size=(45,1), enable_events=True, key='-DIRE-MEMES-'), sg.FolderBrowse('Seleccionar',initial_folder=ruta_unlp)] 
              ]
    
    subtitle = [[sg.Text(''), sg.Push(),sg.VPush()],      
                [sg.Push(),sg.Button('Guardar',key='-GUARDAR-',font=("Helvetica",16))]]    
    
    return [[title],
            [sg.Column(layout,justification="center")],
            [subtitle]]
            

def run():
    """
    El programa principal,con el bucle de eventos
    """
    window = sg.Window('Ventana de Configuración', layout(),finalize=True, resizable=True)    #le pase a la ventana TODO para que funcione
    window.set_min_size((600,400))         #tamaño mínimo

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == '-SALIR-':
            break
        #esto debería volver a la ventana anterior más que salir,se verá más adelante
        if event == '-GUARDAR-':
            guardar_configuracion(values)
            fecha = OF()
            AL(User.alias,'change_config',fecha) #FUNCIONA
            imprimir()
           
            break

    window.close()
