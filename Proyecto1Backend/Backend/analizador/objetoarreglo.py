class bloqueArreglo:
    def __init__(self, arr = []):
        self.arreglo = arr

    def agregar(self,valor):
        return self.__agregar(valor,self.arreglo)
    
    def __agregar(self,valor,arreglo):
        return arreglo.append(valor)

    def existe(self, posiciones):
        return self.__exist(0, posiciones, self.arreglo)

    def __exist(self, indice, posiciones, arreglo):
        if indice < len(posiciones):
            index = posiciones[indice]
            if index < len(arreglo):
                if (index + 1) <= len(arreglo) and (indice + 1 ) == len(posiciones):
                     return True
                else:
                    return self.__exist(indice + 1, posiciones, arreglo[index])
            else:
                print("FUERA DE RANGO DENTRO DEL ARREGLO")
                print("SE BUSCA POSICION:", index, "EN",arreglo)
                return False
        else:
            print("FUERA DE RANGO")
            return False

    def obtener(self,lst_posiciones):
        return self.__get(0,lst_posiciones,self.arreglo)
    
    def __get(self,indice,posiciones,arreglo):
        if (indice + 1 ) == len(posiciones):
            return arreglo[posiciones[indice]]
        else:
            return self.__get(indice +1, posiciones, arreglo[posiciones[indice]])

    def actualizar(self,lst_posiciones,valor):
        print("SE VAN A ACTUALIZAR",valor)
        self.__update(0,lst_posiciones,valor,self.arreglo)
    
    def __update(self,indice,posiciones,valor,arreglo):
        if(indice + 1) == len(posiciones):
            arreglo[posiciones[indice]] = valor;
        else:
            return self.__update(indice + 1, posiciones, valor, arreglo[posiciones[indice]])

    def sacar(self):
        return self.__pop(self.arreglo)
    
    def __pop(self,arreglo):
        return arreglo.pop()
