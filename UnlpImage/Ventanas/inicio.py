import PySimpleGUI as sg
import json
import os
import io
from PIL import Image
from .perfil import run_Perfil
from ..Clases.Usuario import Usuario
from .menu_principal import run_menu_princial


sg.theme("Purple")
ruta_json = os.path.join("UnlpImage","Assets","info_perfil.json") 

try: 
    with  open(ruta_json,'r+',encoding="UTF-8") as archivo:
        info = json.load(archivo)

except (FileNotFoundError , json.JSONDecodeError):       
    ruta_image =[]
else: 
    #Guardo las direcciones de las imagenes para cada perfil
    ruta_image= [perfil["Image"] for perfil in info]
    #Guardo el Nick de cada perfil
    nombres_perfiles = [perfil["Nick"] for perfil in info]

#Abro la imagen mas para luego usarlo de boton
nuevoP = os.path.join("UnlpImage","Image","mas.png")

#Lo agrego ruta_image para despues usarlo todo junto
ruta_image.insert(0,nuevoP)  
breakpoint
#Redimensiono la imagen del avatar
def red_image(ruta,dimensiones):
    img = Image.open(ruta)
    img.thumbnail(dimensiones)
    
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

#Creo el layout 
def layout() : 
    avatar =[
            #Creo los botones, para que cada boton sea la imagen del avatar que eligio el usuario
            [sg.Button(
             image_data = red_image(ruta,(100,100)),
             key ="-NUEVOPERFIL-" if posicion == 0 else f"-SELECCIONARIMAGEN-{posicion}", #si es la primera imagen la contraseña va a ser nuevo perfil el resto va a ser seleccionarimagen + la posicion para poder diferencialas entre si
             button_color = (sg.theme_button_color()),
             border_width=0, # Sin borde

            )for posicion,ruta in reversed(list(enumerate(ruta_image[:5])))]
    ]
    #Para ubicar los botones
    avatar_column = sg.Column(
        avatar,
        expand_x=True,
        element_justification="center",
        pad = ((40,0),(60,0)),
    )
     
    verMas =[
        #Si el tamaño de ruta image es +5, es decri hay mas de 4 perfiles guardados (el de la pos 0 siempre esta porque es el mas) muestro el boton Ver Más
        [sg.Button( "Ver más > ",key="-MOSTRARMAS-",visible= len(ruta_image) > 5)],
    ]
    
    #En el caso de que haya mas perfles los muestro al tocar el boton mas 
    masBotones =[
            [sg.Button(
             image_data = red_image(ruta,(80,80)),
             key =f"-SELECCIONARIMAGEN-{posicion + 5}", #le sumo 5 porque son los avatars de los perfiles restante y no de los 5 que ya mostre y como uso la posicion para el jsno siempre los que esten aca van a estar 5 posiciones mas
             button_color = (sg.theme_button_color()),
             border_width=0, 

            )for posicion,ruta in reversed(list(enumerate(ruta_image[5:])))]#Tomo todos los restantes menos los primeros 5
    ]
   #Para ubicar los demas botones
    masBotones_column = sg.Column(
        masBotones,
        expand_x=True,
        key = "-MASPERFILES-",
        element_justification="center",
        visible = False,
        pad = ((40,0),(0,0)),
    )
    
    return [
        [sg.Text("UNLPImage", key="-TITULO-", font=("Times New Roman", 20), justification="left")],

        [avatar_column],

        [sg.Column(layout=verMas, expand_x=True, element_justification="center")],

        [masBotones_column],
    ]

def run_inicio():
    # Crea la ventana
    window = sg.Window("", layout(), finalize=True, resizable=True)
    window.set_min_size((550, 400))#Tamaño minimo de la ventana
   
    # Bucle principal de eventos
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED :
            break

        elif event.startswith("-SELECCIONARIMAGEN-"):#Me fijo si tienen en comun la primeras palabras es porque selecciono una imagen determinada 
            print (event)
           # breakpoint()
            pos_imagen_seleccionada = (int(event.split("-")[-1]))-1  #Me quedo con la posicion de la imagen - 1 porque tenía una imagen que guarde de mas, entonces en el json siempre va a estar en una posicion menor  
            
            # Buscar el perfil correspondiente a la imagen seleccionada
            perfil_seleccionado = info[pos_imagen_seleccionada] 
            
            #Creo el usuario con los datos ingresaos y lo mando a menu principal 
            Usuario.alias = perfil_seleccionado["Nick"]
            Usuario.nombre = perfil_seleccionado["Nombre"]
            Usuario.edad = perfil_seleccionado["Edad"]
            Usuario.genero_autopercibido = perfil_seleccionado["Genero"]
            Usuario.url_avatar = perfil_seleccionado["Image"]
            print(Usuario.nombre)

            window.hide() #Escondo la ventana
            run_menu_princial(Usuario)
            window.close() #Muestro nuevamente la venata

        elif event == "-NUEVOPERFIL-":
           window.hide() #Escondo la ventana
           run_Perfil() # Abre la ventana de perfil
           window.un_hide() #Muestro nuevamente la venta 


        elif event == "-MOSTRARMAS-":
           # Actualizar la lista de botones de perfil para mostrar más nombres
           window["-MASPERFILES-"].update(visible=True)
           window["-MOSTRARMAS-"].update(visible=False)

    # Cierra la ventana
    window.close()

    