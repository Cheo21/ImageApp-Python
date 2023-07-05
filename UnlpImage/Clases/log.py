import os
from datetime import datetime
import csv
# Nuevos paths agregados #
ruta_unlp = os.path.abspath(os.path.dirname(__file__))
print(ruta_unlp)
ruta_unlp = os.path.abspath(os.path.dirname(ruta_unlp))
print(ruta_unlp)


class Log:
    #Atributos
    nick : str
    operacion: str
    time: datetime.timestamp

    def __init__(self, nick, operacion, time):
        self.nick = nick
        self.operacion = operacion
        self.time = time  #antes era self = time y me decía que no tenía tiempo,yo interpreté que fue un error de sintaxis,y así me funciona así que no sé
    

def crear_csv(ruta: str, datos_log):
    """
    Esto crea el CSV si no existe,y le pone el encabezado
    me parece que no hace falta mandar valores o texto porque 
    el CSV se va a crear cuando se cree un nuevo perfil,básicamente
    la primera y única acción que podés hacer con el programa,y 
    valores y texto solo se usa para generar memes y collages
    """
    #print("A punto de entrar")
    with open(ruta, "w", newline='') as arch_log:
        writer_csv = csv.writer(arch_log)
        writer_csv.writerow(["time","Nick","ope","valores","text"])
    with open(ruta, "a",newline='') as arch_log:
        writer_csv = csv.writer(arch_log)
        writer_csv.writerow([datos_log.time, datos_log.nick, datos_log.operacion])

    """  with open(ruta, "r") as arch_log:
        reader_csv = csv.reader(arch_log)
        print("se va a imprimir el csv")
        print(next(reader_csv))
        print("saliendo") """ #Esto es de prueba,igual no quiere funcionar así que da lo mismo ._.


def añadir_nuevo_log(ruta: str, datos_log, valores, texto):
    with open(ruta, "a",newline='') as arch_log:
        writer_csv = csv.writer(arch_log)
        writer_csv.writerow([datos_log.time, datos_log.nick, datos_log.operacion,valores,texto]) #estos decían .fecha,después los cambié a .time y ahora es fecha devuelta

## Funcion que llama las demas
def añadir_log(nick, operacion, fecha, valores="", texto=""):  #agregué fecha como parámetro de entrada
    log = Log(nick, operacion, fecha)
    ruta_logs = os.path.join(ruta_unlp,"Assets","logs.csv")    #recorté un poco y agregué ruta_unlp
    print (ruta_logs)
    if os.path.exists(ruta_logs):
        añadir_nuevo_log(ruta_logs, log,valores,texto)
    else:
        crear_csv(ruta_logs,log)
