#!/usr/bin/python
# -*- coding: utf-8 -*-

from operator import attrgetter
from collections import namedtuple
import time
import random

Node = namedtuple("Node", ['node','neborCount', 'prohibCount', 'prohibited', 'nebors', 'toDo' ])
Sol = namedtuple("Sol", ['node', 'color'])
finSol = namedtuple("finSol", ['nCol', 'sol'])

start = time.clock()
#  -----------------========= CUSTOM FUNCTIONS ==========---------------------
def setColor(nodes, solution, colors, currLoop):
    nodes = sorted(nodes, key=attrgetter('toDo', 'neborCount', 'prohibCount'), reverse=True)
    
    if currLoop < 5:
        tempNodes = []
        for i in range(0, len(nodes)):
            if nodes[i].toDo == 1:
                tempNodes.append(Node(nodes[i].node, nodes[i].neborCount, nodes[i].prohibCount, nodes[i].prohibited, nodes[i].nebors, nodes[i].toDo))    
        
        currNode = random.choice (tempNodes)
    else: currNode = nodes[0]

#     nodes = sorted(nodes, key=attrgetter('toDo'), reverse=True)
#     print nodes[0].node
#     print nodes
    
    #------------ Colors Management-----------------------------
    if currNode.prohibited != None:
        col_opt = list(set(colors) -  set(currNode.prohibited))
        if len(col_opt) == 0 :
            color = len(colors)
            colors.append(color)
#         else: color = col_opt[0]
        else: color = random.choice (col_opt)
    else : 
        col_opt = colors
#         color = col_opt[0]
        color = random.choice (col_opt)
    #-----------------------------------------------------------
    
    solution.append(Sol(currNode.node, color))
    toUpdate = [] #-----------Array of nodes to be updated  
    nodes1 = sorted(nodes, key=attrgetter('node'))
    for i in range(0, currNode.neborCount):
        j = currNode.nebors[i]  
    
        prohib = []
        prohibCnt = 0
#         if j != 0: 
        if nodes1[j].prohibited != None :
            prohibCnt+= nodes1[j].prohibCount
            for k in range(0, len(nodes1[j].prohibited)):
                prohib.append(nodes1[j].prohibited[k])
        if color not in prohib :
            prohibCnt+= 1
            prohib.append(color)        
                    
        newNeborCount = nodes1[j].neborCount - 1
        newNebors = list(set(nodes1[j].nebors) - set([currNode.node]))
                
        
        toUpdate.append(Node(nodes1[j].node, nodes1[j].neborCount, prohibCnt, prohib, nodes1[j].nebors, nodes1[j].toDo))
    #-----------------------------------------------------------  
    
    for i in range(0, len(nodes1)):
        for j in range(0, len(toUpdate)):
            if nodes1[i].node == toUpdate[j].node :
                del nodes1[i]
                nodes1.append(Node(toUpdate[j].node, toUpdate[j].neborCount, toUpdate[j].prohibCount, toUpdate[j].prohibited, toUpdate[j].nebors, toUpdate[j].toDo))         
    
    for j in range(0, len(nodes1)) :        
        if nodes1[j].node == currNode.node:
            nodes1.append(Node(nodes1[j].node, nodes1[j].neborCount, nodes1[j].prohibCount, nodes1[j].prohibited, nodes1[j].nebors, 0))
            del nodes1[j]
    
    nodes = nodes1
    colors = colors
    
#     nodes3 = sorted(nodes, key=attrgetter('toDo'), reverse=True)
#     nodes3 = sorted(nodes, key=attrgetter('toDo', 'neborCount', 'prohibCount'), reverse=True)

#     print len(nodes1)
#     print nodes3[0].node
#     print nodes1
#     print toUpdate
#     print "col opt: " + str(col_opt)
#     print "col : " + str(color)
#     print "prohib : " + str(prohib)
#     print "solution : " + str(len(solution))
    
    result = []
    result.append(nodes)
    result.append(solution)
    result.append(colors)
    
    return result
    
    
#  -----------------========= CUSTOM FUNCTIONS END ==========---------------------


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # my SOLUTION ***********************************************************
    finalSol = []
    probables = range(0, node_count)
    for k in range(0, 10):
        solution = []
        colors = []
        colors.append(0)
        colors.append(1)
        nodes = []
#         nebor_coll = []   # collects neighbors
        for i in range(0, node_count):
            indEdgeCount = 0
            nebors = []
            for j in range(0, edge_count):            
                if edges[j][0] == i :
                    indEdgeCount+= 1
                    nebors.append(edges[j][1])
                if edges[j][1] == i :
                    indEdgeCount+= 1
                    nebors.append(edges[j][0])
#             nebor_coll.append((i, indEdgeCount, nebors))
            prohib = None
            nodes.append(Node(i, indEdgeCount, 0, None, nebors, 1))
            
        
        for i in range(0, node_count):
            resSetCol = setColor(nodes, solution, colors, i)
            nodes = resSetCol[0]
            solution = resSetCol[1]      
            colors = resSetCol[2]          
        
        solution = sorted(solution, key=attrgetter('node'))
        soltemp = []
        for i in range(0, len(solution)):
            soltemp.append(solution[i].color)
#         solution = range(0, node_count)
        solution = soltemp
        nCols = len(colors)
        
        finalSol.append(finSol(nCols, solution))
        
    finalSol = sorted(finalSol, key=attrgetter('nCol'))

    # prepare the solution in the specified output format
    output_data = str(finalSol[0].nCol) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, finalSol[0].sol))
#     output_data += str(solution)
    
        
#     print finalSol
#     print nebor_coll
#     print nodes
#     print "colors: " + str(colors)
#     print soltemp
#     print 170 in nebor_coll[0][2]
#     print nodes1
    return output_data


import sys

if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         file_location = sys.argv[1].strip()
#         input_data_file = open(file_location, 'r')
#         input_data = ''.join(input_data_file.readlines())
#         input_data_file.close()
#         print solve_it(input_data)
#     else:
#         print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

#  ----------- to be commented out before submission ----------------- 
    input_data_file = open('./data/gc_20_5', 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()
    print solve_it(input_data)
    