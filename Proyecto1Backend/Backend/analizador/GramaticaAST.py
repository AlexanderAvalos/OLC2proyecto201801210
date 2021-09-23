import ply.yacc as yacc
import ply.lex as lex
from Instruccion import *
import re

indice = 0
class Nodo:
    def __init__(self,instruccion,nodoh) :
        self.instruccion = instruccion
        self.nodo = nodoh

class NodoH:
    def __init__(self,indice,nombre,hijos = []):
        self.indice = indice
        self.nombre = nombre
        self.hijos = hijos

    def agregar(self,hijo):
        self.hijos.append(hijo)
        

reservadas = {
    'nothing': 'NOTHING',
    'int64': 'INT64',
    'float64': 'FLOAT64', 
    'bool': 'BOOL',
    'char': 'CHAR',
    'string': 'STRING',
    'parse': 'PARSE',
    'uppercase': 'UPPERCASE',
    'println': 'PRINTLN',
    'lowercase': 'LOWERCASE',
    'log10': 'LOG10',
    'log': 'LOG',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'sqrt': 'SQRT',
    'print': 'PRINT',
    'function': 'FUNCTION',
    'end': 'END',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'struct': 'STRUCTR',
    'mutable': 'MUTABLE',
    'true': 'TRUE',
    'false': 'FALSE',
    'lenght': 'LENGHT',
    'elseif': 'ELSEIF',
    'parse':'PARSE',
    'trunc':'TRUNC',
    'push':'PUSH',
    'pop':'POP',
    'float':'FLOAT',
    'typeof':'TYPEOF',
    'global':'GLOBAL',
    'local': 'LOCALR' 
}


tokens = [
    # noreservadas
    'MAS',
    'MENOS',
    'MULTIPLICACION',
    'DIVISION',
    'POTENCIA',
    'MODULO',
    'MAYOR',
    'MENOR',
    'IGUAL',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'DOBLEPUNTO',
    'PUNTOYCOMA',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'COMA',
    'PUNTO',
    'AND',
    'OR',
    'NOT',
    # Datos
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
    'CARACTER',
    'DOSPUNTOS',
] + list(reservadas.values())


t_PUNTOYCOMA = r';'
t_DOSPUNTOS = r':'
t_MAS = r'\+'
t_MULTIPLICACION = r'\*'
t_MENOS = r'-'
t_DIVISION = r'/'
t_POTENCIA = r'\^'
t_MODULO = r'%'
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_IGUALIGUAL = r'=='
t_DIFERENTE = r'!='
t_DOBLEPUNTO = r'::'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORDER = r'\]'
t_CORIZQ = r'\['
t_COMA = r'\,'
t_PUNTO = r'\.'
t_OR = r'\|\|'
t_NOT = r'\!'
t_AND = r'&&'
t_IGUAL = r'='
t_ignore = " \t\r"

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error: %d ", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor del integer erroneo %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t


def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_CARACTER(t):
    r'\'.?\''
    t.value = t.value[1:-1]
    return t


def t_COMENTARIOSIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1


def t_COMENTARIOMULTIPLE(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')


def t_NUEVALINEA(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
   t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'COMA'),
    ('right', 'NOT'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALIGUAL', 'DIFERENTE'),
    ('left', 'MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'MODULO'),
    ('left', 'POTENCIA','SQRT'),
    ('right','UMENOS' )
    )

def getIndex():
    global indice
    indice = indice + 1
    return indice

def p_init(p):
    'init : instrucciones'
    nodoaux = NodoH(getIndex(),"init",[])
    for i in p[1].nodo:
        nodoaux.agregar(i)
    p[0] = Nodo(p[1].instruccion,nodoaux)

def p_instrucciones(p):
    'instrucciones : instrucciones instruccion'
    p[1].instruccion.append(p[2].instruccion)
    nodoaux = NodoH(getIndex(),"instruccion",[])
    nodoaux.agregar(p[2].nodo)
    p[1].nodo.append(nodoaux)
    nodo = NodoH(getIndex(),"Instrucciones",p[1].nodo)
    p[0]= Nodo(p[1].instruccion, [nodo] )

def p_instrucciones2(p):
    'instrucciones : instruccion'
    nodo = NodoH(getIndex(),"instruccion",[p[1].nodo])
    p[0] = Nodo([p[1].instruccion], [nodo])

def p_instruccion(p):
    ''' instruccion : asignacion
                    | arreglos
                    | nativa
                    | sentencia
                    | funcion
                    | callfuncion
                    | structs
    '''
    p[0] = p[1]

def p_sentencia(p):
    '''sentencia : if  
                 | for  
                 | while  
                 | return 
                 | continue
                 | break
    '''
    p[0] = p[1]

# arreglos 

def p_declaracionarreglos(p):
    'arreglos : ID IGUAL CORIZQ valores CORDER PUNTOYCOMA'
    nodo = NodoH(getIndex(),"arreglos",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(NodoH(getIndex(),"[",None))
    for val in p[4].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"]",None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(DeclaracionArreglos(p[1],p[4],p.lineno(1), buscar_columna(p.slice[1])),nodo)


def p_operacionarreglos(p):
    'operacion : CORIZQ  valores CORDER'
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(NodoH(getIndex(),"[",None))
    for val in p[2].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"]",None))
    p[0] = Nodo(OperacionArreglo(p[2],p.lineno(1), buscar_columna(p.slice[1])),nodo)

def p_operacionarreglo(p):
    'operacion : ID listaposiciones'
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    for val in p[2].nodo:
        nodo.agregar(val)
    p[0] = Nodo(OperacionArregloget(p[1],p[2],p.lineno(1), buscar_columna(p.slice[1])),nodo)

def p_asignacionArreglo(p):
    'asignacion : ID listaposiciones IGUAL operacion PUNTOYCOMA'
    nodo = NodoH(getIndex(),"asginacion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    for val in p[2].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(p[4].nodo)
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(AsignacionArreglo(p[1],p[2],p[4],p.lineno(1), buscar_columna(p.slice[1])),nodo)

def p_listaposiciones(p):
    'listaposiciones : listaposiciones listaposicion'
    p[1].instruccion.append(p[2].instruccion)
    nodoaux = NodoH(getIndex(),"listaposiciones",[])
    nodoaux.agregar(p[2].nodo)
    p[1].nodo.append(nodoaux)
    nodo = NodoH(getIndex(),"listaposicion",p[1].nodo)
    p[0]= Nodo(p[1].instruccion, [nodo] )

def p_listaposiciones2(p):
    'listaposiciones : listaposicion'
    nodo = NodoH(getIndex(),"listaposicion",[p[1].nodo])
    p[0] = Nodo([p[1].instruccion], [nodo])

def p_listaposicion(p):
    'listaposicion : CORIZQ operacion CORDER'
    nodo = NodoH(getIndex(),"listaposicion",[])
    nodo.agregar(NodoH(getIndex(),"[",None))
    nodo.agregar(p[2].nodo)
    nodo.agregar(NodoH(getIndex(),"]",None))
    p[0] = Nodo(listaindicies(p[2],p.lineno(1), buscar_columna(p.slice[1])),nodo)


# delcaracion struct
def p_structMutable(p):
    'structs : MUTABLE STRUCTR ID listaAtributos END PUNTOYCOMA'
    nodo = NodoH(getIndex(),"structs",[])
    nodo.agregar(NodoH(getIndex(),"MUTABLE",None))
    nodo.agregar(NodoH(getIndex(),"STRUCT",None))
    nodo.agregar(NodoH(getIndex(),str(p[3]),None))
    for val in p[4].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"END",None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(StructsIn(p[3], p[4], p.lineno(1), buscar_columna(p.slice[1])),nodo)


def p_structInmutable(p):
    'structs : STRUCTR ID listaAtributos END PUNTOYCOMA'
    nodo = NodoH(getIndex(),"structs",[])
    nodo.agregar(NodoH(getIndex(),"STRUCT",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    for val in p[3].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"END",None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(StructsIn(p[2], p[3], p.lineno(1), buscar_columna(p.slice[1])),nodo)

def p_listaatributos(p):
    'listaAtributos : listaAtributos lista'
    p[1].instruccion.append(p[2].instruccion)
    nodoaux = NodoH(getIndex(),"listaAtributos",[])
    nodoaux.agregar(p[2].nodo)
    p[1].nodo.append(nodoaux)
    nodo = NodoH(getIndex(),"lista",p[1].nodo)
    p[0]= Nodo(p[1].instruccion, [nodo] )

def p_listaAtributos(p):
    'listaAtributos : lista '
    nodo = NodoH(getIndex(),"lista",[p[1].nodo])
    p[0] = Nodo([p[1].instruccion], [nodo])

def p_lista(p):
    'lista : ID DOBLEPUNTO tipo PUNTOYCOMA'
    nodo = NodoH(getIndex(),"listaposicion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    nodo.agregar(NodoH(getIndex(),"::",None))
    nodo.agregar(NodoH(getIndex(),str(p[3]),None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(StructAtributos(p[1],p[3],p.lineno(1), buscar_columna(p.slice[1])),nodo)

def p_lista2(p):
    'lista : ID PUNTOYCOMA'
    nodo = NodoH(getIndex(),"listaposicion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(StructAtributos(p[1],None,p.lineno(1), buscar_columna(p.slice[1])),nodo)


#struct leer
def p_operacionStruct(p):
    'operacion : ID operacionstructs'
    nodo = NodoH(getIndex(),"listaposicion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    for val in p[2].nodo:
        nodo.agregar(val)
    p[0] = Nodo(OperacionStruct(p[1],p[2],p.lineno(1), buscar_columna(p.slice[1])),nodo)


def p_operacionStruct2(p):
    'operacionstructs : operacionstructs operacionstruct'
    p[1].instruccion.append(p[2].instruccion)
    nodoaux = NodoH(getIndex(),"operacionstructs",[])
    nodoaux.agregar(p[2].nodo)
    p[1].nodo.append(nodoaux)
    nodo = NodoH(getIndex(),"opreacionstruct",p[1].nodo)
    p[0]= Nodo(p[1].instruccion, [nodo] )

def p_operacionstruct3(p):
    'operacionstructs : operacionstruct'
    nodo = NodoH(getIndex(),"operacionstruct",[p[1].nodo])
    p[0] = Nodo([p[1].instruccion], [nodo])

def p_operacionstruct4(p):
    'operacionstruct : PUNTO ID'
    p[0]= Nodo(OperacionVariable(p[2], p.lineno(2), buscar_columna(p.slice[2])),NodoH(getIndex(),str(p[2]),None))


#asignacion struct

def p_asignacionstruct(p):
    'asignacion : ID operacionstructs IGUAL operacion PUNTOYCOMA'
    nodo = NodoH(getIndex(),"asignacion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    for val in p[2].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(p[4].nodo)
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(AsginacionStruc(p[1],p[2],p[4],p.lineno(1),buscar_columna(p.slice[1])),nodo)

def p_declaglobal(p):
    'asignacion : GLOBAL ID PUNTOYCOMA'
    nodo = NodoH(getIndex(),"instruccion",[])
    nodo.agregar(NodoH(getIndex(),"Global",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(Declaracionaux(p[1],p[2],p.lineno(2),buscar_columna(p.slice[2])),nodo)

def p_declalocal(p):
    'asignacion : LOCALR ID PUNTOYCOMA'
    nodo = NodoH(getIndex(),"instruccion",[])
    nodo.agregar(NodoH(getIndex(),"Local",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(Declaracionaux(p[1],p[2],p.lineno(2),buscar_columna(p.slice[2])),nodo)

    p[0] = Declaracionaux(p[1],p[2],p.lineno(2),buscar_columna(p.slice[2]))

def p_asignacion(p):
    'asignacion : ID IGUAL operacion DOBLEPUNTO tipo PUNTOYCOMA'
    nodo = NodoH(getIndex(),"instruccion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(NodoH(getIndex(),str(p[3]),None))
    nodo.agregar(NodoH(getIndex(),"::",None))
    nodo.agregar(NodoH(getIndex(),str(p[5]),None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(Declaracion(None,p[1],p[3],p[5],p.lineno(6),buscar_columna(p.slice[1])),nodo)

def p_asignacion2(p):
    'asignacion : ID IGUAL operacion PUNTOYCOMA'
    nodo = NodoH(getIndex(),"asignacion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(Declaracion(None,p[1],p[3],None,p.lineno(4),buscar_columna(p.slice[1])),nodo)

def p_asignacion5(p):
    'asignacion : LOCALR ID IGUAL operacion PUNTOYCOMA'
    nodo = NodoH(getIndex(),"asignacion",[])
    nodo.agregar(NodoH(getIndex(),"LOCALR",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(p[4].nodo)
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] =  Nodo(Declaracion(p[1],p[2],p[4],None,p.lineno(2),buscar_columna(p.slice[1])),nodo)

def p_asignacion6(p):
    'asignacion : LOCALR ID IGUAL operacion DOBLEPUNTO tipo PUNTOYCOMA'
    nodo = NodoH(getIndex(),"asignacion",[])
    nodo.agregar(NodoH(getIndex(),"LOCALR",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(p[4].nodo)
    nodo.agregar(NodoH(getIndex(),"::",None))
    nodo.agregar(NodoH(getIndex(),str(p[6]),None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(Declaracion(p[1],p[2],p[4],p[6],p.lineno(2),buscar_columna(p.slice[1])),nodo)

def p_asignacion3(p):
    'asignacion : GLOBAL ID IGUAL operacion PUNTOYCOMA'
    nodo = NodoH(getIndex(),"asignacion",[])
    nodo.agregar(NodoH(getIndex(),"GLOBAL",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(p[4].nodo)
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] =  Nodo(Declaracion(p[1],p[2],p[4],None,p.lineno(2),buscar_columna(p.slice[1])),nodo)

def p_asignacion4(p):
    'asignacion : GLOBAL ID IGUAL operacion DOBLEPUNTO tipo PUNTOYCOMA'
    nodo = NodoH(getIndex(),"asignacion",[])
    nodo.agregar(NodoH(getIndex(),"GLOBAL",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    nodo.agregar(NodoH(getIndex(),"=",None))
    nodo.agregar(p[4].nodo)
    nodo.agregar(NodoH(getIndex(),"::",None))
    nodo.agregar(NodoH(getIndex(),str(p[6]),None))
    nodo.agregar(NodoH(getIndex(),";",None))
    p[0] = Nodo(Declaracion(p[1],p[2],p[4],p[6],p.lineno(2),buscar_columna(p.slice[1])),nodo)
#funciones

def p_funciones(p):
    'funcion : FUNCTION ID PARIZQ parametros PARDER instrucciones END PUNTOYCOMA'
    nodo = NodoH(getIndex(),"instruccion",[])
    nodo.agregar(NodoH(getIndex(),"Funtion",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    nodo.agregar(NodoH(getIndex(),"(",None))
    for val in p[4].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),")",None))
    for val in p[6].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"end", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(Funcion(p[2],p[4],p[6],p.lineno(1),buscar_columna(p.slice[1])),nodo)

def p_funciones2(p):
    'funcion :  FUNCTION ID PARIZQ PARDER instrucciones END PUNTOYCOMA'
    nodo = NodoH(getIndex(),"instruccion",[])
    nodo.agregar(NodoH(getIndex(),"Funtion",None))
    nodo.agregar(NodoH(getIndex(),str(p[2]),None))
    nodo.agregar(NodoH(getIndex(),"(",None))
    nodo.agregar(NodoH(getIndex(),")",None))
    for val in p[5].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"end", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(Funcion(p[2], None,p[5], p.lineno(1),buscar_columna(p.slice[1])),nodo)

def p_parametros(p):
    'parametros : parametros COMA parametro'
    p[1].instruccion.append(p[3].instruccion)
    nodoaux = NodoH(getIndex(),"parametros",[])
    nodoaux.agregar(p[3].nodo)
    p[1].nodo.append(nodoaux)
    nodo = NodoH(getIndex(),"parametro",p[1].nodo)
    p[0]= Nodo(p[1].instruccion, [nodo] )

def p_parametros2(p):
    'parametros : parametro'
    nodo = NodoH(getIndex(),"parametro",[p[1].nodo])
    p[0] = Nodo([p[1].instruccion], [nodo])

def p_pamaretrosimple(p):
    'parametro : ID DOBLEPUNTO tipo '
    nodo = NodoH(getIndex(),"parametro",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    nodo.agregar(NodoH(getIndex(),"::",None))
    nodo.agregar(NodoH(getIndex(),str(p[3]),None))
    p[0] = Nodo(Parametros(p[1],p[3],p.lineno(1),buscar_columna(p.slice[1])),nodo)

def p_parametrossimple2(p):
    'parametro : ID '
    nodo = NodoH(getIndex(),"parametro",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    p[0] = Nodo(Parametros(p[1], None, p.lineno(1),buscar_columna(p.slice[1])),nodo)


#llamada
def p_llamada(p):
    'callfuncion : ID PARIZQ PARDER PUNTOYCOMA'
    nodo = NodoH(getIndex(),"callfuncion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    nodo.agregar(NodoH(getIndex(),"(",None))
    nodo.agregar(NodoH(getIndex(),")",None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(llamada(p[1], None, p.lineno(1),buscar_columna(p.slice[1])),nodo)

def p_llamada2(p):
    'callfuncion : ID PARIZQ valores PARDER PUNTOYCOMA'
    nodo = NodoH(getIndex(),"callfuncion",[])
    nodo.agregar(NodoH(getIndex(),str(p[1]),None))
    nodo.agregar(NodoH(getIndex(),"(",None))
    for val in p[3].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),")",None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(llamada(p[1], p[3], p.lineno(1),buscar_columna(p.slice[1])),nodo)
#nativas

def p_nativo(p):
    '''nativa   : impresion  
    '''
    p[0] = p[1]

def p_impresionVacia(p):
    '''impresion : PRINT PARIZQ  PARDER PUNTOYCOMA
                 | PRINTLN PARIZQ  PARDER PUNTOYCOMA
    '''
    nodo = NodoH(getIndex(),"impresion",[])
    nodo.agregar(NodoH(getIndex(), str(p[1]), None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(NodoH(getIndex(), ")", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(PrintCadena([p[1]], p.lineno(3),buscar_columna(p.slice[1])) , nodo)

def p_impresionSimple(p):
    '''impresion : PRINT PARIZQ valores PARDER PUNTOYCOMA
                 | PRINTLN PARIZQ valores PARDER PUNTOYCOMA
    '''
    nodo = NodoH(getIndex(),"impresion",[])
    nodo.agregar(NodoH(getIndex(), str(p[1]), None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    for val in p[3].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(), ")", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(Printval([p[1]], p[3], p.lineno(3),buscar_columna(p.slice[1])), nodo)
#sentencias

#sentencia if
def p_if(p):
    'if : IF operacion instrucciones END PUNTOYCOMA'
    s_if = SentenciaIf(p[2],p[3],p.lineno(1),buscar_columna(p.slice[1]))
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), "if", None))
    nodo.agregar(p[2].nodo)
    for val in p[3].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"end", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(If(s_if, None, None, p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_ifelse(p):
    'if : IF operacion instrucciones ELSE instrucciones END PUNTOYCOMA'
    s_if = SentenciaIf(p[2],p[3],p.lineno(1),buscar_columna(p.slice[1]))
    s_else = SentenciaIf(None, p[5],p.lineno(4),buscar_columna(p.slice[4]))
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), str(p[1]), None))
    nodo.agregar(p[2].nodo)
    for val in p[3].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),str(p[4]), None))
    for val in p[5].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),str(p[6]), None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(If(s_if, None, s_else, p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_elseif2(p): 
    'if : IF operacion instrucciones elseifaux END PUNTOYCOMA'
    s_if = SentenciaIf(p[2],p[3],p.lineno(1),buscar_columna(p.slice[1]))
    s_elif = p[4]
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), str(p[1]), None))
    nodo.agregar(p[2].nodo)
    for val in p[3].nodo:
        nodo.agregar(val)
    for val in p[4].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),str(p[5]), None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(If(s_if, s_elif, None, p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_elseif1(p):
    'elseifaux : elseifaux aux'
    p[1].instruccion.append(p[2].instruccion)
    nodoaux = NodoH(getIndex(),"elseifaux",[])
    nodoaux.agregar(p[2].nodo)
    p[1].nodo.append(nodoaux)
    nodo = NodoH(getIndex(),"aux",p[1].nodo)
    p[0]= Nodo(p[1].instruccion, [nodo] )

def p_elseif3(p):
    'elseifaux : aux'
    nodo = NodoH(getIndex(),"aux",[p[1].nodo])
    p[0] = Nodo([p[1].instruccion], [nodo])

def p_elif2(p):
    'aux : ELSEIF operacion instrucciones'
    nodo = NodoH(getIndex(),"aux",[])
    nodo.agregar(NodoH(getIndex(), str(p[1]), None))
    nodo.agregar(p[2].nodo)
    for val in p[3].nodo:
        nodo.agregar(val)
    p[0] = Nodo(SentenciaIf(p[2],p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_ifelseifelse(p):
    'if : IF operacion instrucciones elseifaux ELSE instrucciones END PUNTOYCOMA'
    s_if = SentenciaIf(p[2],p[3],p.lineno(1),buscar_columna(p.slice[1]))
    s_elif = p[4]
    s_else = SentenciaIf(None, p[6], p.lineno(5),buscar_columna(p.slice[5]))
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), str(p[1]), None))
    nodo.agregar(p[2].nodo)
    for val in p[3].nodo:
        nodo.agregar(val)
    for val in p[4].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),str(p[5]), None))
    for val in p[6].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),str(p[7]), None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(If(s_if, s_elif, s_else, p.lineno(1),buscar_columna(p.slice[1])), nodo)


#for 
def p_for(p):
    'for : FOR ID IN condicional instrucciones END PUNTOYCOMA'
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), "for", None))
    nodo.agregar(NodoH(getIndex(), p[2], None))
    nodo.agregar(p[4].nodo)
    for val in p[5].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"end", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(For(p[2], p[4], p[5], p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_condicional2(p):
    'condicional : operacion DOSPUNTOS operacion'
    nodo = NodoH(getIndex(),"condicional",[])
    nodo.agregar(p[1].nodo)
    nodo.agregar(NodoH(getIndex(), ":", None))
    nodo.agregar(p[3].nodo)
    p[0] = Nodo(condicionalRango(p[1],p[3], p.lineno(1)), nodo)


def p_condicional1(p):
    'condicional : operacion'
    nodo = NodoH(getIndex(),"condicional",[])
    nodo.agregar(p[1].nodo)
    p[0] = Nodo(condicionalSimple(p[1], p.lineno(1)), nodo)


#while 

def p_while(p):
    'while : WHILE operacion instrucciones END PUNTOYCOMA'
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), "while", None))
    nodo.agregar(p[2].nodo)
    for val in p[3].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(),"end", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(While(p[2], p[3], p.lineno(1),buscar_columna(p.slice[1])), nodo)


def p_break(p):
    'break : BREAK PUNTOYCOMA'
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), "BREAK", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(SentenciaBreak(p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_continue(p):
    'continue : CONTINUE PUNTOYCOMA'
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), "Continue", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(SentenciaContinue(p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_return(p):
    'return : RETURN operacion PUNTOYCOMA'
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), "Return", None))
    nodo.agregar(p[2].nodo)
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(SentenciaReturn(p[2],p.lineno(1),buscar_columna(p.slice[1])), nodo)


#operaicon


def p_valores(p):
    'valores : valores COMA operacion' 
    p[1].instruccion.append(p[3].instruccion)
    nodoaux = NodoH(getIndex(),"operacion",[])
    nodoaux.agregar(p[3].nodo)
    p[1].nodo.append(nodoaux)
    nodo = NodoH(getIndex(),"valores",p[1].nodo)
    p[0]= Nodo(p[1].instruccion, [nodo] )

def p_valores2(p):
    'valores : operacion'
    nodo = NodoH(getIndex(),"operacion",[p[1].nodo])
    p[0] = Nodo([p[1].instruccion], [nodo])


def p_operacionLogicas(p):
    '''operacion   : operacion AND              operacion
                   | operacion OR               operacion
    '''
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(p[1].nodo)
    nodo.agregar(NodoH(getIndex(),p[2], None))
    nodo.agregar(p[3].nodo)
    p[0] = Nodo(OperacionLogica(p[1],p[3],p[2],p.lineno(1),buscar_columna(p.slice[2])),nodo) 

def p_operacionRelacional(p):
    '''operacion    : operacion IGUALIGUAL      operacion 
                    | operacion DIFERENTE       operacion
                    | operacion MAYOR           operacion 
                    | operacion MENOR           operacion
                    | operacion MENORIGUAL      operacion
                    | operacion MAYORIGUAL      operacion
    '''
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(p[1].nodo)
    nodo.agregar(NodoH(getIndex(),p[2], None))
    nodo.agregar(p[3].nodo)
    p[0] = Nodo(OperacionRelacional(p[1],p[3],p[2],p.lineno(1),buscar_columna(p.slice[2])),nodo)  

def p_operacionAritmeticas(p):
    '''operacion    : operacion MAS             operacion
                    | operacion MENOS           operacion
                    | operacion MULTIPLICACION  operacion
                    | operacion DIVISION        operacion
                    | operacion MODULO          operacion
                    | operacion POTENCIA        operacion
    '''
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(p[1].nodo)
    nodo.agregar(NodoH(getIndex(),p[2], None))
    nodo.agregar(p[3].nodo)
    p[0] = Nodo(OperacionNumerica(p[1],p[3],p[2],p.lineno(1),buscar_columna(p.slice[2])),nodo)  

def p_operacionUnarias(p):
    '''operacion   : MENOS  operacion %prec UMENOS
                   | NOT    operacion %prec UMENOS 
    '''
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(NodoH(getIndex(),p[1], None))
    nodo.agregar(p[2].nodo)
    p[0] = Nodo(OperacionUnaria(p[2],p[1],p.lineno(1),buscar_columna(p.slice[1])),nodo) 


def p_operacionValor(p):
    'operacion : valor'
    nodo = NodoH(getIndex(),"valor",[p[1].nodo])
    p[0] = Nodo(p[1].instruccion, nodo)


def p_operacionParentesis(p):
    'operacion : PARIZQ operacion PARDER'
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[2].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(p[2].instruccion, nodo)

def p_operacionLlamada3(p):
    'operacion : ID PARIZQ valores PARDER '
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(NodoH(getIndex(), str(p[1]), None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    for val in p[3].nodo:
        nodo.agregar(val)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(llamada(p[1], p[3], p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLlamada4(p):
    'operacion : ID PARIZQ  PARDER '
    nodo = NodoH(getIndex(),"operacion",[])
    nodo.agregar(NodoH(getIndex(), str(p[1]), None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(llamada(p[1], None, p.lineno(1),buscar_columna(p.slice[1])), nodo)


#locales


def p_operacionLocal(p):
    'operacion : local'
    p[0] = p[1]

def p_operacionLocalsen(p):
    'local    : SIN PARIZQ operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "SIN", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionSen(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalcos(p):
    'local    : COS PARIZQ operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "COS", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionCos(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalTan(p):
    'local    : TAN PARIZQ operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "TAN", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionTan(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalLog10(p):
    'local    : LOG10 PARIZQ operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "LOG10", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionLog10(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalLog(p):
    'local    : LOG PARIZQ operacion COMA operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "LOG", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ",", None))
    nodo.agregar(p[5].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionLog(p[3],p[5],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalSqrt(p):
    'local    : SQRT PARIZQ operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "SQRT", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionSQRT(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalUpper(p):
    'local    : UPPERCASE PARIZQ operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "UPPERCASE", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionUPPER(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalLower(p):
    'local    : LOWERCASE PARIZQ operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "LOWERCASE", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionLOWER(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalLenght(p):
    'local    : LENGHT PARIZQ operacion PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "LENGTH", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionLenght(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocalparse(p):
    'local     : PARSE PARIZQ tipo COMA CADENA PARDER '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "PARSE", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(NodoH(getIndex(), p[3], None))
    nodo.agregar(NodoH(getIndex(), ",", None))
    nodo.agregar(NodoH(getIndex(), str(p[5]), None))
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionParse(p[3],p[5],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocaltrunc(p):
    'local     : TRUNC PARIZQ DECIMAL PARDER  '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "TRUNC", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(NodoH(getIndex(), str(p[3]), None))
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionTrunc(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)
    
def p_operacionLocalfloat(p):
    'local     : FLOAT PARIZQ ENTERO PARDER  '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "FLOAT", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(NodoH(getIndex(), str(p[3]), None))
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionFloat(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)
    
def p_operacionLocalstring(p):
    'local     : STRING PARIZQ operacion PARDER  '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "STRING", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionString(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionLocaltypeof(p):
    'local     : TYPEOF PARIZQ operacion PARDER  '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "TYPEOF", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(p[3].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionTypeof(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)

def p_operacionpush(p):
    'sentencia     : PUSH NOT PARIZQ ID COMA operacion PARDER PUNTOYCOMA '
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), "PUSH", None))
    nodo.agregar(NodoH(getIndex(), "!", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(NodoH(getIndex(), str(p[4]), None))
    nodo.agregar(p[6].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(OperacionPush(p[4],None,p[6],p.lineno(1),buscar_columna(p.slice[4])), nodo)

def p_operacionpush2(p):
    'sentencia     : PUSH NOT PARIZQ ID listaposiciones COMA operacion PARDER PUNTOYCOMA '
    nodo = NodoH(getIndex(),"sentencia",[])
    nodo.agregar(NodoH(getIndex(), "PUSH", None))
    nodo.agregar(NodoH(getIndex(), "!", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(NodoH(getIndex(), str(p[4]), None))
    for val in p[5].nodo:
        nodo.agregar(val)
    nodo.agregar(p[7].nodo)
    nodo.agregar(NodoH(getIndex(), ")", None))
    nodo.agregar(NodoH(getIndex(), ";", None))
    p[0] = Nodo(OperacionPush(p[4],p[5],p[7],p.lineno(1),buscar_columna(p.slice[1])), nodo)



def p_operacionpop(p):
    'local     : POP NOT PARIZQ ID PARDER  '
    nodo = NodoH(getIndex(),"local",[])
    nodo.agregar(NodoH(getIndex(), "POP", None))
    nodo.agregar(NodoH(getIndex(), "!", None))
    nodo.agregar(NodoH(getIndex(), "(", None))
    nodo.agregar(NodoH(getIndex(), str(p[4]), None))
    nodo.agregar(NodoH(getIndex(), ")", None))
    p[0] = Nodo(OperacionPop(p[3],p.lineno(1),buscar_columna(p.slice[1])), nodo)





#valores


#tipos y valores 
def p_tipo(p):
    '''tipo     :   INT64
                |   FLOAT64
                |   BOOL
                |   CHAR
                |   ID
                |   STRING
                |   NOTHING
    '''
    p[0] = p[1]

def p_valorInt(p):
    'valor : ENTERO'
    p[0] = Nodo(OperacionNumero(p[1], p.lineno(1), buscar_columna(p.slice[1])),NodoH(getIndex(),str(p[1]),None)) 


def p_valorID(p):
    'valor : ID'
    p[0]= Nodo(OperacionVariable(p[1], p.lineno(1), buscar_columna(p.slice[1])),NodoH(getIndex(),str(p[1]),None))


def p_valorFloat(p):
    'valor : DECIMAL'
    p[0]= Nodo(OperacionNumero(p[1], p.lineno(1), buscar_columna(p.slice[1])),NodoH(getIndex(),str(p[1]),None))


def p_valorString(p):
    'valor : CADENA'
    p[0]= Nodo(OperacionCadena("\""+p[1]+"\"", p.lineno(1), buscar_columna(p.slice[1])),NodoH(getIndex(),str(p[1]),None))


def p_valorChar(p):
    'valor : CARACTER'
    p[0]= Nodo(OperacionCaracter("\'"+p[1]+"\'", p.lineno(1), buscar_columna(p.slice[1])),NodoH(getIndex(),str(p[1]),None))


def p_valorFalse(p):
    'valor : TRUE'
    p[0]= Nodo(OperacionBooleana(p[1], p.lineno(1), buscar_columna(p.slice[1])),NodoH(getIndex(),str(p[1]),None))


def p_valorTrue(p):
    'valor : FALSE'
    p[0]= Nodo(OperacionBooleana(p[1], p.lineno(1), buscar_columna(p.slice[1])),NodoH(getIndex(),str(p[1]),None))

def p_valorNulo(p):
    'valor : NOTHING'
    p[0]= Nodo(OperacionNULO(p[1],p.lineno(1), buscar_columna(p.slice[1])),NodoH(getIndex(),str(p[1]),None))

input = ""
parser = yacc.yacc(write_tables = True)

def parse(inpu):
    global indice
    global parser
    global input
    lexer = lex.lex(reflags= re.IGNORECASE)
    lexer.lineno = 0
    return parser.parse(inpu, lexer=lexer)

def restart():
    global parser
    global indice 
    indice = 0
    parser.restart()

def buscar_columna(token):
    line_start = input.rfind('\n', 0, token.lexpos)+1
    return (token.lexpos - line_start)+1
