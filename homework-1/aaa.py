import fileinput
import random
import matplotlib.pyplot as plt
import pylab
from numpy import log as ln
import numpy as np

class Graph:
    _totalDegrees = 0
    __n = 0
    __m = 0
    __vertices = {}

    class Vertex:
        def __init__(self, outer, index):
            self.__index = index
            self.outer = outer
            self.__edges = []
            self.__degree = 0

        def nextVertices(self):
            vertices = []
            for edge in self.__edges:
                vertices.append(edge.end())
            return vertices

        def addEdge(self, edge):
            if not edge in self.__edges:
                self.__edges.append(edge)

        def getIndex(self):
            return self.__index

        def setIndex(self, index):
            self.__index = index

        def increaseDegree(self):
            self.__degree = self.__degree + 1
            self.outer._totalDegrees = self.outer._totalDegrees + 1

        def getDegree(self):
            return self.__degree

    class Edge:
        def __init__(self, start, end):
            self.__start = start
            self.__end = end
            start.increaseDegree()
            end.increaseDegree()

        def end(self):
            return self.__end

        def start(self):
            return self.__start

    def __init__(self, n, m0, m):
        self.__n = n
        self.__m = m
        self.__m0 = m0
        if n < m0 or n < m:
            raise Exception('invalid parameters')
        self.__createClique(m0)
        self.__fillGraph()

    """
    keeps adding new vertices until n
    imagine the degrees of the vertices as spaces on a line
    we get at random a number between zero and the total sum
    the value it lands on determines the node
    """

    def __fillGraph(self):
        for i in range(self.__m0 + 1, self.__n + 1):
            vtx = Graph.Vertex(self, i)
            self.__vertices[i] = vtx
            for j in range(0, self.__m):
                cumulative = random.uniform(0, self._totalDegrees)
                sum = 0
                for vtxr in self.__vertices.values():
                    sum = sum + vtxr.getDegree()
                    if sum > cumulative:
                        self.__addEdge(i, vtxr.getIndex())
                        break

    """
    the purpose of this function is to create the initial
    connections , by definition connecting all n nodes
    """

    def __createClique(self, m0):
        for i in range(1, m0 + 1):
            self.__vertices[i] = Graph.Vertex(self, i)

        for i in range(1, m0 + 1):
            for j in range(1, i):
                if self.__yes():
                    self.__addEdge(i, j)
                else:
                    self.__addEdge(j, i)

    """
    this function just returns True with probability 0.5
    False otherwise
    """

    def __yes(self):
        return random.uniform(0, 1) < 0.5

    """
    helper function for the import of the edges
    it accepts two indexes: for the two vertices
    and adds an edge to the graph
    """

    def __addEdge(self, index_i, index_j):
        vertex_i = self.__vertices[index_i]
        vertex_j = self.__vertices[index_j]
        if self.__yes():
            edge = Graph.Edge(vertex_i, vertex_j)
            vertex_i.addEdge(edge)
        else:
            edge = Graph.Edge(vertex_j, vertex_i)
            vertex_j.addEdge(edge)

    def printG(self):
        for start in self.__vertices.values():
            for end in start.nextVertices():
                print("%d %d" % (start.getIndex(), end.getIndex()))

    """
    notice that no node is connected to less than m other nodes
    """
    def getAlpha(self):
        degrees = [vtx.getDegree() for vtx in self.__vertices.values()]
        sum = 0
        n   = len(degrees)
        for i in range(0, len(degrees)):
            sum = sum + ln(degrees[i] / self.__m)
        alpha = 1 + n / sum
        return alpha

    def frequencyBinning(self):
        degrees = [vtx.getDegree() for vtx in self.__vertices.values()]
        dg = [0] * len(degrees)
        for i in range(0, len(degrees)):
            dg[i] = sum(j > degrees[i] for j in degrees)
        x_data = np.array(degrees)
        y_data = np.array(dg)
        log_x_data = np.log(x_data)
        log_y_data = np.log(y_data + 1)
        curve_fit = np.polyfit(log_x_data, log_y_data, 1)
        fig = plt.figure()
        plt.title("By frequency binning", fontsize=18)
        plt.xlabel('x', fontsize=18)
        plt.ylabel('frequency sample > x', fontsize=16)
        ax = plt.gca()
        ax.plot(degrees, dg, 'o', c='blue', markeredgecolor='none', label="data")
        ax.set_yscale('log')
        ax.set_xscale('log')
        poly = np.poly1d(curve_fit)
        yfit = lambda x: np.exp(poly(np.log(x)))
        plt.loglog(degrees, yfit(degrees), c="red",  label='alpha - 1 = ' +str("%f.2" %(curve_fit[0])))
        plt.legend()
        plt.grid(True)
        pylab.savefig("./frequency_binning2.png")
        pylab.show()

    def printG(self):
        for start in self.__vertices.values():
            for end in start.nextVertices():
                print("%d %d" % (start.getIndex(), end.getIndex()))


if __name__ == '__main__':
    graph = Graph(2000, 3, 1)
    graph.printG()
