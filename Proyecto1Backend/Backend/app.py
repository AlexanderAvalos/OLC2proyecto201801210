import sys
sys.path.insert(1, './analizador')
import Gramatica as g
import GramaticaAST as gast
import AST as ast
import interprete as inter
import ts as TS
from flask import Flask,request,jsonify 
from flask_cors import CORS 
salida = ""
interpre = []

app = Flask(__name__)
CORS(app)



@app.route('/serv/ast', methods = ['POST'])
def recibir2():
    astsa = ""
    data = request.json
    input = data['valor']
    nodo = gast.parse(input)
    graficar = ast.GraficarArbol(args=(nodo,"AST"))
    astsa = graficar.run()
    gast.restart()
    return  astsa



@app.route('/serv/simbolo',methods = ['GET'])
def TablaSimbolo():
    aux = ""
    if len(interpre) > 0:
        for val in interpre:
            aux = val.graficar()
        interpre.remove(val);
        print(aux)
    return aux 


@app.route('/serv/error', methods = ['GET'])
def tablaError():
    aux = ""
    if len(interpre) > 0:
        for val in interpre:
            aux = val.graficarErrores()
        interpre.remove(val);
    else:
        print("error al crear grafica")   
    print(aux)
    return aux

@app.route('/serv', methods = ['POST'])
def recibir():
    data = request.json
    input = data['valor']
    Instruccion = g.parse(input)
    ts_global = TS.TablaSimbolos()
    funciona = inter.interprete(Instruccion,ts_global)
    funciona.run(Instruccion)
    interpre.append(funciona)
    salida = funciona.salida
    
    return  salida

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)