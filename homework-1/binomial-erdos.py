#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 11:59:34 2022

@title: Erdos-Renyi Model
@author: Rafael Sucena
"""
import random
import matplotlib.pyplot as plt


class Vertex:
    def __init__(self, index):
        self.__index = index
        self.__edges = []

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
            vtx = Vertex(i)
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
        else:
            edge = Edge(vertex_j, vertex_i)
            vertex_j.addEdge(edge)

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


if __name__ == '__main__':
    graph = Graph(0.09, 100)
    graph.printG()
