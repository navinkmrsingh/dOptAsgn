#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from operator import attrgetter
from collections import namedtuple
import time

Item = namedtuple("Item", ['index', 'value', 'weight', 'valueDensity'])
Node = namedtuple("Node", ['node', 'value', 'room', 'estimate'])

start = time.clock()
#  -----------------========= CUSTOM FUNCTIONS ==========---------------------
def evaluateNode(nodes, node, items):
    taken = node.node.split()
    nodeLength = len(taken)
    node1 = str(node.node) + ' 1'
    node1value = node.value + items[nodeLength].value
    node1room = node.room - items[nodeLength].weight
    if node1room >= 0 :
        nodes.append(Node(node1, node1value, node1room, node.estimate))
#         print 'Created: ' + node1
#     else:
#         print 'discarded: ' + node1
    
    
    node0 = str(node.node) + ' 0'
    node0estimate = node.estimate - items[nodeLength].value    
    nodes.append(Node(node0, node.value, node.room, node0estimate))
#     print 'Created: ' + node0
    
    return nodes

def delNode(nodes, node):
    nodesTemp = []
    for nodeElement in nodes:
        if (nodeElement.node != node.node):
            nodesTemp.append(nodeElement)
    nodes = nodesTemp
#     print 'Deleted: ' + node.node
    return nodes

def expandNode(nodes, node, items):
    nodes = evaluateNode(nodes, node, items)
    nodes = delNode(nodes, node)
    return nodes
#  -----------------========= CUSTOM FUNCTIONS END ==========---------------------





def solve_it(input_data):
    # ----------Modify this code to run your optimization algorithm

    # ----------parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    estimate = 0

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), (int(parts[0])/int(parts[1]))))
        estimate+= int(parts[0])
        
#     print(sorted(items, key=attrgetter('valueDensity'), reverse=True))
#     items = sorted(items, key=attrgetter('valueDensity'), reverse=True)

    # ----------a trivial greedy algorithm for filling the knapsack
    # ----------it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)
# 
#     for item in items:
#         if weight + item.weight <= capacity:
#             taken[item.index] = 1
#             value += item.value
#             weight += item.weight

    # ----------mySOLUTION
    nodes = []
    room = capacity - items[0].weight
    newEstimate = estimate - items[0].value
    nodes.append(Node(str(1), items[0].value, room, estimate))
    nodes.append(Node(str(0), 0, capacity, newEstimate))
    
    repeat = 1
    itr = 0
    lastNode = nodes[1].node
    
    while repeat != 0:
        nodes = sorted(nodes, key=attrgetter('estimate'), reverse=True)
        if nodes[0].node == lastNode :
            repeat = 0
            break
        
        length = nodes[0].node.split()
        length = len(length)
        if length == item_count :
            break 
        
        elapsed = (time.clock() - start)
        if elapsed >= 17880:
            nodes = sorted(nodes, key=attrgetter('value'), reverse=True)
            break
#         print 'time: ' + str(elapsed)
            
        lastNode = nodes[0].node
        nodes = expandNode(nodes, nodes[0], items)
        
        itr+= 1
#         print itr
#         print nodes[0]
#         print 'Total # of Nodes: ' + str(len(nodes))
    
    value = nodes[0].value
    taken = nodes[0].node
        
    
    
    # -----------prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += taken
#     output_data += ' '.join(map(str, taken))
    return output_data

    

import sys 

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()        
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'


#  ----------- to be commented out before submission ----------------- 
#     input_data_file = open('./data/ks_100_0', 'r')
#     input_data = ''.join(input_data_file.readlines())
#     input_data_file.close()
#     print solve_it(input_data)
 
    
