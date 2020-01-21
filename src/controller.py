#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

# Esta classe manipula todos os principais recursos do programa
class Control():
    def __init__(self, interval, cicles, intensity, path, point):
        self.interval = interval        # Intervaalo de tempo (em dias) em que se salva a saáda
        self.cicles = cicles*interval   # Numero de dias de poluição
        self.intensity = intensity      # Intensidade do poluente
        self.path = path                # Caminho da malha da ilha
        self.point = point              # Foco do poluente

        importedMap = self.importMap()
        self.lines = importedMap[0]     # Numero de linhas da malha
        self.columns = importedMap[1]   # Numero de colunas na malha
        self.MAP = importedMap[2]       # Mapa da ilha
        self.cMap = [[0.0]*self.columns for i in range (0,self.lines)] # Mapa de concentração de poluente
        self.cache = []                 # Aramzena os mapas de concetração da saida
        self.y = int(self.point[0])
        self.x = int(self.point[1])
        try:
            self.cMap[self.y][self.x] = intensity
            self.main()
        except IndexError:
            print("Esse ponto esta fora da malha.")
            exit()

    # Método responsável por atualizar os status da saída
    def main(self):
        self.saveMap("poluente_t_000.txt")
        for cicle in range(1, self.cicles+1):
            self.cMap = self.calculateDispersion()
            
            if(cicle%self.interval == 0):
                name = "poluente_t_{:003d}.txt".format(cicle)
                self.saveMap(name)

    # Método para calcular o mapa de concentração de poluente {Complexidade O(n2)}
    def calculateDispersion(self):
        cacheMap = self.cacheMesh(self.cMap)    # Copia do mapa de concentração
        for i in range(0, self.lines):
            for j in range (0, self.columns):
                if((self.y, self.x) == (i, j)):
                    continue
                self.cMap[i][j] = self.C(cacheMap, (i, j))
        return self.cMap

    # Importa a malha que contém o mapa {Complexidade O(n)}
    # Entrada: Caminho do arquivo que contém a malha
    # Saida: Matriz que descreve o mapa bem como seu 
    # número de linhas e colunas.
    def importMap(self):
        self.lines = 0   # Número de linhas da malha
        self.columns = 0 # Número de colunas da malha 
        
        mapFile = open(self.path)
        myMap = mapFile.readlines()
        mapFile.close()
        
        lines = int(myMap[0].strip())
        columns = int(myMap[1].strip())
        
        myMap.pop(0)
        myMap.pop(0)
        
        for i in range (0, lines):
            myMap[i] = myMap[i].strip().split('\t')
        
        return (lines, columns, myMap)

    # Este método salva a saida do porgram
    # Entrada: Nome do arquivo
    # Saída: Arquivo com as concentrações de um determidado estágio da simulação
    def saveMap(self, name):
        self.cache.append(self.cMap)
        string = ""                 # String para armazenar o conteúdo da saída
        newpath = r'./outfiles'     # Pasta de destino da saída
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        try:
            fmap = open("outfiles/"+name, "w")
            for i in range(0, self.lines):
                for j in range(0, self.columns):
                    string += "{: .1f}".format(self.cMap[i][j])
                    if(j != self.columns-1):
                        string += '\t'
                if(i != self.lines-1):
                    string += '\n'
            fmap.write(string)
            fmap.close()
            print("{} foi salvo com sucesso.".format(name))
            return 1
        except:
            print ("Erro: Falha ao salvar o arquivo {}".format (name))
            return 0
            
    # Método para calcular concentração de um poluente num ponto {Complexidade O(1)}
    # Entrda: Mapa de Concentração, ponto onde vai ser calculada a nova concentração
    # Numero de linhas e colunas da malha
    # Saida: Valor da concentação de um ponto
    def C(self, cMap, point):
        ciless = 0.0
        cimore = 0.0
        cjless = 0.0
        cjmore = 0.0
        
        if(point[0] > 0):
            ciless = cMap[point[0]-1][point[1]]
        if(point[0] < self.lines-1):
            cimore = cMap[point[0]+1][point[1]]
        if(point[1] > 0):
            cjless = cMap[point[0]][point[1]-1]
        if(point[1] < self.columns-1):
            cjmore = cMap[point[0]][point[1]+1]
            
        out = (ciless + cjless + cimore + cjmore)/4
        
        return out

    # Cria copia do mapa de concentrações para servir de nova referência
    def cacheMesh(self, mesh):
        newMesh = [[0]*self.columns for i in range (0,self.lines)] # Mapa de concentração de poluente
        
        for i in range (0, self.lines):
            for j in range (0, self.columns):
                newMesh[i][j] = mesh[i][j]
        
        return newMesh