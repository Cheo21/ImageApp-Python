import ast
import io
import os
import PySimpleGUI as sg
from PIL import Image
import csv
from datetime import datetime
from ..Clases.Usuario import Usuario as User
from ..Clases.log import añadir_log as AL

#imports vitales para q funque
#En la línea 249 aprox está el thumbnail,podés cambiar libremente el número por si la imágen es muy grande o muy chica👍
path_absoluto = os.path.abspath(os.path.dirname(__file__))
#print(path_absoluto)
path_absoluto = os.path.abspath(os.path.dirname(path_absoluto))
#print(path_absoluto)
path_absoluto = os.path.join(path_absoluto,"Assets") #Esto termina con el path en Assets,carpeta donde están los CSV,entre otras cosas
#print(path_absoluto)  #No sé si path absoluto es un buen nombre,es el path hasta Assets,donde están los csv
#path_completo = os.path.join(path_absoluto, path_superrelativo)

def modificar_tags (elim,ruta):
    """
    Esta función modifica los tags de la ruta que le das. Lo que hace es tratar de eliminar la posición que le das (los parámetros que recibe)
    """
    with open(os.path.join(path_absoluto,'metadata.csv'), 'r+', newline='',encoding="UTF-8") as archivo_csv:   
                lector_csv = csv.reader(archivo_csv)
                contenido_csv = list(lector_csv)
                for i, sublist in enumerate(contenido_csv): 
                    if ruta in sublist:                  
                        posicion = i
                        datos_imagen_original = sublist  
                        break
                tags = datos_imagen_original[7]
                elementos = tags.split(',')
                #print("print de prueba lista")
                #print(tags_lista)
                if elim < len(elementos):
                    elementos.pop(elim)  # Eliminar el elemento en la posición indicada
                else:
                    sg.popup('Está intentando eliminar una posición inválida')
                elementos2=",".join(elementos)
                tags_actualizado = elementos2 
                #print("print de prueba2 tags lista actualizada")
                #print(tags_actualizado)
                datos_imagen_original[7] = tags_actualizado
                contenido_csv[posicion] = datos_imagen_original

                archivo_csv.seek(0)  # Regresar al inicio del archivo
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerows(contenido_csv)
                archivo_csv.truncate()  # Truncar el archivo para eliminar el contenido adicional si es necesario


def agarrar_Tags(ruta):
    """
    Esta función agarra los tags de la imágen desde el CSV y los devuelve en una variable
    """
    with open(os.path.join(path_absoluto,'metadata.csv'), 'r+', newline='',encoding="UTF-8") as archivo_csv:   #una copia de mi módulo que buscaba
        lector_csv = csv.reader(archivo_csv)                                                                   #la imagen en el csv y leía lo que tenía
        contenido_csv = list(lector_csv)                                                                       #bueno,ahora parecido,solo que lo guardo en una variable
        for i, sublist in enumerate(contenido_csv): 
            if ruta in sublist:                  
                posicion = i
                datos_imagen_original = sublist  
                break
        tags_str = datos_imagen_original[7]#Sacado de chatGPT,por fin me tiró una buena...
        print(f"se va a imprimir tags_str: {tags_str}") #y es algo básico que viene incluído en python
    return tags_str

def path_csv():
    """
    Esta función lee lo que tiene el CSV en la primera línea,para saber cual es el directorio de imágenes
    """
    with open (os.path.join(path_absoluto,'configuracionCSV.csv'), 'r' ,newline='',encoding="UTF-8") as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        contenido_csv = list(lector_csv)
        route = contenido_csv[1][0]
        print('ruta:')
        print(route)
    return route 

def obtener_fecha():
    """
    Obtiene la fecha del instante en el que se ejecuta,para guardar
    la última modificación en el csv
    """
    timestamp = datetime.timestamp(datetime.now())
    fecha = int(timestamp)
    return fecha

"""
            path_csv = os.path.join(path_absoluto, "metadata.csv") Esto antes existía,pero después de 
            revisar como van a evaluar el programa,traté de reducir la cantidad de variables globales 
            todo lo posible. Estos eran prints de prueba para testear
            print('absoluto') print(path_absoluto) print('relativo') print(path_relativo)         
            print('completo') print(path_completo) print('pathcsv')  print(path_csv)                                    
"""       
        
def buscar_imagen(ruta):
    """
    Esta función abre el archivo metadata,en modo lectura
    lo pasamos a una lista y usamos el mágico comando que
    le copie a la profe donde la lista es ennumerada, y 
    creamos una sublista que tiene los contenidos de los
    renglones que estamos leyendo. Básicamente obtuvimos
    el archivo en una lista. Conseguimos la línea que 
    queríamos leer,la transformamos en una lista,y de 
    ahí sacamos manualmente cada metadato
    """
    
    with open(os.path.join(path_absoluto,'metadata.csv'), 'r', newline='',encoding="UTF-8") as archivo_csv: 
        datos_imagen_original = None    #Esto es un parche que cubre un caso que por algún motivo no debería pasar,pero puede pasar(?)
        lector_csv = csv.reader(archivo_csv)
        contenido_csv = list(lector_csv)
        for i, sublist in enumerate(contenido_csv):  
            if ruta in sublist:                  
                datos_imagen_original = sublist
                break
        if datos_imagen_original:
            res = str(datos_imagen_original[4])+ "x" + str(datos_imagen_original[3])
            size = datos_imagen_original[5]
            mimetype = datos_imagen_original[6]
            descrip = datos_imagen_original[8]
            etiqs = datos_imagen_original[7]
        else:
            res = ''
            size = ''
            mimetype = ''
            descrip = ''
            etiqs = []

        return res,size,mimetype,descrip,etiqs
  

def actualizar_archivo(ruta,desc,res,size,type,tags,fecha,User):
    """
    Esta función recibe de parámetros la metadata,que previamente
    se obtuvo de el csv con la función "buscar_imagen".

    Abre el archivo de modo lectura,lo pasamos a una lista
    y usamos el mágico comando que le copie a la profe donde
    la lista es ennumerada,y creamos una sublista que tiene
    los contenidos de los renglones que estamos leyendo
    terminamos el bucle con la lista a modificar (posicion)
    y una lista de sus contenidos,para cambiar cada uno manualmente.

    Luego,escribe nomás
    """

    with open(os.path.join(path_absoluto,'metadata.csv'), 'r+', newline='',encoding="UTF-8") as archivo_csv:   
        lector_csv = csv.reader(archivo_csv)
        contenido_csv = list(lector_csv)
        for i, sublist in enumerate(contenido_csv): 
            if ruta in sublist:                  
                posicion = i
                datos_imagen_original = sublist  
                break
        datos_imagen_original[8] = desc
        datos_imagen_original[7] = tags
        datos_imagen_original[0] = fecha
        datos_imagen_original[1] = User
        contenido_csv[posicion]=datos_imagen_original
    with open(os.path.join(path_absoluto,'metadata.csv'), 'w',newline='',encoding="UTF-8") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerows(contenido_csv)     


def existe_imagen(img):   
    """
    Esta función une el path absoluto,con el nombre del
    archivo (metadata) y revisa si existe la imagen ese lugar.
    
    Tiene una excepción para la primera vez que se ejecuta el programa
    (cuando no debería haber un archivo,y habría error).Ahí crea el archivo
    y le da unos encabezados para la primera línea.
    """
    b=False
    try:
        with open(os.path.join(path_absoluto, "metadata.csv"), 'r+',encoding="UTF-8") as arch:    
            reader = csv.reader(arch)
            for linea in reader:
                if linea[2] == img:  #Si lo que está en la línea 0 (La ruta) coincide con la ruta de la imagen
                    #print("EXISTE")
                    b=True
            #if not b:
                #print("NO EXISTE")
    except FileNotFoundError:           
            print('No existe el archivo csv')
            with open(os.path.join(path_absoluto, "metadata.csv"), 'w+', newline='',encoding="UTF-8") as archivo: 
                escritor = csv.writer(archivo)
                escritor.writerow(['time','Nick','imagen','alto','ancho','tamaño','tipo','tags','des'])
    finally:
        print("se va a imprimir b") #esto para probar/debuggear
        print(b)
        return b
"""
Esta función daba error la primera vez siempre,porque iba a querer revisar el csv que no existía
Por lo que entendí,tenemos que permitir que el programa cree el csv si no existe,por eso usé w+ en la otra función
Entonces esto cubre el primer caso,de la primera imágen,donde no existe csv que revisar :)
"""

def guardar_nueva_imagen(path,desc,res,size,type,tags,fecha,User):
    """
    Esta función recibe de parámetros la metadata sacada de la imágen,
    y los junta en una variable "todojunto" para más cómodidad
    Recordar que esta es una función para agregar una imagen que no estaba 
    previamente en el archivo,por lo que se usa append
    """
    resolucion = res
    width,height = map(int,resolucion.split("x"))
    todojunto = [fecha,User,path,height,width,size,type,tags,desc]
    
    with open(os.path.join(path_absoluto, "metadata.csv"),'a',newline='',encoding="UTF-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(todojunto)

def encontrar_ruta(filename):
    """
    Esta función junta los paths para 
    conseguir la carpeta de la imágen leída,
    más el nombre de la imágen
    """
    path_de_la_imagen=os.path.basename(filename) #Obtengo el nombre del archivo solo,separado
    carpeta_contenedora = os.path.dirname(filename) #Obtengo la ruta de la carpeta que contiene el archivo
    print('contenedora')
    print(carpeta_contenedora)
    nombre_carpeta = os.path.basename(carpeta_contenedora) #Obtengo el nombre de la carpeta
    print('nombrecarpeta')
    print(nombre_carpeta)
    nombre_assets = os.path.dirname(carpeta_contenedora)
    print('nombre_assets')
    print(nombre_assets)
    nombre_assets = os.path.basename(nombre_assets)
    print('nombre_assets')
    print(nombre_assets)
    path_a_mostrar=os.path.join(nombre_assets,nombre_carpeta,path_de_la_imagen) #Los junto a ambos para tener carpeta + archivo
    ruta = path_a_mostrar #Variable a devolver
    return ruta



def layout():
    """
    No creo que haga falta explicar lo que hace esta función,simplemente es un layout,un poco feo,pero es lo que hay
    """
    if os.path.exists(os.path.join(path_absoluto,'configuracionCSV.csv')):
        csv = path_csv()
    else:
        csv = ''
    title = [[sg.Text('Etiquetar imágenes', font=("Helvetica", 18), justification="left"), sg.Push(), sg.Button('Volver',key='-SALIR-', font= ("Helvetica", 18))]]

    layout = [[sg.Text("Seleccione la imágen")],
              [sg.Input(size=(25, 1), key="-IMAGEN-"),sg.FileBrowse('Seleccionar',initial_folder=csv),sg.Button('Aceptar')], #si no le ponía un botón para "aceptar procesar la imagen"
              [sg.Image(key='-IMAGE-', size=(200,200),data='')]]  # imagen vacía                          #no había chance que me lo detecte como un evento,para poder
            # Nueva sección para mostrar la metadata,se llama layout2 porque soy muy original                                                                                          #actualizar la imágen más adelante,quizá es tosco,pero funca
    layout2 = [[sg.Text("Información de la imagen:",key="-info-de-la-img-",visible=False)], 
              [sg.Text("Nombre:",key="-nom-",visible=False), sg.Text(size=(20,1), key='-NOMBRE-DEL-ARCHIVO-',visible=False)],
              [sg.Text("Ruta:",key="-path-",visible=False), sg.Text(size=(20,1), key='-PATH-DEL-ARCHIVO-',visible=False)],
              [sg.Text("Tamaño:",key="-size-",visible=False), sg.Text(size=(20,1), key='-TAMAÑO-',visible=False)],
              [sg.Text("Resolución:",key="-res-",visible=False), sg.Text(size=(20,1), key='-RESOLUCION-',visible=False)],
              [sg.Text("Tipo:",key="-type-",visible=False), sg.Text(size=(20,1), key='-MIMETYPE-',visible=False)],

              [sg.Text("Tags:",key="-etiquetas-",visible=False), sg.Text(size=(35,1), key='-ETIQUETAS-',visible=False)],
              [sg.Text("Ingrese posición a eliminar(Arranca en 0)",key="-elim_tags-",visible=False)],
              [sg.Input(size=(5, 1), key="-ELIM_TAGS-",visible=False),sg.Button('Aceptar',key="Acep3",visible=False)],

              [sg.Text("Ingrese etiquetas(Agregar nuevos tags de uno a la vez)",key="-tags-",visible=False)],
              [sg.Input(size=(35, 1), key="-TAGS-",visible=False),sg.Button('Aceptar',key="Acep1",visible=False)],
              

              [sg.Text("Desc:",key="-Descrip-",visible=False), sg.Text(size=(35,1), key='-descrip-',visible=False)],
              [sg.Text("Ingrese descripción",key="-desc-",visible=False)],
              [sg.Input(size=(35, 1), key="-DESC-",visible=False),sg.Button('Aceptar',key="Acep2",visible=False)],
              
              ]                                                                                               
    subtitle = [[sg.Text(''), sg.Push(),sg.VPush()], #De esta manera guardar queda abajo a la derecha como yo lo quiero     
                [sg.Push(),sg.Button('Guardar',key='-GUARDAR-',font=("Helvetica",16))]]    
                #Este uso de los layouts está copiado de mi ventana anterior igual(configuración)
    return [[title],
            [sg.Column(layout,justification="center")], 
            [sg.Column(layout2,justification="center")],#esto está hecho una columna
            [subtitle]]
            
def run():
    """
    Literalmente es todo el programa,con el bucle principal
    """

    window = sg.Window('Configurar Etiquetas', layout(),finalize=True, resizable=True)    
    window.set_min_size((600,400))         

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == '-SALIR-':
            break
        if event == 'Aceptar':
            filename=values['-IMAGEN-'] #creo una variable que va a tener los valores(el directorio de la imagen)
            try:    
                if not os.path.exists(filename):#si no existe en el directorio este archivo que queremos abrir:
                    raise ValueError(f'El archivo "{filename}" no existe')  
                if os.path.splitext(filename)[1] not in ('.png', '.jpg', '.jpeg'): # esto separa el path de la extensión
                    raise ValueError('Debe seleccionar un archivo de imagen válido (PNG/JPG/JPEG') 
                                                                                         
                image = Image.open(values["-IMAGEN-"]) #la variable imagen va a abrir la imagen,con el tamaño del thumbnail
                image.thumbnail((150, 150))            #que si entendí bien,lo que hace thumbnail es mantener la relacion de aspecto
                bio = io.BytesIO()   #se guardan los bytes de la imagen
                image.save(bio, format="PNG")    #esto complementa la instrucción anterior. Me acabo de dar cuenta que transforma la imágen a png,aunque solo para mostrarla
                window["-IMAGE-"].update(data=bio.getvalue()) #y le pasamos la data a la ventana imagen para que se actualize con estos bytes
                                                              #mostrando así,la imágen
                ruta = encontrar_ruta(filename) #Si no extraigo la ruta de la imagen misma,no tengo forma de buscarlo en el csv
                existe = existe_imagen(ruta)  #Reviso si la imágen está en el csv
                print(existe)
                #Hacer aparecer los strings invisibles que van a dar la info de la imagen
                window["-info-de-la-img-"].update(visible=True), window["-nom-"].update(visible=True)
                window["-path-"].update(visible=True), window["-size-"].update(visible=True)
                window["-res-"].update(visible=True), window["-type-"].update(visible=True)
                window["-tags-"].update(visible=True), window["-TAGS-"].update(visible=True)
                window["Acep1"].update(visible=True), window["-desc-"].update(visible=True)
                window["-DESC-"].update(visible=True), window["Acep2"].update(visible=True)
                window["-etiquetas-"].update(visible=True), window["-Descrip-"].update(visible=True)
                if not existe: 
                    #print("No existe")
                    """
                    Si la imagen no existe en el csv,la mostramos de esta manera,extrayendo los metadatos de la imágen directamente.
                    Estas variables son para hacer lo de abajo,actualizar la info de los objetos de texto del layout.
                    """
                    res = str(image.width) + 'x' + str(image.height)
                    size = f"{round(os.path.getsize(filename)/1024, 1)}KB"
                    mimetype = image.format_description
                    descrip = "No tiene"
                    etiqs = "No tiene"
                    
                    """
                    Tenía entendido que las variables de acá arriba,yo podía simplemente asignarle el valor de las etiquetas que están aca abajo,pero cuando
                    lo hice,siempre tiraban keyerror o algún otro error,no entendí por qué,tengo entendido que puedo asignarle a una variable "values['etiqueta']"
                    y de hecho está hecho más arriba para la imágen,pero acá no quiso funcionar así que lo hice variables aparte nomás
                    """
                    #Actualizar la información de la imagen 
                    window["-descrip-"].update(value=descrip,visible=True),window["-TAMAÑO-"].update(value=size, visible=True)
                    window["-ETIQUETAS-"].update(value=etiqs,visible=True),window["-RESOLUCION-"].update(value=res,visible=True)
                    window["-NOMBRE-DEL-ARCHIVO-"].update(value=os.path.basename(filename),visible=True),window["-PATH-DEL-ARCHIVO-"].update(value=ruta,visible=True)
                    window["-MIMETYPE-"].update(value=mimetype,visible=True)     
                    """
                    Todos estos comandos los saqué de internet,es para conseguir la info exif;
                    Si no hacía a todos los objetos invisibles,y después los hacía visibles devuelta
                    Los objetos que no hubiera cambiado,hubieran cambiado de lugar con los otros. 
                    Parece que la visibilidad de los objetos está vinculada al "espacio" que ocupan en la gui
                    Osea,la visibilidad no es una característica aislada,más bien desaparece al objeto totalmente
                    Así que hice invisible todo hasta que no hiciera falta,un quilombo lo admito
                    """
                else:
                    #print("Existe")
                    res,size,mimetype,descrip,etiqs = buscar_imagen(ruta)
                    print(res),print(size),print(mimetype),print(descrip),print(etiqs)
    
                    window["-descrip-"].update(value=descrip,visible=True),window["-TAMAÑO-"].update(value=size, visible=True)
                    window["-ETIQUETAS-"].update(value=etiqs,visible=True),window["-RESOLUCION-"].update(value=res,visible=True)
                    window["-NOMBRE-DEL-ARCHIVO-"].update(value=os.path.basename(filename),visible=True),window["-PATH-DEL-ARCHIVO-"].update(value=ruta,visible=True)
                    window["-MIMETYPE-"].update(value=mimetype,visible=True) ,window["-elim_tags-"].update(visible=True) 
                    window["-ELIM_TAGS-"].update(visible=True) ,window["Acep3"].update(visible=True)
            except ValueError as e:
                sg.popup_error(str(e)) #Esto transforma en string el parámetro e,que es una variable que  almacena 
                                       #información sobre la excepción, como su tipo y un mensaje de error asociado.
        if event == 'Acep3':
            elim = int(values["-ELIM_TAGS-"])
            
            modificar_tags(elim,ruta)

            res,size,mimetype,descrip,etiqs = buscar_imagen(ruta)
            window["-ETIQUETAS-"].update(value=etiqs,visible=True) 
        if event == 'Acep1':
            tag = values["-TAGS-"]
        if event == 'Acep2':
            desc = values["-DESC-"]
        if event == '-GUARDAR-':

            existe = existe_imagen(ruta) #Si no repito este chequeo acá,podrías agregar por error 
            fecha = obtener_fecha() #múltiples veces una imágen la primera vez que la ingreses
            try:      
                if not existe:  
                    tags=""   #Se crea una lista vacía,y se le append-ea el tag recién leído
                    tags="".join(tag)
                    print(f"se va a imprimir {tags}")
                    print("guardar_nueva_imagen")
                    guardar_nueva_imagen(ruta,desc,res,size,mimetype,tags,fecha,User.alias)
                    AL(User.alias,'new_image',fecha)
                    #Una vez guardado,vamos a buscar denuevo la data de la imagen al CSV,ahora tiene que estar si o sí,y actualizamos descripción y etiquetas :)
                    res,size,mimetype,descrip,etiqs = buscar_imagen(ruta)
                    window["-descrip-"].update(value=descrip,visible=True)
                    window["-ETIQUETAS-"].update(value=etiqs,visible=True)  
                    window["-elim_tags-"].update(visible=True) 
                    window["-ELIM_TAGS-"].update(visible=True) ,window["Acep3"].update(visible=True)
                else:
                    #print(f"se va a imprimir el tag a agregar {tag}")
                    tags=agarrar_Tags(ruta) #Esto agarra los tags
                    #print(f"se va a imprimir agarrar tags {tags}")
                    if tags:
                        tags+=f",{tag}" #Y esto los agrega,total es una cadena de string
                    else:
                        tags+=tag
                    #print(f"se va a imprimir tags {tags}")
                    print("actualizar_archivo")
                    actualizar_archivo(ruta,desc,res,size,mimetype,tags,fecha,User.alias)
                    AL(User.alias,'edit_image',fecha)
                    #lo mismo que arriba
                    res,size,mimetype,descrip,etiqs = buscar_imagen(ruta)
                    window["-descrip-"].update(value=descrip,visible=True)
                    window["-ETIQUETAS-"].update(value=etiqs,visible=True) 
                sg.popup('¡Imágen guardada correctamente!')
            except UnboundLocalError as e:
                sg.popup('No ingreso tags o descripción')
            


    window.close()
