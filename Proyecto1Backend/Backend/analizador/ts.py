from enum import Enum

class Tipo(Enum):
    ENTERO = 1
    DECIMAL = 2
    STRING = 3
    CHAR = 4
    BOOL = 5
    NULO = 6
    INVALIDO = 9


class ref:
    def __init__(self, valor):
        self.val = valor

    def set(self, nuevo):
        self.val = nuevo

    def get(self):
        return self.val

    
   

class Simbolo:
    def __init__(self, *args):
        self.id = args[0]
        self.valor = ref(args[1])
        self.tipo = self.verficar(args[1],args[2])
        self.line = args[3]
        self.column = args[4]

    def verficar(self, valor, tipo):
        if tipo != None:
            return tipo
        else:
            if  isinstance(valor, int):
                return Tipo.ENTERO 
            elif isinstance(valor, float): 
                return Tipo.DECIMAL
            elif isinstance(valor, str): 
                 return Tipo.STRING
            elif valor == False:
                return Tipo.BOOL
            elif valor == True :
                return Tipo.BOOL
            elif valor == None :
                return Tipo.NULO
            else: 
                return Tipo.CHAR


class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}
        self.padre = None

    def agregar(self, simbolo):
        self.simbolos[simbolo.id] = simbolo

    def existe(self,id):
        return id in self.simbolos

    def setPadre(self, tabla):
        self.padre = tabla

    def getPadre(self):
        return self.padre

    def existepadre(self,tabla):
        return self.verificar(id,tabla)

    def verificar(self,id,tabla):
        if id in tabla.simbolos:
            return True
        if tabla.padre:
            return self.verificar(id,tabla.padre)
        return False
    
    def obtener(self,id,tabla):
        if id in tabla.simbolos:
                return tabla.simbolos[id]
        if tabla.padre: 
            return self.get(id,tabla.padre)
        return False

    def get(self, id, tabla):
        if id in tabla.simbolos:
            return tabla.simbolos[id].valor.get()
        if tabla.padre: 
            return self.get(id,tabla.padre)
        return False

    def actualizar(self, simbolo):
        self.simbolos[simbolo.id].valor.set(simbolo.valor.get())

    def referenciar(self,id,valor):
        self.simbolo[id].valor = valor