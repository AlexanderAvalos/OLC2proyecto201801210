import subprocess

class GraficarArbol():
    def __init__ (self, args=()):
        self.nodo = args[0]
        self.file = ""
    def run(self):
        self.file = self.ConstruirAST(self.nodo)    
        return self.file
    
    def cmd(self,comando):
        subprocess.run(comando,shell =True)

    def ConstruirAST(self, nodo):
        try:
            self.file = self.file +("digraph{ \n")
            self.imprimirnodos(nodo.nodo,self.file)
            self.graficar(nodo.nodo,self.file)
            self.file = self.file +("\n}")
        except:
            print("Error")
        finally:
            return self.file

    def imprimirnodos(self, nodo,file):
        self.file = self.file +(str(nodo.indice) + "[style = \"filled\"; label = \""+nodo.nombre+"\"]\n")
        if nodo.hijos != None:
            for hijo in nodo.hijos:
                self.imprimirnodos(hijo, self.file)
    
    def graficar(self,nodo,file):
        if nodo.hijos != None:
            for hijo in nodo.hijos:
                self.file = self.file +(str(nodo.indice)+ " -> " + str(hijo.indice)+ " ; \n")
                self.graficar(hijo,self.file)
