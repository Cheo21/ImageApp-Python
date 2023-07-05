import PySimpleGUI as sg
import json 
import os
from PIL import Image, ImageTk
#from controlador import ventanaI
from .menu_principal import run_menu_princial
from ..Clases.Usuario import Usuario
from datetime import datetime
from ..Clases.log import añadir_log as lg

ruta_image= os.path.join("UnlpImage","Image","Avatar_default.png") #Ruta de la imagen por defecto
ruta_arch = os.path.join("UnlpImage","Assets","info_perfil.json") #Ruta del json


C_SIZE = 15
T_SIZE = 10  

opcionesG = ["Femenino","Masculino"]#Opciones para la lista de generos

sg.theme("Purple")

sg.set_options(element_size=(30,1),font=("Times New Roman",T_SIZE)) #Tamaño y fuente predeterminada 


def layout():
    #Creo la parte de arriba, titulo y boton volver
    title =[
       [
          sg.Text(
             "Nuevo perfil",
             font=("Times New Roman",C_SIZE),
             justification="left"
          ),
          sg.Column(
            [[sg.Button("< volver",key="-VOLVER-")]],
            expand_x=True,
            element_justification="right"
          )
       ],   
    ] 
    
    #Creo todos los campos que el usuario va a tener que completar 
    lines = [
        [sg.Text("Nick o alias")],
        [sg.Input(size=(35,1),key="-ALIAS-")],

        [sg.Text("Nombre")],
        [sg.Input(size=(35,1),key="-NOMBRE-")],

        [sg.Text("Edad")],
        [sg.Input(size=(35,1),key="-EDAD-")],

        [sg.Text("Genero autopercibido")],
        [sg.Combo(opcionesG,default_value="Seleccione una opción",key='-GENERO-',expand_x=True,readonly=True)],

        [sg.Radio("Otro","GENERO",key= "-OTRO-", default= False,enable_events=True)],

        [sg.Input("Complete el género", key= "-NUEVOGENERO-",disabled=  True)],
    ]
    
    #
    avatares =[
        #Muestra la imagen que se selecciono, si no selecciona ninguna una por defecto, la configura, y le asigna una contraseña 
        [
            sg.Image(
                filename = ruta_image,
               # source = ruta_image,
                key  = "-AVATAR-",
                size = (280,280),
                subsample = 3,
                pad = ((100,100),(0,0))
            )
        ],    
        #Permite que el ususario ingrese una imagen de su propio directorio 
        [
            sg.FileBrowse(
                "Seleccionar imgen",
                key="-FOTO-",
                enable_events =True,
                change_submits = True,
                size=(20,2),
            ),
        ]
    ]
    #Crea lo anterios como columnas 
    columnas = [
        [
            sg.Column(lines),
            sg.Column(
                avatares,
                element_justification="Center",
                size=(450,400)
            )
        ]
    ]
    #boton guardar
    save=[
         [sg.Button("Guardar",key = "-GUARDAR-")]
    ]
     
    #Si no ingresa algun campo que es obligatorio se muestra el siguiente mensaje  
    column_error = [
         [sg.Text("",visible=False,key="-MENSAJE ERROR-",text_color="red", auto_size_text=True)]
    ]
    
    #retorno el layout 
    return [
        [sg.Column(layout=title,expand_x=True)],
        [ 
            sg.Column(
                layout = columnas,
                justification = "center",
                key="main-columnas",
                scrollable = True,
                vertical_scroll_only = True,
                expand_y=True,
                pad=((50,50),(50,50))
            )
       ],
       [sg.Column(layout=column_error, expand_x=True, element_justification="center")],
       [sg.Column(layout=save, expand_x=True, element_justification="right")],
       
    ]  
 

def run_Perfil():
    #Creo la ventana
    window = sg.Window("",layout(),finalize=True,resizable=True) 
    window.set_min_size((700, 620)) #Tamañano minimo de la ventana
    window["main-columnas"].vsb.pack_forget()#Esconde el scrool vertical
    seleccionado = 0 #Variable que utilizo para que se pueda seleccionar y deseccioanr OTROS
    while True:
        event,values = window.read()

        if event == sg.WIN_CLOSED or event == "-VOLVER-":
           break

        elif event == "-OTRO-":
            seleccionado +=1 #Si se activa otro se le suma uno a la variable 
            if seleccionado % 2 != 0: #si es impar es porque antes no estaba seleccionado, porque la cuenta empiza de 0
                window["-NUEVOGENERO-"].Update("",disabled=False)
                values["-GENERO-"] = values["-NUEVOGENERO-"]
            else: # si es par quiere decir que estaba seleccioado y hay que deseleccionarlo 
                window["-NUEVOGENERO-"].Update("Complete el genero",disabled=True)
                window["-OTRO-"].Update(False)

        elif event == "-FOTO-":
            filename = values["-FOTO-"] #Recupero la ruta de la imagen 
            try:
                #Abro el archivo de la imaen 
                with Image.open(filename) as img:
                    #Redimensiono la imagen 
                    img.thumbnail((280, 280), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(img)
                    
                    #Se actualiza -AVATAR- para que muestre la imagen que se selcciono 
                    window["-AVATAR-"].update(
                        data = photo,
                        size = (280,280),
                        subsample = 3
                    ) 
            except OSError as e:
                #Si selecciona cualquier otra cosa que no sea algo que se identifique como imagen o gif
                window["-MENSAJE ERROR-"].update("No se pudo cargar la imagen seleccionada. Por favor seleccione una imagen válida para su avatar.", visible=True)

        elif event == "-GUARDAR-":
            
           # breakpoint()
            
            #print(termina)
           # breakpoint()

            #Si no selecciono ninguna foto o selccione algo que no es foto guardo en el valor "-FOTO-" la imagen por defecto que se encuentra en ruta_image
            termina = (values["-FOTO-"].split(".")[-1])
            if values['-FOTO-']=="" or not termina in ("jpg", "png","gif"):
                values['-FOTO-']= ruta_image

            #breakpoint()

            #Chequeo que haya seleccionado todos los datos obligatorio 
            if values["-ALIAS-"] and values["-NOMBRE-"] and values["-EDAD-"].isnumeric() and ((values["-GENERO-"] != "Seleccione una opción") or (values["-OTRO-"] == True)):
                #Abro el json
                try:
                    archivo = open(ruta_arch, 'r+', encoding="UTF-8")
                    #Pongo en lista_perfil todos los perfiles que tengo hasta el momento
                    try:
                       #Intento cargar el contenido del archivo
                       lista_perfil = json.load(archivo)
                    except json.JSONDecodeError:
                       # Si no puedo, es porque el archivo está vacío y creo una lista vacía
                       lista_perfil = []  # Lista vacía si el archivo está vacío o no se puede decodificar como JSON
                #si no exite 
                except FileNotFoundError:
                    lista_perfil = []  # Lista vacía si el archivo no existe
                    archivo = open(ruta_arch, 'w', encoding="UTF-8")
                          # lo creo ya abro para guardar datos

                # breakpoint()
                        
                #Chequeo que el nick no exista
                if any(perfil["Nick"] == values["-ALIAS-"] for perfil in lista_perfil):
                    window["-MENSAJE ERROR-"].update("EL NICK YA EXISTE. POR FAVOR, ELIJA OTRO NICK.", visible=True)
                    values["-ALIAS-"] = " "# Establecer el valor del nick como una cadena vacía
                else:    
                    # Verifico si el género seleccionado es 'Otro'
                    if (values["-OTRO-"] == True):
                        genero = values["-NUEVOGENERO-"]#Si esta seleccionado modifico el valor de genero para que sea el genero que ingreso el usuario 
                    else:
                        genero = values["-GENERO-"]    

                    #Creo el nuevo reistro
                    nuevo_perfil = {"Nick":values["-ALIAS-"],"Nombre":values["-NOMBRE-"],"Edad":values["-EDAD-"],"Genero":genero,"Image":values["-FOTO-"]}

                    #Lo agrego a la lista
                    lista_perfil.append(nuevo_perfil)
                
                    #Muevo el puntero al principio
                    archivo.seek(0)

                    #Cargo la lista en el archivo
                    json.dump(lista_perfil, archivo, indent=4)
                    archivo.close() # Cierro el archivo
                    
                    #Creo Usuario con el perfil que estoy cargando 
                    Usuario.alias= values["-ALIAS-"]
                    Usuario.nombre = values["-NOMBRE-"]
                    Usuario.edad = values["-EDAD-"]
                    Usuario.genero_autopercibido = genero
                    Usuario.url_avatar = values["-FOTO-"]
                    #Cierro la ventana porque Menu prncipal no guarda un usuario 
                    timestamp = datetime.timestamp(datetime.now())
                    fecha = int(timestamp)
                    lg(values['-ALIAS-'],'new_profile',fecha)
                
                    window.close()
                    run_menu_princial(Usuario) #Voy a menu principal
                #si no ingresa una edad validad es decir todos numeros le muestro un mensaje error
            elif not values["-EDAD-"].isnumeric() and values["-EDAD-"]:
                window["-MENSAJE ERROR-"].update("INGRESE UNA EDAD VALIDAD.", visible=True)
            else: 
                 #Si no los completo le avisa con un mensaje en pantalla 
                 
                 window["-MENSAJE ERROR-"].Update(value="COMPLETE LOS CAMPOS OBLIGATRIOS",visible=True)
    window.close()    
