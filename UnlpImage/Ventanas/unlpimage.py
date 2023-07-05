#El programa pincipal esta dentro de ventanas, porque no pudimos importar inicio si este modulo estaba afuera, nos tiraba errores en las demas importaciones
#no pudimos solucionar el problema y lo dejamos aca 
#SE ABRE  DE LA CARPETA gurpo23
from .inicio import run_inicio

def run():
    run_inicio()