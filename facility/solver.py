#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import itemgetter
import math
import time



#  --------------------========= CUSTOM FUNCTIONS ==========----------------------
start = time.clock()
# def sign(n):
#     sign = 0
#     if n < 0 : sign = -1
#     if n > 0 : sign = 1
#     return sign


# def midPoint(A, B):
#     x = (A.x + B.x)/2
#     y = (A.y + B.y)/2
#     return [x, y]

    
def pseudoLength(point1, point2):
    return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def length(point1, point2):
    return math.sqrt(pseudoLength(point1, point2))

def totalCost(facilities, solution, customers):
    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)
        
    return obj

def resetFacilityDict(facilityDict, facilities):
    for i in range(0, len(facilityDict)):
        facilityDict[i]['customers'] = []
        facilityDict[i]['customerCount'] = 0
        facilityDict[i]['room'] = facilities[i].capacity
    return

def populateOpenFacility(facilityDict):
    openFacilityDict = []
    for i in range(0, len(facilityDict)):  # ------------Selects facilities which are open and aggregates in 'openFacilityDict'
        if facilityDict[i]['status'] == 1 :
            openFacilityDict.append({'index' : facilityDict[i]['index'], 'room' : facilityDict[i]['room'], 'customers' : facilityDict[i]['customers'], 'customerCount' : facilityDict[i]['customerCount'], 'status' : 1})
    return openFacilityDict

def assignFacility(custInd, demand, facilitySelected, facilities, facilityDict):
    facilityDict[facilitySelected]['room']-= demand
    facilityDict[facilitySelected]['customers'].append(custInd)
    facilityDict[facilitySelected]['customerCount']+= 1


def selectFacillity(custInd, custLoc, demand, facilities, facilityDict, openFacilityDict, customerDict, solution):
    distDict = []
#     openFacilityDict = []    
    
#     for i in range(0, len(facilityDict)):  # ------------Selects facilities which are open and aggregates in 'openFacilityDict'
#         if facilityDict[i]['status'] == 1 :
#             openFacilityDict.append({'index' : facilityDict[i]['index'], 'room' : facilityDict[i]['room'], 'customers' : facilityDict[i]['customers'], 'customerCount' : facilityDict[i]['customerCount'], 'status' : 1})
#     
    for i in range(0, len(openFacilityDict)):
        index = openFacilityDict[i]['index']
        dist = length(custLoc, facilities[index].location)
        distDict.append({'index': facilities[index].index, 'dist': dist})    

    distDict = sorted(distDict, key=itemgetter('dist'))
    
    i = 0
    while demand > facilityDict[distDict[i]['index']]['room'] :
        i+= 1
    facilitySelected = distDict[i]['index']
    assignFacility(custInd, demand, facilitySelected, facilities, facilityDict)
    
    solution[custInd] = facilitySelected
    
    print len(solution)    

    return    


def closeFacilities(facilityDict, facilities, solution, customers, customerDict):
    openFacilityDict = []
    lastCost = totalCost(facilities, solution, customers)
    print lastCost
    
    toClose = []
    facilityDict = sorted(facilityDict, key=itemgetter('customerCount'))
    for i in range(0, len(facilityDict)):
        toClose.append(facilityDict[i]['index'])
    print toClose
    
#     for i in range(0, len(facilityDict)):
    for i in range(0,30):
        facilityDict = sorted(facilityDict, key=itemgetter('index'))
        index = toClose[i]
        
        facilityDict[index]['status'] = 0
        if facilityDict[index]['customerCount'] > 0 :
            resetFacilityDict(facilityDict, facilities)
            openFacilityDict = populateOpenFacility(facilityDict)
            for customer in customers:
                selectFacillity(customer.index, customer.location, customer.demand, facilities, facilityDict, openFacilityDict, customerDict, solution)
             
            newCost = totalCost(facilities, solution, customers)
            print newCost
             
            if newCost > lastCost: 
                facilityDict[iindex]['status'] = 1
                openFacilityDict = populateOpenFacility(facilityDict)
                resetFacilityDict(facilityDict, facilities)
                for customer in customers:
                    selectFacillity(customer.index, customer.location, customer.demand, facilities, facilityDict, openFacilityDict, customerDict, solution)
                newCost = totalCost(facilities, solution, customers)
                 
            print newCost
    
    return 
#  ------------------========= CUSTOM FUNCTIONS END ==========--------------------

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))
        
    
            
    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    solution = [-1]*len(customers)
    capacity_remaining = [f.capacity for f in facilities]

    facility_index = 0
#     for customer in customers:
#         if capacity_remaining[facility_index] >= customer.demand:
#             solution[customer.index] = facility_index
#             capacity_remaining[facility_index] -= customer.demand
#         else:
#             facility_index += 1
#             assert capacity_remaining[facility_index] >= customer.demand
#             solution[customer.index] = facility_index
#             capacity_remaining[facility_index] -= customer.demand
            
            
            
     # My SOLUTION******************************************************
    
    facilityDict = []
    customerDict = []   
    
    for i in range(0, facility_count):
        facilityDict.append({'index':i, 'room':facilities[i].capacity, 'customers':[], 'customerCount' : 0, 'status' : 1})    
#         print facilities[i]
    
    
    
    
    print 'Customers: ' + str(customer_count)
    
    for i in range(0, customer_count):
        customerDict.append({'index':i, 'facility':-1})
#         print customers[i]
        
#     print customerDict   
    
    openFacilityDict = populateOpenFacility(facilityDict)
    for customer in customers:
        selectFacillity(customer.index, customer.location, customer.demand, facilities, facilityDict, openFacilityDict, customerDict, solution)
    
    closeFacilities(facilityDict, facilities, solution, customers, customerDict)   
   
    facilityDict = sorted(facilityDict, key=itemgetter('customerCount'))
    for i in range(0, facility_count):
        print facilityDict[i]
        
    
    
    #********************************************************************            
            
            

    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         file_location = sys.argv[1].strip()
#         input_data_file = open(file_location, 'r')
#         input_data = ''.join(input_data_file.readlines())
#         input_data_file.close()
#         print 'Solving:', file_location
#         print solve_it(input_data)
#     else:
#         print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)'

#  ----------- to be commented out before submission ----------------- 
    input_data_file = open('./data/fl_100_11', 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()
    print solve_it(input_data)
