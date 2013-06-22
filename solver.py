#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]

        #debug - checks contents of line
        #print(str(line))
        
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

    weights_values = [weights,values]
    

    max_values = []
    #builds max_values matrix
    for r in (range(0,capacity)):
        max_values.append([])
        for c in (range(0,items)):
            max_values[r].append([])
    return max_values
    
    #this function builds the max_values matrix
    def maximize(current_cap,current_item,current_val):

        if (weights[current_item] < capacity-current_cap):
            # if weight of current item is less than total capacity - current_cap
            # add the item's value to table
            # increment current_cap
            # then recursive call maximize of current_cap 
            # and add current item's val to current_val
            
            #update matrix
            max_values[current_cap][current_item] = values[current_item]
            
            #update current_val acc.
            current_val+=values[current_item]

            #increment item
            current_item+=1

            #recurse
            maximize(current_cap,current_item,current_val)
                

        elif (weights[current_item] == capacity-current_cap):
            # else if weight of current item = total capacity - current_cap
            # K is at capacity if current item is include
            # add the item's value + current_total_val to table
            # stop the recursion
            # and current_val

            #add current_val and val of current item to matrix
            max_values[cap][item] = values[item]+current_val

            #no recursion

        elif (weights[item] > capacity-current_cap):

            max_values[current_cap][current_item] = current_val

        else:
            max_values[cap][item] = current_val

            #debug
            # print 'Current cap: ' + str(current_cap)
            # print 'Current index: ' + str(index)
            
            #increments current cap
            # current_cap += 1

            #if the weight of the current item
            #is less than the current capacity
            #then add the value of current item
            #to the max_values matrix


        #     if weights_values[0][index] <= current_cap:
        #         #if the item fits its value is added to
        #         #the max_values matrix
        #         max_values[index].append(weights_values[1][index])
                
        #     else:
        #         #if the item doesn't fit, the values matrix
        #         #has a zero added
        #         max_values[index].append(0)

    solutions = []

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = []


    for i in range(0, items):
        #determines if the current total weight and the new added weight exceed capacity
        if weight + weights[i] <= capacity:
            #append a 'true' value to the taken array.
            #this is also what is outputed at the bottom of each line.
            taken.append(1)

            #total value is incremented by the value of current item
            value += values[i]

            #weight is incremented by the weight of the current item.
            weight += weights[i]
        else:
            taken.append(0)

    # need to represent a comparison between the 'values' of
    # various configurations

    #debug
    print '[ [weights], [values] ]'
    print weights_values

    #debug
    print 'maximize func'
    print maximize(0,0,0)

    #debug shows heading of max_vals matrix
    z = 0
    a = []
    for z in range(0,items):
        a.append(z)
    print "Max Values of items..."
    print "-------"
    print a
    print "-------"

    #debug - checks context of max_values matrix
    for r in range(0, len(max_values)):
        print max_values[r]


    #debug
    # print "Max Values: "
    # print max_values

    #end algorithm

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()

        #prints/processes the solution
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

