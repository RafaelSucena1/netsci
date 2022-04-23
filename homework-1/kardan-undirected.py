#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:09:08 2022

@author: zed
"""

import fileinput

import matplotlib.pyplot as plt
import numpy
import random
import sys

class Vertex:

    def __init__(self):
        self.__index = None
        self.__lowlink = None
        self.__edges = []
        self.__onStack = False

    def nextVertices(self):
        vertices = []
        for edge in self.__edges:
            if edge.end() == self:
                vertices.append(edge.start())
            else:
                vertices.append(edge.end())
        return vertices

    def addEdge(self, edge):
        if not edge in self.__edges:
            self.__edges.append(edge)

    def getIndex(self):
        return self.__index

    def setIndex(self, index):
        self.__index = index

    def setOnStack(self, onStack):
        self.__onStack = onStack

    def getOnStack(self):
        return self.__onStack

    def setLowLink(self, lowLink):
        self.__lowlink = lowLink

    def getLowLink(self):
        return self.__lowlink

class Edge:
    def __init__(self, start, end):
        self.__start = start
        self.__end = end

    def end(self):
        return self.__end

    def start(self):
        return self.__start

class Graph:
    __n = 0
    __p = 0
    __vertices = {}

    """
    helper function for the import of the graph
    it initializes the dictionary of vertices
    """

    def __prepareVertices(self):
        for i in range(1, self.__n + 1):
            vtx = Vertex()
            self.__vertices[i] = vtx

    """
    helper function for the import of the edges
    it accepts two indexes: for the two vertices
    and adds an edge to the graph
    """

    def __addEdge(self, index_i, index_j):
        vertex_i = self.__vertices[index_i]
        vertex_j = self.__vertices[index_j]
        if random.uniform(0, 1) < 0.5:
            edge = Edge(vertex_i, vertex_j)
            vertex_i.addEdge(edge)
            vertex_j.addEdge(edge)
        else:
            edge = Edge(vertex_j, vertex_i)
            vertex_j.addEdge(edge)
            vertex_i.addEdge(edge)


    def __yes(self):
        return random.uniform(0, 1) < self.__p

    def __init__(self, p, n):
        self.__n = n
        self.__p = p
        self.__prepareVertices()
        for i in range(1, self.__n + 1):
            for j in range(1, i):
                if self.__yes():
                    self.__addEdge(i, j)

    def printG(self):
        for start in self.__vertices.values():
            for end in start.nextVertices():
                print("%d %d" % (start.getIndex(), end.getIndex()))


    """
    given the name of the file it will import graph
    first line must be the number of nodes
    subsequent lines have two numbers separated
    by a -space- these two numbers are the indexes of 
    the vertices of the edge we are currently adding
    """
    def importGraph(self, file):
        firstLoop = True
        finput = fileinput.input(file)
        for line in finput:
            if firstLoop:
                line.rstrip()
                self.__n = int(line)
                self.__prepareVertices()
                firstLoop = False
            else:
                line.rstrip()
                i, j = line.split(" ")
                i = int(i)
                j = int(j)
                self.__addEdge(i, j)
        finput.close()

    def tarjan(self):
        for (index, vertex) in self.__vertices.items():
            if vertex.getIndex() is None:
                self.__strongConnect(vertex)


    __stack = []
    __index = 0
    __connectedComponents = []

    def __strongConnect(self, vertex):
        vertex.setIndex(self.__index)
        vertex.setLowLink(self.__index)
        self.__index = self.__index + 1

        self.__stack.append(vertex)
        vertex.setOnStack(True)

        for w in vertex.nextVertices():
            if w.getIndex() is None:
                self.__strongConnect(w)
                lowLink = min(vertex.getLowLink(), w.getLowLink())
                vertex.setLowLink(lowLink)
            else:
                if w.getOnStack():
                    lowLink = min(vertex.getLowLink(), w.getIndex())
                    vertex.setLowLink(lowLink)

        if vertex.getLowLink() == vertex.getIndex():
            newSCC = []

            while len(self.__stack) != 0:
                w = self.__stack.pop()
                w.setOnStack(False)
                newSCC.append(w)
                if w is vertex:
                    break

            self.__connectedComponents.append(newSCC)


    def printStats(self):
        print("Number of SCCs: %d" % (len(self.__connectedComponents)))

    def testSCC(self):
        nInSccs = 0
        for scc in self.__connectedComponents:
            nInSccs = nInSccs + len(scc)
        print("the number of elements in the comonents is " + " to the number of vertices")

    def getConnectedComponentsSize(self):
        sizes = [len(x) for x in self.__connectedComponents]
        return sizes

    def getSizeGiantComponent(self):
        self.tarjan()
        return max(self.getConnectedComponentsSize())


def getSizesGiantComponents():
    n = 2000

    sizes = []
    p_    = []

    for p in numpy.arange(0.0001, 0.005, 0.0001):
        graph = Graph(p, n)
        sizes.append(graph.getSizeGiantComponent())
        p_.append(p)

    plt.plot(p_, sizes)
    plt.xlabel("p")
    plt.ylabel("Size largest SCC")
    plt.savefig("Size giant component")
    plt.show()

if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    getSizesGiantComponents()
