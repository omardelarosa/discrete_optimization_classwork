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
    
    #adds a zero-value col
    def make_zero_col():
        #adds a zeros column to end of array
        weights.insert(0,0)
        values.insert(0,0)

    def remove_zero_col():
        #removes zeros colum to end of array
        weights.pop(0)
        values.pop(0)
    
    #builds max_values matrix
    max_values = []

    def build_matrix():
        for r in (range(0,capacity+1)):
            max_values.append([])
            for c in (range(0,items+1)):
                max_values[r].append([])
    
    #this function builds the max_values matrix
    # def maximize(current_cap, current_item, current_val):

    #     if (current_cap > capacity and current_item > items):
    #         #stop recursion and return false
    #         return false

    #     elif (current_cap > capacity):
    #         #go to next item
    #         current_item += 1
    #         #reset cap or begin at row 1
    #         current_cap = 0

    #         #recurse
    #         maximize(current_cap,current_item,current_val)
    #         return true

    #     elif (current_item > items):
    #         return false

    #     elif (weights[current_item] < current_cap):
    #         #add it to the knapsack 
    #         #and add its value to current_val
    #         current_val += values[item]
            
    #         #update matrix
    #         max_values[current_cap][current_item] = values[current_item]
            
    #         #update current_val acc.
    #         current_val+=values[current_item]

    #         #increment item
    #         current_item+=1

    #         #recurse
    #         maximize(current_cap,current_item,current_val)
                

    #     elif (weights[current_item] == capacity-current_cap):
    #         # else if weight of current item = total capacity - current_cap
    #         # K is at capacity if current item is include
    #         # add the item's value + current_total_val to table
    #         # stop the recursion
    #         # and current_val

    #         #add current_val and val of current item to matrix
    #         max_values[cap][item] = values[item]+current_val

    #         #no recursion

    #     elif (weights[item] > capacity-current_cap):

    #         max_values[current_cap][current_item] = current_val

    #     else:
    #         max_values[cap][item] = current_val

    def item_fits(item_index,current_cap):
        if(weights[item_index] <= current_cap):
            return True
        else:
            return False

    def add_val_of_last_item(current_val,current_cap,current_item):
        #if the last item fits and the remaining capacity is not zero
        
        if(current_cap > 0 and current_item > 0 and weights[current_item-1] <= current_cap):
            #add last most valuable item to knapsack
            current_val += values[current_item-1]
            #compare current item to item before that
            add_val_of_last_item(current_val,current_cap-weights[current_item-1],current_item-2)
        else:
            return current_val

    def get_max_val_by_index(current_cap,current_item,current_val):
        #if current item fits the remaining capacity
        if(item_fits(current_item,current_cap)):
            #then add it to current_val
            current_val += values[current_item]

            #subtract its weight from current max_cap
            current_cap -= weights[current_item]

            #recurse for previous items
            print 'recursed at ' + str(current_item) + ' ' + str(current_cap)
            print 'current val is ' + str(current_val)

            return add_val_of_last_item(current_val,current_cap,current_item)

        elif(current_cap==0 and current_item==0):
            # return current_val
            return current_val
        #if the item doesn't fit
        else:
            #enter the current_val into the max_values matrix
            return current_val
                



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
    # print '[ [weights], [values] ]'
    # print weights_values

    #debug
    # print 'maximize func'
    # print maximize(0,0,0)

    #builds matrix
    build_matrix()
    #adds zeros
    make_zero_col()

    
    #debug
    #populate matrix
    for current_cap in (range(0,capacity+1)):
        for current_item in (range(0,items+1)):
            max_values[current_cap][current_item] = get_max_val_by_index(current_cap,current_item,0)
            

    #debug shows heading of max_vals matrix
    z = 0
    a = []
    for z in range(0,items+1):
        a.append(z)
    print "-------"
    print "Max Values of items..."
    print a
    print "-------"
    print "Weights of items..."
    print weights
    print "Values of items..."
    print values
    print "-------"

    
    #debug - checks context of max_values matrix
    for r in range(0, len(max_values)):
        print 'cap '+str(r)+ ': ' + str(max_values[r])


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

