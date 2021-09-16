

import re


class bloqueStruct:
    def __init__(self, dicc = {}):
        self.diccionario = dicc

    def agregar(self,clave,objeto):
        self.add(clave,objeto,self.diccionario)

    def add(self,clave ,objeto, diccionario):
        if isinstance(diccionario,dict):
            if not clave in diccionario:
                diccionario[clave] = objeto
            else:
                diccionario[clave] = objeto

    def obtener(self,clave):
        return self.get(clave,self.diccionario)
    
    def get(self,clave, diccionario):
        if clave in diccionario:
            return diccionario[clave]
        else:
            return 1

    def existe(self,claves):
        return self.__exist(0, claves, self.diccionario)

    def __exist(self, indice, claves, diccionario):
        if (indice + 1) < len(claves):
            clave = claves[indice]
            print("@@@@@@@@@@@@@@@@@@@", clave)
            if clave in diccionario:
                return  self.__exist(indice + 1, claves, diccionario[clave])
            else:
                return False
        return True

    def get2(self,claves):
        return self.__get2(0, claves, self.diccionario)

    def __get2(self, indice, claves, diccionario):
        if (indice + 1) == len(claves):
            return diccionario[claves[indice]]
        else:
            return self.__get2(indice + 1, claves, diccionario[claves[indice]])