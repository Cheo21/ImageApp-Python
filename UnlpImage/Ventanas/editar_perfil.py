import PySimpleGUI as sg
from PIL import Image
import io
import os
import json
from ..Clases.Usuario import Usuario
from datetime import datetime
from ..Clases.log import añadir_log as AL

ruta_json = os.path.join("UnlpImage","Ventanas","Clases","info_perfil.json")

def obtener_fecha():
    """
    Obtiene la fecha del instante en el que se ejecuta,para guardar
    la última modificación en el csv
    """
    timestamp = datetime.timestamp(datetime.now())
    fecha = int(timestamp)
    return fecha

def validarUsuario(usuario: Usuario) -> bool:
        print(f"Nombre: {usuario.nombre}, edad: {usuario.edad},  genero: {usuario.genero_autopercibido}, url: {usuario.url_avatar}")
        if (
            usuario.nombre == ""
            or not usuario.edad.isnumeric()
            or usuario.genero_autopercibido == ""
            or usuario.url_avatar == ""
        ):
            return False
        else:
            return True

def generarImagen(ruta):
    image = Image.open(ruta) 
    image.thumbnail((200, 200))            
    bio = io.BytesIO() 
    image.save(bio, format="PNG")    
    return bio.getvalue()


def actualizar_json(usuario: Usuario):
    if os.path.isfile(ruta_json):
        with open (ruta_json, "r+") as arch_json:
            lista_perfiles = json.load(arch_json)
            for perfil in lista_perfiles:
                if perfil["Nick"] == usuario.alias:
                    perfil["Nombre"] = usuario.nombre
                    perfil["Edad"] = usuario.edad
                    perfil["Genero"] = usuario.genero_autopercibido
                    perfil["Image"] = usuario.url_avatar
                    break
            arch_json.seek(0)
            json.dump(lista_perfiles, arch_json, indent=4)
            arch_json.truncate()
def genero_txt(usuario):
    return usuario.genero_autopercibido if usuario.genero_autopercibido not in ("Femenino", "Masculino") else ""

def run_editarPerfil(usuario: Usuario):

    # Definir los elementos del formulario
    formulario = [
        [sg.Text('Nombre:'), sg.InputText(key='-NOMBRE-', size=(10,10), default_text=usuario.nombre)],
        [sg.Text('Edad:'), sg.InputText(default_text=usuario.edad, key='-EDAD-')],
        [sg.Text('Género:')],
        [sg.Radio('Masculino', "genero", enable_events=True, key='-MASCULINO-', default=(usuario.genero_autopercibido == "Masculino")), sg.Radio('Femenino', "genero", enable_events=True, key='-FEMENINO-', default=(usuario.genero_autopercibido=="Femenino"))],
        [sg.Radio('Otro', "genero", default=(not (usuario.genero_autopercibido in ("Femenino", "Masculino"))), key='-OTRO-', enable_events=True)],
        [sg.InputText(key='-OTRO-TEXTO-', default_text=genero_txt(usuario), disabled=True,size=(10,10))],
        [sg.Button('Actualizar', key="-ACTUALIZAR-"), sg.Button('Borrar', key="-BORRAR-")]
    ]

    

    perfil = [[sg.Image(
                data=generarImagen(usuario.url_avatar),
                key  = "-IMAGEN-",
                pad = ((100,100),(0,0))
            )],
            [ sg.Text(''), sg.Push(), sg.In(size=(20,1), disabled=True, enable_events=True, key='-REPO-IMAGEN-', default_text=usuario.url_avatar), sg.FileBrowse('Seleccionar',enable_events=True, key='prueba' )]
            ]
            


    layout = [[sg.Text("EDITAR PERFIL"), sg.Push(), sg.Button("Volver", size=(10,2), key="-VOLVER-")],
            [sg.Column(formulario, pad=(0,100,0,0)), sg.Push(), sg.Column(perfil)]
            ]

    # Crear la ventana
    window = sg.Window('Formulario', layout, size=(600, 500), finalize=True, resizable=True)

    # Loop principal para leer los eventos de la ventana
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event =="-VOLVER-":
            break
        if event == "-REPO-IMAGEN-":
            imagen_nueva = values["-REPO-IMAGEN-"]
            window["-IMAGEN-"].update(data=generarImagen(imagen_nueva)              
            )
        elif event == '-OTRO-':
            # Habilitar el campo de texto si el usuario selecciona la opción 'Otro'
            window['-OTRO-TEXTO-'].update(disabled=False)
        elif event == '-MASCULINO-' or event == '-FEMENINO-':
            # Deshabilitar el campo de texto si el usuario selecciona la opción 'Masculino' o 'Femenino'
            window['-OTRO-TEXTO-'].update(disabled=True)
            window["-OTRO-"].update(value= "")
        elif event == '-ACTUALIZAR-':
            # Se creao un objeto usuario auxiliar
            usuario_aux = Usuario()
            # Obtener los valores de los campos del formulario
            usuario_aux.nombre = values['-NOMBRE-']
            usuario_aux.edad = values['-EDAD-']
            if values["-REPO-IMAGEN-"]:
                usuario_aux.url_avatar = values["-REPO-IMAGEN-"]
            if values['-MASCULINO-']:
                usuario_aux.genero_autopercibido = 'Masculino'
            elif values['-FEMENINO-']:
                usuario_aux.genero_autopercibido = 'Femenino'
            elif values['-OTRO-']:
                usuario_aux.genero_autopercibido = values['-OTRO-TEXTO-']
           
            if validarUsuario(usuario_aux):
                #actualizar_json(usuario)
                actualizar_json(usuario_aux)
                usuario = usuario_aux
                # Mostrar una ventana emergente de confirmación
                sg.popup('Datos actualizados!')
                AL(usuario_aux.nombre, "modificar_perfil", obtener_fecha())
            else:
                sg.PopupError("Valor no valido", title="Error")    
    # Cerrar la ventana al salir del loop principal
    window.close()
    return usuario
