class ArbolCaracter:

    def __init__(self, cadena):
        self.caracateres = []

        for x in range(len(cadena)):
            self.caracateres.append(cadena[x])

    
    def getText(self):
        salida =""
        for x in range(len(self.caracateres)):
            salida += self.caracateres[x]
        return salida