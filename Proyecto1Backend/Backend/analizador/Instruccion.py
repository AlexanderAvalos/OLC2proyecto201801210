
import expresiones as exp
from ts import Tipo

#intrucciones
class Instruccion:
    'Clase definida para usar como interfaz'
#isntrucciones basicas
class Declaracion(Instruccion):
    def __init__(self,id, valor,tipo, linea,columna):
        self.id = id
        self.valor = valor 
        self.columna = columna
        self.tipo = tipo
        self.linea = linea
        super().__init__()

class OperacionLlamada(Instruccion):
    def __init__(self,id,parametros):
        self.id = id 
        self.parametros = parametros
        super().__init__()

class PrintComp(Instruccion):
    def __init__(self,tipo,cadena,argumentos,line):
        self.tipo = tipo
        self.cadena = cadena 
        self.argumentos = argumentos
        self.line = line
        super().__init__()

class PrintCadena(Instruccion):
    def __init__(self,tipo,cadena,line):
        self.tipo = tipo
        self.cadena = cadena 
        self.line = line
        super().__init__()

class Printval(Instruccion):
    def __init__(self,tipo,val,line):
        self.tipo = tipo
        self.val = val 
        self.line = line
        super().__init__()        

#llamada

class llamada(Instruccion): 
    def __init__(self, idfuncion, parametros, linea):
        self.idfuncion = idfuncion
        self.parametros = parametros
        self.linea = linea 
        super().__init__()
#funciones

class Funcion(Instruccion):
    def __init__(self,idFuncion,parametros, sentencias,linea):
        self.idFuncion = idFuncion
        self.parametros = parametros
        self.sentencias = sentencias 
        self.linea = linea 
        super().__init__()

class Parametros(Instruccion):
    def __init__(self, idparametro, tipo, linea,columna):
        self.idparametro = idparametro
        self.tipo = tipo
        self.linea = linea 
        self.columna = columna
        super().__init__()

#sentencias 
class SentenciaReturn(Instruccion):
    def __init__(self,operacion,linea):
        self.operacion = operacion
        self.linea = linea 
        super().__init__()

class SentenciaBreak(Instruccion):
    def __init__(self,line):
        self.line = line
        super().__init__()

class SentenciaContinue(Instruccion):
    def __init__(self,line):
        self.line = line
        super().__init__()

#if
class If(Instruccion):
    def __init__(self, s_if, s_elif, s_else, linea):
        self.s_if = s_if
        self.s_elif = s_elif
        self.s_else = s_else
        self.linea = linea
        super().__init__()

class SentenciaIf(Instruccion):
    def __init__(self,condicion, sentencias, linea):
        self.condicion = condicion
        self.sentencias = sentencias
        self.linea = linea
        super().__init__()

#while
class While(Instruccion):
    def __init__(self, condicion, sentencias, linea):
        self.condicion = condicion
        self.sentencias = sentencias
        self.linea = linea
        super().__init__()

#for
class For(Instruccion):
    def __init__(self,id, condicional, sentencias, linea):
        self.id = id
        self.condicional = condicional
        self.sentencias = sentencias
        self.linea = linea 
        super().__init__()

class condicionalSimple(Instruccion):
    def __init__(self,operacion,linea):
        self.operacion = operacion
        self.linea = linea
        super().__init__()

class condicionalRango(Instruccion):
    def __init__(self, rangoizq, rangoder, linea ):
        self.rangoizq = rangoizq
        self.rangoder = rangoder 
        self.liena = linea 
        super().__init__()

#operaciones 
#valores
class OperacionNumero(Instruccion):
    def __init__(self,num, line, columna) :
        self.num = num
        self.line = line 
        self.columna = columna
        super().__init__()

class OperacionVariable(Instruccion):
    def __init__(self,id,linea,columna):
        self.id = id
        self.linea = linea 
        self.columna = columna
        super().__init__()

class OperacionCaracter(Instruccion):
    def __init__(self, car, linea,columna):
        self.car = car
        self.linea = linea 
        self.columna = columna
        super().__init__()

class OperacionCadena(Instruccion):
    def __init__(self,cadena,linea,columna):
        self.cadena = cadena
        self.linea = linea 
        self.columna = columna
        super().__init__()

class OperacionBooleana(Instruccion):
    def __init__(self, val, linea , columna):
        self.val = val
        self.linea = linea 
        self.columna = columna
        super().__init__()


#numerica
class OperacionNumerica(Instruccion):
    def __init__(self,opIzq,opDer,operacion,line,columna):
        self.opIzq = opIzq
        self.opDer = opDer
        self.operacion = self.verficarNum(operacion)
        self.line = line
        self.columna = columna
        super().__init__()

    def verficarNum(self,operacion):
        if operacion == '+':
            return exp.OPERACION_NUMERICA.SUMA
        elif  operacion == '-':
            return exp.OPERACION_NUMERICA.RESTA
        elif  operacion == '*':
            return exp.OPERACION_NUMERICA.MULTIPLICACION
        elif  operacion == '/':
            return exp.OPERACION_NUMERICA.DIVISION
        elif  operacion == '%':
            return exp.OPERACION_NUMERICA.MODULAR
        elif  operacion == '^':
            return exp.OPERACION_NUMERICA.POTENCIA    
        else:
            print('error')

#relacional
class OperacionRelacional(Instruccion):
    def __init__(self,opIzq,opDer,operacion,line,columna):
        self.opIzq = opIzq
        self.opDer = opDer
        self.operacion = self.verficarRelacional(operacion)
        self.line = line
        self.columna = columna
        super().__init__()
    
    def verficarRelacional(self,operacion):
        if operacion == '==':
            return exp.OPERACION_RELACIONAL.IGUAL
        elif  operacion == '>':
            return exp.OPERACION_RELACIONAL.MAYOR
        elif  operacion == '<':
            return exp.OPERACION_RELACIONAL.MENOR
        elif  operacion == '<=':
            return exp.OPERACION_RELACIONAL.MENORQUE
        elif  operacion == '>=':
            return exp.OPERACION_RELACIONAL.MAYORQUE
        elif  operacion == '!=':
            return exp.OPERACION_RELACIONAL.DIFERENTE
        else:
            print('error')

#logica
class OperacionLogica(Instruccion):
    def __init__(self,opIzq,opDer,operacion,line,columna):
        self.opIzq = opIzq
        self.opDer = opDer
        self.operacion = self.verficarLog(operacion)
        self.line = line
        self.columna = columna
        super().__init__()
    
    def verficarLog(self,operacion):
        if operacion == '&&':
            return exp.OPERACION_LOGICA.AND
        elif  operacion == '||':
            return exp.OPERACION_LOGICA.OR
        else:
            print('error')

#operaciones aparte 
class OperacionBinaria(Instruccion):
    def __init__(self,opIzq,opDer,operacion,line,columna):
        self.opIzq = opIzq
        self.opDer = opDer
        self.operacion = operacion
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionUnaria(Instruccion):
    def __init__(self,op1,operacion,line,columna):
        self.op1 = op1
        self.operacion = self.verficarUni(operacion)
        self.line = line
        self.columna = columna
        super().__init__()

    def verficarUni(self,operacion):
        if operacion == '!':
            return exp.OPERACION_LOGICA.NOT
        elif  operacion == '-':
            return exp.OPERACION_NUMERICA.RESTA

class OperacionSen(Instruccion):
    def __init__(self, operador,line,columna):
        self.operador = operador
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionCos(Instruccion):
    def __init__(self, operador,line,columna):
        self.operador = operador
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionTan(Instruccion):
    def __init__(self, operador,line,columna):
        self.operador = operador
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionLog10(Instruccion):
    def __init__(self, operador,line,columna):
        self.operador = operador
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionLog(Instruccion):
    def __init__(self, operador,operador2,line,columna):
        self.operador = operador
        self.operador2 = operador2
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionSQRT(Instruccion):
    def __init__(self, operador,line,columna):
        self.operador = operador
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionLOWER(Instruccion):
    def __init__(self, operador,line,columna):
        self.operador = operador
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionUPPER(Instruccion):
    def __init__(self, operador,line,columna):
        self.operador = operador
        self.line = line
        self.columna = columna
        super().__init__()
    
class OperacionLenght(Instruccion):
    def __init__(self, operador,line,columna):
        self.operador = operador
        self.line = line
        self.columna = columna
        super().__init__()

class OperacionParse(Instruccion):
    def __init__(self, tipo, valor, linea):
        self.tipo = self.verficartipo(tipo)
        self.valor = valor
        self.linea = linea
        super().__init__()

    def verficartipo(self,tipo):
        if tipo.lower() == "int64":
            return Tipo.ENTERO
        elif tipo.lower() == "float64":
            return Tipo.DECIMAL
        else:
            print("tipo invalido")
            return Tipo.INVALIDO

class OperacionTrunc(Instruccion):
    def __init__(self, valor, linea):
        self.valor = valor
        self.linea = linea
        super().__init__()


class OperacionFloat(Instruccion):
    def __init__(self,  valor,linea):
        self.valor = valor
        self.linea = linea
        super().__init__()

class OperacionString(Instruccion):
    def __init__(self,valor,linea):
        self.valor = valor
        self.linea = linea
        super().__init__()

class OperacionTypeof(Instruccion):
    def __init__(self,valor,linea):
        self.valor = valor
        self.linea = linea
        super().__init__()

#arreglos
class OperacionPush(Instruccion):
    def __init__(self,valor,linea):
        self.valor = valor
        self.linea = linea
        super().__init__()

class OperacionPop(Instruccion):
    def __init__(self,valor,linea):
        self.valor = valor
        self.linea = linea
        super().__init__()

#structs

class StructsMutable(Instruccion):
    def __init__(self, objeto, listaAtributos, linea, columna):
        self.objeto = objeto
        self.listaAtributos = listaAtributos
        self.linea = linea
        self.columna = columna
        super().__init__()

class StructsIn(Instruccion):
    def __init__(self, objeto, listaAtributos, linea, columna):
        self.objeto = objeto
        self.listaAtributos = listaAtributos
        self.linea = linea
        self.columna = columna
        super().__init__()

class StructAtributos(Instruccion):
    def __init__(self, id, tipo,linea, columna):
        self.id = id
        self.tipo = tipo
        self.linea = linea
        self.columna = columna
        super().__init__()

class DeclaracionStruct(Instruccion):
    def __init__(self,id, tipo, idstruct, atributos,linea,columna):
        self.id = id
        self.tipo = tipo
        self.idstruct = idstruct
        self.atributos = atributos
        self.linea = linea 
        self.columna = columna
        super().__init__()

class OperacionStruct(Instruccion):
    def __init__(self,idstruct, lstid,linea,columna) :
        self.idstruct = idstruct
        self.lstid = lstid
        self.linea = linea 
        self.columna = columna
        super().__init__()
#arreglos
class DeclaracionArreglos(Instruccion):
    def __init__(self,id,listavalores,linea, columna):
        self.id = id
        self.lista = listavalores
        self.linea = linea
        self.columna = columna
        super().__init__()

class ValorArreglo(Instruccion):
    def __init__(self,Valor, linea, columna):
        self.valor = Valor
        self.linea = linea
        self.columna = columna
        super().__init__()