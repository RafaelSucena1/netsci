#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 11:59:34 2022

@title: Erdos-Renyi Model
@author: Rafael Sucena
"""
import random
import matplotlib.pyplot as plt

class Graph:
    edges = {}
    n = 0
    p = 0
    
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.degrees = [0] * n
        
    def addEdge(self, i, j):
        self.edges[i].append(j)
    
    def __initializeNode(self, i):
        self.edges[i] = []
        
    def clear(self):
        self.edges.clear()
        
    def __yes(self):
        return random.uniform(0, 1) > self.p
    
    def update(self):
        for i in range(1, self.n + 1):
            self.__initializeNode(i)
            for j in range(1, i):
                if self.__yes(): 
                    self.degrees[i] = self.degrees[i] + 1
                    self.degrees[j] = self.degrees[j] + 1
                    self.addEdge(i, j)                    
                    
    def printG(self):
        for start in self.edges.keys():
            for end in self.edges[start]:
                print(str(start) + " " + str(end))
                
                
    def plotDegree(self):
        plt.bar(range(1, self.n), self.degrees)
  
    def plotNumberNodesWithK(self):
        Ks = [0] * self.n
        for i in range(1, self.n + 1):
            Ks[self.degrees[i]] = Ks[self.degrees[i]] + 1
        plt.bar(range(0, self.n), Ks)

       





        
graph = Graph(100, 0.9)
graph.update()

graph.printG()

                    
                    
                
