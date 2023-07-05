class Usuario:
    #Atributos
    alias = ""
    nombre =""
    edad = ""
    genero_autopercibido = ""
    url_avatar = ""

    #constructor
    def __init__(self, alias="", nombre="", edad="", genero_autopercibido="", url_avatar=""):
        self.alias = alias
        self.nombre = nombre
        self.edad = edad
        self.genero_autopercibido = genero_autopercibido
        self.url_avatar = url_avatar 