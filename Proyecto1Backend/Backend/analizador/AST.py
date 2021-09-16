import subprocess

class GraficarArbol():
    def __init__ (self, args=()):
        self.nodo = args[0]
    
    def run(self):
        self.ConstruirAST(self.nodo)    
    
    def cmd(self,comando):
        subprocess.run(comando,shell =True)

    def ConstruirAST(self, nodo):
        ruta = "arbol.dot"
        comando = "dot -Tpng arbol.dot -o arbol.png"
        try:
            file = open(ruta,"w")
            file.write("digraph{ \n")
            self.imprimirnodos(nodo.nodo,file)
            self.graficar(nodo.nodo,file)
            file.write("\n}")
            file.close()
        except:
            print("Error")
        finally:
            self.cmd(comando)

    def imprimirnodos(self, nodo,file):
        file.write(str(nodo.indice) + "[style = \"filled\"; label = \""+nodo.nombre+"\"]\n")
        if nodo.hijos != None:
            for hijo in nodo.hijos:
                self.imprimirnodos(hijo, file)
    
    def graficar(self,nodo,file):
        if nodo.hijos != None:
            for hijo in nodo.hijos:
                file.write(str(nodo.indice)+ " -> " + str(hijo.indice)+ " ; \n")
                self.graficar(hijo,file)
