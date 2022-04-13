#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:09:08 2022

@author: zed
"""

import fileinput
import random

class Vertex:

    def __init__(self):
        self.__index = None
        self.__lowlink = None
        self.__edges = []
        self.__onStack = False

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
    __vertices = {}
    __edges = set()

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
        """
        print("i: %d, j: %d" %(index_i, index_j))
        """
        vertex_i = self.__vertices[index_i]
        vertex_j = self.__vertices[index_j]
        edge = Edge(vertex_i, vertex_j)
        vertex_i.addEdge(edge)
        self.__edges.add(edge)



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
                print("in index: %d" % (index))
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





if __name__ == '__main__':
    graph = Graph()
    graph.importGraph("random1.txt")
    graph.tarjan()
    x = 2

    """
    take care:
     -> vertex: lowlink
    """