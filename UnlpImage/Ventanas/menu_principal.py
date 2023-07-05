import os 
from PIL import Image
import io
import PySimpleGUI as sg
from .configuracion import run 
from .editar_perfil import run_editarPerfil
from ..Clases.Usuario import Usuario
from .etiquetarimagen import run as run_etiquetar
from .config import config_ventanas as conf_vent
from .meme import run_meme
from .collage import run_collage
from .ayuda import ventana_ayuda

ruta_directorio = os.path.dirname(os.path.abspath(__file__))
ruta_icono = os.path.normpath(os.path.join(ruta_directorio, "../Assets/icono.png"))


def generarImagen(ruta):
    image = Image.open(ruta) 
    image.thumbnail((20, 20))            
    bio = io.BytesIO() 
    image.save(bio, format="PNG")    
    return bio.getvalue()


def run_menu_princial(usuario: Usuario):
    #Layout de la ventana
    layout = [[sg.Image(data=generarImagen(usuario.url_avatar),key="-EDITAR-PERFIL-", enable_events=True, pad=(0,20)), sg.Push(), sg.Column([[sg.Button("Configuraciones", key="-CONFIGURACION-")], [sg.Button("Ayuda", key="-AYUDA-")]])],
            [sg.Column([[sg.Button("Etiquetar Imagen", size=(20,2), key="-ETIQUETAR-IMAGEN-")],
                        [sg.Button("Generar MEME", size=(20,2), key="-GENERAR-MEME-")],
                        [sg.Button("Generar College", size=(20,2), key="-GENERAR-COLLAGE-")],
                        [sg.Button("Salir", size=(20,2), key="-SALIR-")]], 
                        justification="center", pad=(0,100,0,0))]
            
            ]


    window = sg.Window('Menu principal', layout, size=(600, 500))

    while True:
        
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "-SALIR-"):
            break
        elif event == "-AYUDA-":
            window.hide()
            ventana_ayuda()
            window.un_hide()
        elif event == "-CONFIGURACION-":
            window.hide()
            run() ##Esto es una prueba para saber como linkear entre las pantallas, funciona
            window.un_hide()
        elif event == "-EDITAR-PERFIL-":
            window.hide()
            usuario = run_editarPerfil(usuario)
            window.un_hide()
            window["-EDITAR-PERFIL-"].update(data=generarImagen(usuario.url_avatar))
        elif event == "-ETIQUETAR-IMAGEN-":
            window.hide()
            run_etiquetar( )
            window.un_hide()
        elif event == "-GENERAR-MEME-":
            window.hide()
            run_meme(usuario)
            window.un_hide()
        elif event == "-GENERAR-COLLAGE-":
            window.hide()
            run_collage()
            window.un_hide()    
    window.close()


