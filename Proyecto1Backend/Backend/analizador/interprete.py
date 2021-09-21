import Gramatica as g
import ts as TS
import math
from expresiones import *
from Instruccion import *
from ArbolCaracteres import *
import Errores as err
import subprocess
import Objetostruct as st
import objetoarreglo as arre

class Funcionesaux:
    def __init__(self,idfuncion,parametros,instrucciones,tipo):
        self.idfuncion = idfuncion
        self.parametros = parametros
        self.instrucciones = instrucciones 
        self.tipo = tipo

class interprete:
    # opreciones
    def __init__(self,Instruccion,ts):
        self.Instruccion = Instruccion
        self.ts = ts
        self.cont_global = 0
        self.break_global = 0
        self.return_global = 0
        self.listaFunciones = []
        self.valorretorna = None
        self.salida = ''
        self.lst_errores = g.lst_error
        self.local = []
        self.structs = st.bloqueStruct()

#operaciones
    def procesar_operacion(self, operacion,ts):
        if isinstance(operacion, OperacionNumerica):
            return self.procesar_operacionNum(operacion,ts)
        elif isinstance(operacion, OperacionLogica):
            return self.procesar_operacionLog(operacion,ts)
        elif isinstance(operacion, OperacionRelacional):
            return self.procesar_operacionRel(operacion,ts)
        elif isinstance(operacion, OperacionVariable):
            return self.procesar_valor(operacion,ts)
        elif isinstance(operacion, OperacionNumero):
            return self.procesar_valor(operacion,ts)
        elif isinstance(operacion, OperacionCadena):
            return self.procesar_valor(operacion,ts)
        elif isinstance(operacion, OperacionCaracter):
            return self.procesar_valor(operacion,ts)
        elif isinstance(operacion, OperacionBooleana):
            return self.procesar_valor(operacion,ts)
        elif isinstance(operacion,OperacionNULO):
            return None;
        elif isinstance(operacion, OperacionUnaria):
            return self.procesar_operacionunaria(operacion,ts)
        elif isinstance(operacion, OperacionSen):
            return self.procesar_sen(operacion,ts)
        elif isinstance(operacion, OperacionCos):
            return self.procesar_cos(operacion,ts)
        elif isinstance(operacion, OperacionTan):
            return self.procesar_tan(operacion,ts)
        elif isinstance(operacion, OperacionSQRT):
            return self.procesar_sqrt(operacion,ts)
        elif isinstance(operacion, OperacionLog10):
            return self.procesar_log10(operacion,ts)
        elif isinstance(operacion, OperacionLog):
            return self.procesar_log(operacion,ts)
        elif isinstance(operacion, OperacionLOWER):
            return self.procesar_lower(operacion,ts)
        elif isinstance(operacion, OperacionUPPER):
            return self.procesar_upper(operacion,ts)
        elif isinstance(operacion, OperacionLenght):
            return self.procesar_length(operacion,ts)
        elif isinstance(operacion, OperacionParse):
            return self.procesar_parse(operacion)
        elif isinstance(operacion, OperacionTrunc):
            return self.procesar_trunc(operacion)
        elif isinstance(operacion, OperacionFloat):
            return self.procesar_float(operacion)
        elif isinstance(operacion, OperacionString):
            return self.procesar_Fstring(operacion,ts)
        elif isinstance(operacion, OperacionTypeof):
            return self.procesar_typeof(operacion,ts)
        elif isinstance(operacion, llamada):
            return self.procesar_llamada(operacion,ts)
        elif isinstance(operacion, OperacionStruct):
            return self.procesar_operacionStruct(operacion,ts)
        elif isinstance(operacion,OperacionArreglo):
            return self.procesar_operacionArreglo(operacion,ts)
        elif isinstance(operacion,OperacionArregloget):
            return self.procesar_operacionArregloget(operacion,ts)
        
        elif isinstance(operacion,OperacionPop):
            return self.procesar_arreglopop(operacion,ts)
        else: 
            nuevo = err.TokenError("Semantico","Operacion desconocida", operacion.linea,operacion.columna)
            self.lst_errores.append(nuevo)

#unaria

    def procesar_operacionunaria(self,operacion,ts):
        op1 = self.procesar_valor(operacion.op1,ts)
        try:
            if operacion.operacion == OPERACION_LOGICA.NOT:
                if op1 == True:
                   return 0
                elif op1 == 0:
                    return False
                else: 
                    nuevo = err.TokenError("Semantico","opreacion not invalida", operacion.linea,operacion.columna)
                    self.lst_errores.append(nuevo)
                    return 0
            elif operacion.operacion == OPERACION_NUMERICA.RESTA:
                if isinstance(op1,int) or isinstance(op1,float):
                    return -1*op1
            else :
                nuevo = err.TokenError("Semantico","tipo \"{0}\" desconocido".format(operacion), operacion.linea,operacion.columna)
                self.lst_errores.append(nuevo)
                return op1
        except:
            nuevo = err.TokenError("Semantico","Operacion \"{0}\" desconocido".format(operacion), operacion.linea,operacion.columna)
            self.lst_errores.append(nuevo)

#numerica 
    def procesar_operacionNum(self, operacion,ts):
        try:
            if operacion.operacion == OPERACION_NUMERICA.MULTIPLICACION: 
                op1 = self.procesar_valor(operacion.opIzq,ts)
                op2 = self.procesar_valor(operacion.opDer,ts)
                if isinstance(op1, ArbolCaracter) and isinstance(op2, ArbolCaracter):
                    return str(op1.getText().replace("\"", "") + op2.getText().replace("\"", ""))
                elif isinstance(op1, ArbolCaracter) and isinstance(op2,str):
                    return str(op1.getText().replace("\"", "")) + str(op2).replace("\"", "")
                elif isinstance(op1, str) and isinstance(op2,ArbolCaracter):
                    return op1.replace("\"", "") + op2.getText().replace("\"", "")
                elif isinstance(op1,str) and isinstance(op2,str):
                    return str(op1) + str(op2)
                else: 
                    return op1 * op2 
            elif operacion.operacion == OPERACION_NUMERICA.POTENCIA:
                op1 = self.procesar_valor(operacion.opIzq,ts)
                op2 = self.procesar_valor(operacion.opDer,ts)
                if  isinstance(op1, ArbolCaracter) and (isinstance(op2, int) or isinstance(op2,float)):
                    return str(op1.getText().replace("\"", "") * op2)
                elif  isinstance(op1, str):
                   return op1.replace('\'', '') * op2
                else: 
                    return op1 ** op2 
            elif operacion.operacion == OPERACION_NUMERICA.SUMA:
                return self.procesar_valor(operacion.opIzq,ts) + self.procesar_valor(operacion.opDer,ts)
            elif operacion.operacion == OPERACION_NUMERICA.RESTA:
                return self.procesar_valor(operacion.opIzq,ts) - self.procesar_valor(operacion.opDer,ts)
            elif operacion.operacion == OPERACION_NUMERICA.DIVISION:
                return self.procesar_valor(operacion.opIzq,ts) / self.procesar_valor(operacion.opDer,ts)
            elif operacion.operacion == OPERACION_NUMERICA.MODULAR:
                return self.procesar_valor(operacion.opIzq,ts) % self.procesar_valor(operacion.opDer,ts)
            else:
                nuevo = err.TokenError("Semantico","Error al realizar la operacion Numerica ",  0,0)
                self.lst_errores.append(nuevo)
                return None
        except:
            nuevo = err.TokenError("Semantico","Error al realizar la operacion Numerica ",  0,0)
            self.lst_errores.append(nuevo)

#relacional 

    def procesar_operacionRel(self,operacion,ts):
        op1 = self.procesar_operacion(operacion.opIzq,ts)
        op2 = self.procesar_operacion(operacion.opDer,ts)
        if isinstance(op1,ArbolCaracter): op1 = op1.getText()
        if isinstance(op2,ArbolCaracter): op2 = op2.getText()
        try:
            if operacion.operacion == OPERACION_RELACIONAL.IGUAL: return True if(op1==op2) else False
            elif operacion.operacion == OPERACION_RELACIONAL.MAYOR: return True if(op1>op2) else False
            elif operacion.operacion == OPERACION_RELACIONAL.MENOR: return True if(op1<op2) else False
            elif operacion.operacion == OPERACION_RELACIONAL.DIFERENTE: return True if(op1!=op2) else False
            elif operacion.operacion == OPERACION_RELACIONAL.MAYORQUE: return True if(op1>=op2) else False
            elif operacion.operacion == OPERACION_RELACIONAL.MENORQUE: return True if(op1 <= op2) else False
            else:
                nuevo = err.TokenError("Semantico","Error al realizar la operacion Relacional ",  0,0)
                self.lst_errores.append(nuevo)
                return None
        except : 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion Relacion desconocida", 0,0)
            self.lst_errores.append(nuevo)

#logica

    def procesar_operacionLog(self,operacion,ts):
        op1 = self.procesar_valor(operacion.opIzq,ts)
        op2 = self.procesar_valor(operacion.opDer,ts)
        izq = False
        der = False
        if op1 == True:
            izq = True
        elif op1 == False:
            izq = False
        else: 
            nuevo = err.TokenError("Semantico","Tipo desconocida",  0,0)
            self.lst_errores.append(nuevo)
            return 0
        if op2 == True:
            der = True
        elif op2 == False:
            der = False
        else: 
            nuevo = err.TokenError("Semantico","Tipo desconocida",  0,0)
            self.lst_errores.append(nuevo)
            return 0
        try:
            if operacion.operacion == OPERACION_LOGICA.AND: 
                return True if (izq and der) else False
            elif operacion.operacion == OPERACION_LOGICA.OR:
                return True if (izq or der) else False
            else:
                nuevo = err.TokenError("Semantico","Error al realizar la operacion Logica ",  0,0)
                self.lst_errores.append(nuevo)
                return None
        except:
            nuevo = err.TokenError("Semantico","Error al realizar la operacion Logica", 0,0)
            self.lst_errores.append(nuevo)

#nativas

    def procesar_parse(self,operacion):
        if operacion.tipo == Tipo.ENTERO:
            return int(float(operacion.valor))
        elif operacion.tipo == Tipo.DECIMAL:
            return float(operacion.valor)
        else:
            nuevo = err.TokenError("Semantico","tipo desconocido", operacion.linea,0)
            self.lst_errores.append(nuevo)

    def procesar_trunc(self,operacion):
        if isinstance(operacion.valor, float):
             return int(float(operacion.valor))
        else: 
            nuevo = err.TokenError("Semantico","tipo no es float", operacion.linea,0)
            self.lst_errores.append(nuevo)
    
    def procesar_float(self,operacion):
        if isinstance(operacion.valor, int):
            return float(operacion.valor)
        else: 
            nuevo = err.TokenError("Semantico","Valor no es Entero", operacion.linea,0)
            self.lst_errores.append(nuevo)

    def procesar_Fstring(self,operacion,ts):
        if operacion.valor != None:
            return  "\""+ str(self.procesar_valor(operacion.valor,ts)) + "\""
        else: #faltan arreglos
            nuevo = err.TokenError("Semantico","error al convertir en string", operacion.linea,0)
            self.lst_errores.append(nuevo)
    
    def procesar_typeof(self,operacion,ts):
            op1 = self.procesar_operacion(operacion.valor,ts)  
            if op1 == False:
                tipo = Tipo.BOOL
            elif op1 == True :
                tipo = Tipo.BOOL  
            elif isinstance(op1, int):
                tipo = Tipo.ENTERO 
            elif isinstance(op1, float): 
                tipo = Tipo.DECIMAL
            elif isinstance(op1, ArbolCaracter): 
                 tipo = Tipo.STRING
            elif op1 == None :
                tipo = Tipo.NULO
            else: 
                tipo = Tipo.INVALIDO

            if tipo == Tipo.ENTERO:
                return "INT64"
            elif tipo == Tipo.DECIMAL:
                return "FLOAT64"
            elif tipo == Tipo.BOOL:
                return "BOOLEAN"
            elif tipo == Tipo.CHAR:
                return "CHAR"
            elif tipo == Tipo.STRING:
                return "CADENA"
            elif tipo == Tipo.NULO:
                return "NOTHING"
            else:
                nuevo = err.TokenError("Semantico","Tipo Desconocido", operacion.linea,0)
                self.lst_errores.append(nuevo)

#nativas Parte 2

    def procesar_sen(self,operacion,ts):
        op1 = self.procesar_valor(operacion.operador,ts) 
        try:
            return math.sin(op1)
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)
        
    def procesar_cos(self,operacion,ts):
        op1 = self.procesar_valor(operacion.operador,ts) 
        try:
            return math.cos(op1)
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)
    
    def procesar_tan(self,operacion,ts):
        op1 = self.procesar_valor(operacion.operador,ts) 
        try:
            return math.tan(op1)
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)

    def procesar_log10(self,operacion,ts):
        op1 = self.procesar_valor(operacion.operador,ts) 
        try:
            return math.log10(op1)
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)
    
    def procesar_log(self,operacion,ts):
        op1 = self.procesar_valor(operacion.operador,ts) 
        op2 = self.procesar_valor(operacion.operador2,ts) 
        try:
            return math.log(op1,op2)
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)

    def procesar_sqrt(self,operacion,ts):
        op1 = self.procesar_valor(operacion.operador,ts) 
        try:
            return math.sqrt(op1)
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)
    
    def procesar_lower(self,operacion,ts):
        op1 = self.procesar_valor(operacion.operador,ts) 
        try:
            if isinstance(op1, ArbolCaracter):
                opaux = op1.getText().replace("\"","")
                return opaux.lower()
            else:
                opaux = self.procesar_operacion(operacion.operador,ts) 
                return opaux.lower()
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)

    def procesar_upper(self,operacion,ts):
        op1 = self.procesar_valor(operacion.operador,ts) 
        try:
            if isinstance(op1, ArbolCaracter):
                opaux = op1.getText().replace("\"","")
                return opaux.upper()
            else:
                opaux = self.procesar_operacion(operacion.operador,ts) 
                return opaux.upper()
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)
    
    def procesar_length(self,operacion,ts):
        
        op1 = self.procesar_valor(operacion.operador,ts)
        try:
            if isinstance(op1, ArbolCaracter):
                opaux = op1.getText().replace("\"","")
                return opaux.__len__()
            else:
                opaux = self.procesar_operacion(operacion.operador,ts)
                return opaux.__len__()
        except: 
            nuevo = err.TokenError("Semantico","Error al realizar la operacion \"{0}\"".format(operacion.operador), operacion.line,operacion.columna)
            self.lst_errores.append(nuevo)

#valores
    def procesar_valor(self, expresion,ts):
        if isinstance(expresion, OperacionNumero):
            if isinstance(expresion.num, int):
                return int(expresion.num)
            elif isinstance(expresion.num, float):
                return float(expresion.num)
            else:
                nuevo = err.TokenError("Semantico","valor numerico desconocido", expresion.linea,expresion.columna)
                self.lst_errores.append(nuevo)
                return None
        elif isinstance(expresion, OperacionVariable):
            if ts.verificar(expresion.id,ts) == True:     
                return ts.get(expresion.id, ts)
            else:
                nuevo = err.TokenError("Semantico","Variable desconocida", expresion.linea,expresion.columna)
                self.lst_errores.append(nuevo)
                return None
        elif isinstance(expresion, OperacionCadena):
            return self.procesar_cadena(expresion)
        elif isinstance(expresion, OperacionCaracter):
            return str(expresion.car)
        elif isinstance(expresion, OperacionBooleana):
            if expresion.val.lower() == 'false':
                return False
            elif expresion.val.lower() == 'true':
                return True
            else:
                nuevo = err.TokenError("Semantico","Booleano desconocido", expresion.linea,expresion.columna)
                self.lst_errores.append(nuevo)
                return None
        elif isinstance(expresion,OperacionNULO):
            return None
        else:
            return self.procesar_operacion(expresion,ts)

    def procesar_cadena(self,expresion):
        if isinstance(expresion,OperacionCadena):
            return ArbolCaracter(expresion.cadena)

##intrucciones 
#declaracion 
    def procesar_Declaracion(self, instr, ts):
        op1 =  self.procesar_operacion(instr.valor,ts)
        if instr.ambiente == ['global']:
            if isinstance(op1, ArbolCaracter):
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,op1.getText().replace("\"", "") , Tipo.STRING,  instr.ambiente,instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, op1.getText().replace("\"", ""), Tipo.STRING,  instr.ambiente,instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id),instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)
            else: 
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,op1 , instr.tipo,  instr.ambiente, instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, op1, instr.tipo, instr.ambiente,instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id), instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)
        elif instr.ambiente == ['local']:
            print('error')
        else: 
            if isinstance(op1, ArbolCaracter):
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,op1.getText().replace("\"", "") , Tipo.STRING,  'Global',instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, op1.getText().replace("\"", ""), Tipo.STRING,  'Global', instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id),instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)
            else: 
               
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,op1 , instr.tipo, 'Global', instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, op1, instr.tipo, 'Global',instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id), instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)

    def procesar_declaracionaux(self,instr,ts):
        if instr.tipo == ['global']:
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,None , Tipo.STRING,  instr.tipo,instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, None, Tipo.STRING,  instr.tipo,instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id),instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)
        elif instr.tipo == ['local']:
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,None , Tipo.STRING,  instr.tipo,instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, None, Tipo.STRING,  instr.tipo,instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id),instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)
       
            

    def procesar_DeclaracionesAmbito(self,ambito,instr,ts):
        op1 =  self.procesar_operacion(instr.valor,ts)
        if instr.ambiente == ['global']:
            self.procesar_Declaracion(instr,ts)
        elif instr.ambiente == ['local']:
            if isinstance(op1, ArbolCaracter):
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,op1.getText().replace("\"", "") , Tipo.STRING,  ambito,instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, op1.getText().replace("\"", ""), Tipo.STRING,  ambito,instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id),instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)
            else: 
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,op1 , instr.tipo,  ambito, instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, op1, instr.tipo, ambito,instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id), instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)
        else:
            if isinstance(op1, ArbolCaracter):
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,op1.getText().replace("\"", "") , Tipo.STRING,  ambito,instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, op1.getText().replace("\"", ""), Tipo.STRING,  ambito,instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id),instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)
            else: 
                if ts.verificar(instr.id, ts) == False:
                    simbolo = TS.Simbolo(instr.id,op1 , instr.tipo,  ambito, instr.linea, instr.columna)
                    ts.agregar(simbolo)
                elif instr.valor != None:
                    simbolo = TS.Simbolo(instr.id, op1, instr.tipo, ambito,instr.linea, instr.columna)
                    ts.actualizar(simbolo)
                else: 
                    nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(instr.id), instr.linea,instr.columna)
                    self.lst_errores.append(nuevo)


# impresion valores sencillos
    def procesar_impresion(self,instr, ts):
        if instr.tipo == ['print']:
            for val in instr.val:
                if isinstance(val,OperacionVariable): 
                    self.salida = self.salida + str(self.procesar_variable(val,ts))  
                elif isinstance(val,OperacionCadena): 
                    op1 = self.procesar_valor(val,ts)
                    if isinstance(op1,ArbolCaracter): 
                        self.salida = self.salida + op1.getText().replace("\"", "")
                else: 
                    self.salida = self.salida +  str(self.procesar_operacion(val,ts))
        else: 
            for val in instr.val:
                if isinstance(val,OperacionVariable): 
                    self.salida = self.salida + str(self.procesar_variable(val,ts)) 
                elif isinstance(val,OperacionCadena): 
                    op1 = self.procesar_valor(val,ts)
                    if isinstance(op1,ArbolCaracter): 
                        self.salida = self.salida + op1.getText().replace("\"", "")
                else: 
                    self.salida = self.salida +  str(self.procesar_operacion(val,ts)) 
            self.salida = self.salida + '\n'
    
    def procesar_impresionvacia(self,instr,ts):
        if instr.tipo == ['print']:
           self.salida = self.salida
        else:   
            self.salida = self.salida + '\n'

    def procesar_variable(self,val,ts):
        if ts.existe(val.id) == True:
            return(self.procesar_valor(val,ts))
        else:
            nuevo = err.TokenError("Semantico","Valor \"{0}\" desconocido".format(val.id), val.linea,val.columna)
            self.lst_errores.append(nuevo)

# impresion arreglos

#sentencia if 
    def procesar_if(self,instr,ts):
        s_if = instr.s_if
        s_else = instr.s_else
        s_elif = instr.s_elif
        entro = False
        if s_if != None: 
            if self.procesar_operacion(s_if.condicion,ts):
                val = self.procesar_instrucciones(s_if.sentencias, ts)
                entro = True
                if val != None:
                    return val
        if s_elif != None and entro == False:
            for aux in s_elif:
                if self.procesar_operacion(aux.condicion,ts):
                    val = self.procesar_instrucciones(aux.sentencias, ts)
                    entro = True
                    if val != None:
                        return val
        if s_else != None and entro == False:
            val = self.procesar_instrucciones(s_else.sentencias, ts)
            if val != None:
                return val
        
        
#sentencias while
    
    def procesar_while(self,instr,ts):
        while self.procesar_operacion(instr.condicion,ts):
            if self.cont_global == 1:
                self.cont_global = 0
                continue
            if self.break_global == 2:
                self.break_global = 0
                break
            else: 
                val = self.procesar_instrucciones(instr.sentencias,ts)
                if val != None:
                    return val
        
#sentencia For

    def procesar_for(self,instr,ts):

        val = None
        simbolo = TS.Simbolo(instr.id, 0, None,'for', instr.linea, 0)
        ts.agregar(simbolo)
        if isinstance(instr.condicional, condicionalSimple):
            op1 = self.procesar_operacion(instr.condicional.operacion,ts)
            if isinstance(op1, ArbolCaracter):
                variable = instr.id
                for variable in self.procesar_operacion(instr.condicional.operacion,ts).getText():
                    simbolo = TS.Simbolo(instr.id, variable, str,'for', instr.linea, 0)
                    ts.actualizar(simbolo)
                    if self.cont_global == 1:
                        self.cont_global = 0
                        continue
                    if self.break_global == 2:
                        self.break_global = 0
                        break
                    if self.return_global == 3:
                        self.return_global = 0
                        return 
                    else: 
                        val = self.procesar_instrucciones(instr.sentencias,ts)
            else : 
                variable = instr.id
                for variable in op1:
                    simbolo = TS.Simbolo(instr.id, variable, str, 'for',instr.linea, 0)
                    ts.actualizar(simbolo)
                    if self.cont_global == 1:
                        self.cont_global = 0
                        continue
                    if self.break_global == 2:
                        self.break_global = 0
                        break
                    if self.return_global == 3:
                        self.return_global = 0
                        return 
                    else: 
                       val = self.procesar_instrucciones(instr.sentencias,ts)
        elif isinstance(instr.condicional,condicionalRango):
            
            op1 = self.procesar_operacion(instr.condicional.rangoizq,ts)
            op2 = self.procesar_operacion(instr.condicional.rangoder,ts)
            variable = instr.id
            if op1 <= op2:
                for variable in range(op1, op2):
                    simbolo = TS.Simbolo(instr.id, variable, None, 'for',instr.linea, 0)
                    ts.actualizar(simbolo)
                    if self.cont_global == 1:
                            self.cont_global = 0
                            continue
                    if self.break_global == 2:
                            self.break_global = 0
                            break
                    if self.return_global == 3:
                            self.return_global = 0
                            return 
                    else: 
                        val = self.procesar_instrucciones(instr.sentencias,ts)
            else: 
                print("indice izquierdo mayor al derecho")
        else: 
            nuevo = err.TokenError("Semantico","Condicional \"{0}\" desconocido".format(instr.condicional), instr.linea,instr.columna)
            self.lst_errores.append(nuevo)
        
        return val

#funciones 
    def procesar_Funciones(self,inst,ts):
        verificar = False
        if len(self.listaFunciones) > 0:
            for func in self.listaFunciones:
                if func.idfuncion == inst.idFuncion:
                    verificar = True
                    nuevo = err.TokenError("Semantico","Condicional \"{0}\" desconocido".format(inst.idFuncion), inst.linea,inst.columna)
                    self.lst_errores.append(nuevo)
            if verificar == False:
                self.listaFunciones.append(Funcionesaux(inst.idFuncion, inst.parametros, inst.sentencias,TIPO_ESTRUCTURAS.FUNCION))
                simbolo = TS.Simbolo(inst.idFuncion,None , TIPO_ESTRUCTURAS.FUNCION,  'Global', inst.linea, inst.columna)
                ts.agregar(simbolo)
        elif len(self.listaFunciones) == 0:
            self.listaFunciones.append(Funcionesaux(inst.idFuncion, inst.parametros, inst.sentencias,TIPO_ESTRUCTURAS.FUNCION))
            simbolo = TS.Simbolo(inst.idFuncion,None , TIPO_ESTRUCTURAS.FUNCION,  'Global', inst.linea, inst.columna)
            ts.agregar(simbolo)
#llamada
    def procesar_llamada(self, inst, ts):
        #por valor
        tablalocal = TS.TablaSimbolos()
        tablalocal.setPadre(ts)
        if self.listaFunciones != None:
            for func in self.listaFunciones:
                if func.idfuncion == inst.idfuncion:
                    if func.tipo == TIPO_ESTRUCTURAS.FUNCION:
                        if func.parametros != None:
                            if len(func.parametros) == len(inst.parametros):
                                cont = 0
                                while cont < len(func.parametros):
                                    simbololocal = TS.Simbolo(func.parametros[cont].idparametro,self.procesar_operacion(inst.parametros[cont],ts),func.parametros[cont].tipo,inst.idfuncion,func.parametros[cont].linea,func.parametros[cont].columna)
                                    tablalocal.agregar(simbololocal)
                                    cont = cont +1
                            else: 
                                nuevo = err.TokenError("Semantico","Parametros no coinciden", 0,0)
                                self.lst_errores.append(nuevo)
                        if isinstance(func.instrucciones, Declaracion):
                            self.procesar_DeclaracionesAmbito(func.idfuncion,func.instrucciones,tablalocal)
                        val = self.procesar_instrucciones(func.instrucciones, tablalocal)
                        if val != None:
                            
                            return val
                    else:
                        struct = {}
                        struct = self.structs.diccionario[func.idfuncion].copy()
                        if len(struct) == len(inst.parametros):
                            contador = 0
                            for key in struct.keys():
                               
                                valor = self.procesar_operacion(inst.parametros[contador], ts)
                                contador += 1
                               
                                if isinstance(valor,ArbolCaracter):
                                    struct[key] = valor.getText()
                                else:
                                    struct[key] = valor
                            return struct
                        else:
                            nuevo = err.TokenError("Semantico","valores no coinciden",0,0)
                            self.lst_errores.append(nuevo)
        else:
                nuevo = err.TokenError("Semantico","Funciones no declaradas", 0,0)
                self.lst_errores.append(nuevo)
        self.local.append(tablalocal)

#return 
    def procesar_return(self,inst,ts):
        self.return_global = 0
        return self.procesar_operacion(inst.operacion,ts)

#structs

    def procesar_struct(self,inst,ts):
        verificar = False
        if len(self.listaFunciones) > 0:
            for func in self.listaFunciones:
                if func.idfuncion == inst.objeto:
                    verificar = True
                    print('ya existe funcion con ese nombre')
                    return None
            if verificar == False:
                self.listaFunciones.append(Funcionesaux(inst.objeto, 0, 0,TIPO_ESTRUCTURAS.CONSTRUCTOR))
        elif len(self.listaFunciones) == 0:
            self.listaFunciones.append(Funcionesaux(inst.objeto, 0, 0,TIPO_ESTRUCTURAS.CONSTRUCTOR))
        
        clave = inst.objeto
        objeto = {}
        for val in inst.listaAtributos:
            tipo = self.structs.obtener(val.tipo)
            if tipo != 1:
                objeto[val.id] = tipo
            else:
                objeto[val.id] = ''
            simbolo = TS.Simbolo(" "+val.id,None, val.tipo, clave,inst.linea, inst.columna)
            ts.agregar(simbolo)
        self.structs.agregar(clave,objeto)
        simbolo = TS.Simbolo(clave,objeto, TIPO_ESTRUCTURAS.STRUCT, "Global",inst.linea, inst.columna)
        ts.agregar(simbolo)

#operacion struct

    def procesar_operacionStruct(self,expresion,ts):
        if ts.verificar(expresion.idstruct,ts):
            struct = ts.get(expresion.idstruct,ts)
            struct = st.bloqueStruct(struct)
            if struct != False:
                if struct.existe(expresion.lstid):
                    return struct.get2(expresion.lstid)
                else: 
                    nuevo = err.TokenError("Semantico","Operacion struct \"{0}\"desconocida".format(expresion.idstruct), expresion.linea,expresion.columna)
                    self.lst_errores.append(nuevo)
            else:
                nuevo = err.TokenError("Semantico","Operacion struct \"{0}\"desconocida".format(expresion.idstruct), expresion.linea,expresion.columna)
                self.lst_errores.append(nuevo)
        else: 
            nuevo = err.TokenError("Semantico","Operacion struct \"{0}\"desconocida".format(expresion.idstruct), expresion.linea,expresion.columna)
            self.lst_errores.append(nuevo)

#asginacion struct

    def procesar_asignacionstruct(self,expresion,ts):
        if ts.verificar(expresion.idstruct,ts):
            struct = ts.get(expresion.idstruct,ts)
            struct = st.bloqueStruct(struct)
            op = self.procesar_operacion(expresion.operacion,ts)
            if isinstance(op,ArbolCaracter):
                if struct != False:
                    if struct.existe(expresion.lstid):
                        return struct.set(expresion.lstid,op.getText())
                    else: 
                        nuevo = err.TokenError("Semantico","Operacion struct \"{0}\"desconocida".format(expresion.idstruct), expresion.linea,expresion.columna)
                        self.lst_errores.append(nuevo)
                else:
                    nuevo = err.TokenError("Semantico","Operacion struct \"{0}\"desconocida".format(expresion.idstruct), expresion.linea,expresion.columna)
                    self.lst_errores.append(nuevo)
            else:
                if struct != False:
                    if struct.existe(expresion.lstid):
                        return struct.set(expresion.lstid,op)
                    else: 
                        nuevo = err.TokenError("Semantico","Operacion struct \"{0}\"desconocida".format(expresion.idstruct), expresion.linea,expresion.columna)
                        self.lst_errores.append(nuevo)
                else:
                    nuevo = err.TokenError("Semantico","Operacion struct \"{0}\"desconocida".format(expresion.idstruct), expresion.linea,expresion.columna)
                    self.lst_errores.append(nuevo)

#arreglos 

    def procesar_declaracionArreglo(self,inst,ts):
        arr = []
        for val in inst.lista:
            if isinstance(self.procesar_operacion(val,ts),ArbolCaracter ):
                op1 = self.procesar_operacion(val,ts)
                arr.append(op1.getText().replace("\"",""))
            else: 
                arr.append(self.procesar_operacion(val,ts))
        simbolo = TS.Simbolo(inst.id,arr, TIPO_ESTRUCTURAS.ARREGLO, "Global",inst.linea, inst.columna)
        ts.agregar(simbolo)

    def procesar_operacionArreglo(self,operacion,ts):
        aux = []
        for val in operacion.lstoperacion:
                if isinstance(val,OperacionArreglo):
                    aux.append(self.procesar_operacionArreglo(val,ts))
                else : 
                    aux.append(self.procesar_operacion(val,ts))
        return aux

    def procesar_operacionArregloget(self,operacion,ts):
        if ts.verificar(operacion.id,ts):
            arr = ts.get(operacion.id,ts)
            arr = arre.bloqueArreglo(arr)
            posiciones = []
            
            for val in operacion.listaposicion:
                posiciones.append(self.procesar_operacion(val.operacion,ts))

            if arr.existe(posiciones):
                return arr.obtener(posiciones)
            else:
                nuevo = err.TokenError("Semantico","indices fuera de rango", operacion.linea,operacion.columna)
                self.lst_errores.append(nuevo)
                return None
        
    def procesar_asignacionArreglo(self,inst,ts):
        if ts.verificar(inst.id,ts):
            arr = ts.get(inst.id,ts)
            arr = arre.bloqueArreglo(arr)
            posiciones = []
            for val in inst.listaposicion:
                posiciones.append(self.procesar_operacion(val.operacion,ts))

            if arr.existe(posiciones):
                valor = self.procesar_operacion(inst.operacion,ts)
                arr.actualizar(posiciones,valor)
            else:
                nuevo = err.TokenError("Semantico","indices fuera de rango", inst.linea,inst.columna)
                self.lst_errores.append(nuevo)
            

    def procesar_arreglopush(self, expresion,ts):
            if expresion.lista == None:
                if ts.verificar(expresion.arreglo,ts):
                    arr = ts.get(expresion.arreglo,ts)
                    arr = arre.bloqueArreglo(arr)
                    arr.agregar(self.procesar_operacion(expresion.valor,ts))
                    simbolo = TS.Simbolo(expresion.arreglo, arr.arreglo, TIPO_ESTRUCTURAS.ARREGLO,"Global", expresion.linea, 0)
                    ts.actualizar(simbolo)
                else:
                    nuevo = err.TokenError("Semantico","Identificador  \"{0}\"  no existe".format(expresion.arreglo), 0,0)
                    self.lst_errores.append(nuevo)
            else:
                if ts.verificar(expresion.arreglo,ts):
                    arr = ts.get(expresion.arreglo,ts)
                    arr = arre.bloqueArreglo(arr)
                    posiciones = []
                    for val in expresion.lista:
                        posiciones.append(self.procesar_operacion(val.operacion,ts))
                    if arr.existe(posiciones):
                        aux = arr.obtener(posiciones)
                        aux = arre.bloqueArreglo(aux)
                        aux.agregar(self.procesar_operacion(expresion.valor,ts))
                        simbolo = TS.Simbolo(expresion.arreglo, arr.arreglo, TIPO_ESTRUCTURAS.ARREGLO,"Global", expresion.linea, 0)
                        ts.actualizar(simbolo)
                else:
                    nuevo = err.TokenError("Semantico","Identificador  \"{0}\"  no existe".format(expresion.arreglo), 0,0)
                    self.lst_errores.append(nuevo)

    def procesar_arreglopop(self,expresion,ts):
        if ts.verificar(expresion.arreglo,ts):
                arr = ts.get(expresion.arreglo,ts)
                arr = arre.bloqueArreglo(arr)
                val = arr.sacar()
                return val
        else:
            nuevo = err.TokenError("Semantico","Identificador  \"{0}\"  no existe".format(expresion.arreglo), 0,0)
            self.lst_errores.append(nuevo)

# recorrer instrucciones
    def procesar_instrucciones(self, Instruccion, ts):
        # aqui van las intrucciones
        for instr in Instruccion:
            if isinstance(instr, Declaracion) and (self.break_global != 2 and self.cont_global != 1 and self.return_global != 3):
                self.procesar_Declaracion(instr, ts)
            elif isinstance(instr, Printval) and (self.break_global != 2 and self.cont_global != 1 and self.return_global != 3):
                self.procesar_impresion(instr, ts)
            elif isinstance(instr, If) and (self.break_global != 2 and self.cont_global != 1 and self.return_global != 3):
                valor =  self.procesar_if(instr,ts)
                if valor != None:
                    return valor
            elif isinstance(instr, While) and (self.break_global != 2 and self.cont_global != 1 and self.return_global != 3):
                valor = self.procesar_while(instr,ts)
                if valor != None:
                    return valor
            elif isinstance(instr, For) and (self.break_global != 2 and self.cont_global != 1 and self.return_global != 3):
                valor = self.procesar_for(instr,ts)
                if valor != None:
                    return valor
            elif isinstance(instr, SentenciaContinue):
                self.cont_global = 1
            elif isinstance(instr, SentenciaReturn) :
                self.return_global = 3
                return self.procesar_return(instr,ts) 
            elif isinstance(instr, SentenciaBreak) :
                self.break_global = 2
            elif isinstance(instr, Funcion) and (self.break_global != 2 and self.cont_global != 1 and self.return_global != 3):
                self.procesar_Funciones(instr,ts) 
            elif isinstance(instr, llamada)  and (self.break_global != 2 and self.cont_global != 1 and self.return_global != 3):
                self.procesar_llamada(instr,ts)
            elif isinstance(instr,StructsIn):
                self.procesar_struct(instr,ts)
            elif isinstance(instr,AsginacionStruc):
                self.procesar_asignacionstruct(instr,ts)
            elif isinstance(instr,DeclaracionArreglos):
                self.procesar_declaracionArreglo(instr,ts)
            elif isinstance(instr,AsignacionArreglo):
                self.procesar_asignacionArreglo(instr,ts)
            elif isinstance(instr,OperacionPush):
                self.procesar_arreglopush(instr,ts)
            elif isinstance(instr, PrintCadena):
                self.procesar_impresionvacia(instr,ts)
            elif isinstance(instr,Declaracionaux):
                self.procesar_declaracionaux(instr,ts)
            else:
                nuevo = err.TokenError("Semantico","Instruccion  desconocida", 0,0)
                self.lst_errores.append(nuevo)
        self.ts = ts
        
    
    def run(self, instrucciones):
        self.procesar_instrucciones(instrucciones, self.ts)

    def graficar(self):
        try:
            file = ""
            file = file +  "digraph TablaSimbolos{\n"
            file = file + ("graph [ratio = fill]; node [label = \"\\N\", shape=plaintext];\n")
            file = file + ("graph [bb=\"0,0,352,154\"];\n")
            file = file + ("err [label = <\n")
            file = file +("<TABLE ALIGN = \"LEFT\">\n")
            file = file +("<TR><TD>IDENTIFICADOR</TD><TD>TIPO</TD><TD>AMBITO</TD><TD>LINEA</TD><TD>COLUMNA</TD></TR>\n") 
            for val2 in self.ts.simbolos:
                    file = file +("<TR>")
                    file = file +("<TD>")
                    file = file +(val2)
                    file = file +("</TD>")
                    file = file +("<TD>")
                    file = file +(str(self.ts.obtener(val2,self.ts).tipo))
                    file = file +("</TD>")
                    file = file +("<TD>")
                    file = file +(str(self.ts.obtener(val2,self.ts).ambito))
                    file = file +("</TD>")
                    file = file +("<TD>")
                    file = file +(str(self.ts.obtener(val2,self.ts).line))
                    file = file +("</TD>")
                    file = file +("<TD>")
                    file = file +(str(self.ts.obtener(val2,self.ts).column))
                    file = file +("</TD>")
                    file = file +("</TR>\n")       
            file = file +("</TABLE>")
            file = file +("\n>,];\n")
            file = file +("}")
        except:
            print("Error")
        finally:
            return file

    def graficarErrores(self):
        try:
            file = ""
            file = file +("digraph tablaErrores{\n")
            file = file +("graph [ratio = fill]; node [label = \"\\N\", shape=plaintext];\n")
            file = file +("graph [bb=\"0,0,352,154\"];\n")
            file = file +("err [label = <\n")
            file = file +("<TABLE ALIGN = \"LEFT\">\n")
            file = file +("<TR><TD>TIPO</TD><TD>DESCRIPCION</TD><TD>LINEA</TD><TD>COLUMNA</TD></TR>\n")
            for valor in self.lst_errores:
                file = file +("<TR>")
                file = file +("<TD>")
                file = file +(valor.tipo)
                file = file +("</TD>")
                file = file +("<TD>")
                file = file +(valor.descripcion)
                file = file +("</TD>")
                file = file +("<TD>")
                file = file +(str(valor.line))
                file = file +("</TD>")
                file = file +("<TD>")
                file = file +(str(valor.columna))
                file = file +("</TD>")
                file = file +("</TR>\n")
            file = file +("</TABLE>")
            file = file +("\n>,];\n")
            file = file +("}")
        except:
            print('Error al graficar')
        finally:
            return file
    
    def cmd(self,comando):
        subprocess.run(comando,shell=True)