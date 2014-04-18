#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from operator import itemgetter
import time
import itertools

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

start = time.clock()
#  --------------------========= CUSTOM FUNCTIONS ==========----------------------
def sign(n):
    sign = 0
    if n < 0 : sign = -1
    if n > 0 : sign = 1
    return sign


def midPoint(A, B):
    x = (A.x + B.x)/2
    y = (A.y + B.y)/2
    return [x, y]

    
def pseudoLength(point1, point2):
    return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def basicSol(solution, enrouted, points, nodeCount):
    dist = []
    lastPoint = solution[-1]
    remLen = nodeCount - len(solution) # no of remaining points
    enrouted = sorted(enrouted, key=itemgetter(1), reverse=True)
    
    for i in range(0, remLen):
        point1 = points[lastPoint] 
        point2 = points[enrouted[i][0]]
        
        dist.append([enrouted[i][0], pseudoLength(point1, point2)])
    
    dist = sorted(dist, key=itemgetter(1))
    solution.append(dist[0][0])
    
    index = dist[0][0]
    enrouted = sorted(enrouted, key=itemgetter(0)) 
    enrouted[index][1] = 0
    
    
def checkIntersection(A, B, C, D):
    intersect = 0
    Px = midPoint(A, B)[0]
    Py = midPoint(A, B)[1]
    Qx = midPoint(C, D)[0]
    Qy = midPoint(C, D)[1]
    
    ACP = ((Py-C.y)*(A.x-C.x)) - ((A.y-C.y)*(Px-C.x))
    ACQ = ((Qy-C.y)*(A.x-C.x)) - ((A.y-C.y)*(Qx-C.x))
    ADP = ((Py-D.y)*(A.x-D.x)) - ((A.y-D.y)*(Px-D.x))
    ADQ = ((Qy-D.y)*(A.x-D.x)) - ((A.y-D.y)*(Qx-D.x))
    
    BCP = ((Py-C.y)*(B.x-C.x)) - ((B.y-C.y)*(Px-C.x))
    BCQ = ((Qy-C.y)*(B.x-C.x)) - ((B.y-C.y)*(Qx-C.x))
    BDP = ((Py-D.y)*(B.x-D.x)) - ((B.y-D.y)*(Px-D.x))
    BDQ = ((Qy-D.y)*(B.x-D.x)) - ((B.y-D.y)*(Qx-D.x))
    
    if BCP != 0 and BDQ != 0:
        if sign(ACP) == sign(ACQ) and sign(ADP) == sign(ADQ) and sign(BCP) == sign(BCQ) and sign(BDP) == sign(BDQ) : intersect = 1
    return intersect


def twoOptMachine(solA, solB, solC, solD, solution, points):

    sol1 = solution[:solution.index(solA)+1]
    sol2 = solution[solution.index(solB):solution.index(solC)+1]
    sol2 = sol2[::-1]
    sol3 = solution[solution.index(solD):]
    
    solution = sol1 + sol2 + sol3
    
    return solution

    
def twoOpt(solution, points, nodeCount):
    intersectCount = 0
    for i in range(0, nodeCount-1):
        solA = solution[i]
        solB = solution[i+1]
        A = points[solA]
        B = points[solB]
         
        for j in range(i+2, nodeCount-1):
            solC = solution[j]
            solD = solution[j+1]
            
            C = points[solC]
            D = points[solD]
            intersect = checkIntersection(A, B, C, D)
             
            if intersect == 1:
                solution = twoOptMachine(solA, solB, solC, solD, solution, points)
                intersectCount+= 1
                break
#          solution = solution1
    result = []
    result.append(solution)
    result.append(intersectCount)    
    print len(solution)
    return result

    
def twoOptRevMachine(solC, solD, solA, solB, solution, points):

    sol1 = solution[:solution.index(solC)+1]
    sol2 = solution[solution.index(solD):]
    sol2 = sol2[::-1]
#     sol3 = solution[solution.index(solD):]
    
    solution = sol1 + sol2
    
    return solution

    
def twoOptRev(solution, points, nodeCount):
    intersectCount = 0
    
    solA = solution[-1]
    solB = solution[0]
     
    for j in range(1, nodeCount-2):
        solC = solution[j]
        solD = solution[j+1]
        A = points[solA]
        B = points[solB]
        C = points[solC]
        D = points[solD]
        intersect = checkIntersection(C, D, A, B)
         
        if intersect == 1:
            solution = twoOptRevMachine(solC, solD, solA, solB, solution, points)
            intersectCount+= 1
            break
#     solution = solution1
    result = []
    result.append(solution)
    result.append(intersectCount)    
    print len(solution)
    return result       


def threeOptMachine(solA, solB, solC, solD, posE, solution, points):
    sol1 = solution[:solution.index(solA)+1]
    sol2 = solution[solution.index(solD):posE+1]
    sol3 = solution[solution.index(solB):solution.index(solC)+1]
    sol3 = sol3[::-1]
    sol4 = solution[posE+1:]
    
    solution = sol1 + sol2 + sol3 + sol4     
    
    return solution

    
def threeOpt(solution, points, nodeCount):
    repeat = 0
    for i in range(0, nodeCount-1):
        solA = solution[i]
        solB = solution[i+1]
        
        A = points[solA]
        B = points[solB]
        
        for k in range(i+2, nodeCount-i-1):
            solC = solution[k]
            solD = solution[k+1]
            C = points[solC]
            D = points[solD]
            
            posE = i
            
            for j in range(k+3, nodeCount-k+1):
                solE = solution[j]
                solF = solution[j+1]
                E = points[solE]
                F = points[solF]
                
                prevLen = length(A,B) + length(C,D) + length(E,F)
                currLen = length(E,C) + length(B,F) + length(A,D)
                if prevLen > currLen: 
                    posE = j
                    prevLen = currLen
        
            if posE != i:
                solution = threeOptMachine(solA, solB, solC, solD, posE, solution, points)
                repeat+= 1      
                print len(solution)    
                print solution
                break
    result = []
    result.append(solution)
    result.append(repeat)                
        
    return result


def fourOptOrder(solA, solB, solC, solD, solE, solution, points):
    A = points[solA]
    B = points[solB]
    C = points[solC]
    D = points[solD]
    E = points[solE]
    
    newOrder = []
    optLength = 1000000000
    
    for i in itertools.permutations('BCD'):        
        len = length(A, vars()[i[0]]) + length(vars()[i[0]], vars()[i[1]]) + length(vars()[i[1]], vars()[i[2]]) + length(vars()[i[2]], E)       
        
        if len < optLength:
            newOrder = []
            optLength = len
            newOrder.append(points.index(vars()[i[0]]))
            newOrder.append(points.index(vars()[i[1]]))
            newOrder.append(points.index(vars()[i[2]]))
    
    sol1 = solution[:solution.index(solA)+1]
    sol2 = newOrder   
    sol3 = solution[solution.index(solE):]
    solution = sol1 + sol2 + sol3
    
    return solution


def fourOpt(solution, points, nodeCount):
    for i in range(0, nodeCount-4):
        solA = solution[i]
        solB = solution[i+1]
        solC = solution[i+2]
        solD = solution[i+3]
        solE = solution[i+4]
        
        solTemp = fourOptOrder(solA, solB, solC, solD, solE, solution, points)
        solution = solTemp
        
    return solution

#  ------------------========= CUSTOM FUNCTIONS END ==========--------------------

Point = namedtuple("Point", ['index', 'x', 'y'])



def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(i, float(parts[0]), float(parts[1])))


    # ----------mySOLUTION
    mySolution = []
    mySolution.append(0)
    enrouted = []
    
    for i in range(0, nodeCount):
        if i == 0:  enrouted.append([i, 0])
        else: enrouted.append([i, 1])
    
    
    for i in range(0, nodeCount-1):
        basicSolRes = basicSol(mySolution, enrouted, points, nodeCount)
      
        
#     mySolution = range(0, nodeCount)
#     mySolution = threeOpt(mySolution, points, nodeCount) 
     
#     repeat = 1
#     while repeat != 0:
#         mySolutionRes = threeOpt(mySolution, points, nodeCount)
#         mySolution = mySolutionRes[0]             
#         if mySolutionRes[1] == 0: repeat = 0
    
    
    repeat = 1
    while repeat != 0:
        mySolutionRes = twoOpt(mySolution, points, nodeCount)
        mySolution = mySolutionRes[0]            
        if mySolutionRes[1] == 0: repeat = 0
    
#     mySolution = threeOpt(mySolution, points, nodeCount) 
        
    repeat = 1
    while repeat != 0:
        mySolutionRes = twoOptRev(mySolution, points, nodeCount)
        mySolution = mySolutionRes[0]               
        if mySolutionRes[1] == 0: repeat = 0
        
        
#     mySolution = threeOpt(mySolution, points, nodeCount)    
    mySolution = fourOpt(mySolution, points, nodeCount)
    
    repeat = 1
    while repeat != 0:
        mySolutionRes = threeOpt(mySolution, points, nodeCount)
        mySolution = mySolutionRes[0]              
        if mySolutionRes[1] == 0: repeat = 0    
        
    repeat = 1
    while repeat != 0:
        mySolutionRes = twoOpt(mySolution, points, nodeCount)
        mySolution = mySolutionRes[0]             
        if mySolutionRes[1] == 0: repeat = 0
        
    repeat = 1
    while repeat != 0:
        mySolutionRes = threeOpt(mySolution, points, nodeCount)
        mySolution = mySolutionRes[0]             
        if mySolutionRes[1] == 0: repeat = 0
         
    mySolution = fourOpt(mySolution, points, nodeCount)
    
#     repeat = 1
#     while repeat != 0:
#         mySolutionRes = threeOpt(mySolution, points, nodeCount)
#         mySolution = mySolutionRes[0]             
#         if mySolutionRes[1] == 0: repeat = 0
      
    
    
    
#     print mySolution
#     print mySolution[::-1]
    #---------------------
        
    
    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = range(0, nodeCount)
    
    # calculate the length of the tour
    obj = length(points[mySolution[-1]], points[mySolution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[mySolution[index]], points[mySolution[index+1]])
  
    # prepare the mySolution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, mySolution))
    
#     # calculate the length of the tour
#     obj = length(points[solution[-1]], points[solution[0]])
#     for index in range(0, nodeCount-1):
#         obj += length(points[solution[index]], points[solution[index+1]])
#  
#     # prepare the solution in the specified output format
#     output_data = str(obj) + ' ' + str(0) + '\n'
#     output_data += ' '.join(map(str, solution))
    
    
#     twoOptMachine(points[32], points[4], points[0], points[49], mySolution)

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
#         print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

#  ----------- to be commented out before submission ----------------- 
    input_data_file = open('./data/tsp_200_1', 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()
    print solve_it(input_data)
