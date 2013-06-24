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
    
    #check status of items
    def item_fits(current_item,current_cap):
        if(weights[current_item] <= current_cap):
            return True
        else:
            return False

    def take_this_item(item_index,current_val,current_cap):
        if(item_fits(item_index,current_cap)):
            current_val += values[item_index]
            current_cap -= weights[item_index]
            return current_val
        else:
            return current_val

    def get_val_of_best_item(current_item,current_cap):
        #if there's no space, take the 0th item (no item)
        if(current_cap == 0):
            return 0
        #if current item doesn't fit
        elif(not item_fits(current_item,current_cap)):
            #checkif last item fits at current capacity
            if(item_fits(current_item-1,current_cap)):
                #check if max_values at current_cap, last col is not null
                if(max_values[current_cap][current_item-1]):
                    #if so, return the value of the last item at new capacity
                    return max_values[current_cap][current_item-1]
                else:
                    #return nothing
                    return 0
            else:
                return 0
            
        #else if current item fits
        elif(weights[current_item] <= current_cap):
            #check if current item is better than item to its left (last item at same capacity)
            if(values[current_item] >= max_values[current_cap][current_item-1]):
                #if it is....
                #and if its weight is equal to current capacity
                if(weights[current_item] == current_cap):
                    return values[current_item]
                else:
                    #store new_capacity with current item's weight subtracted
                    new_cap = current_cap - weights[current_item]
                    if(not max_values[new_cap][current_item-1]):
                        return values[current_item] + 0
                    else:
                        return values[current_item] + max_values[new_cap][current_item-1]
            #if it's not...
            else:
                #return the item to its left instead
                return max_values[current_item][current_item-1]
        else:
            return 0
            # return 'y'

    def get_last_max_value_that_fits(current_item,current_cap,acc):
        #check if last item fits
        if(item_fits(current_item-1,current_cap)):
            #check if the current item doesn't fit
            if(not item_fits(current_item,current_cap)):
                #if it doesn't, then store value of last max item
                acc += max_values[current_cap][current_item-1]
                #return value of last item
                print 'Acc is ' + str(acc)
                # #if last max item 
                # if(max_values[current_cap-weights][current_item-1] < ):
                return acc
            else:
            #return nothing
                return acc
        #if last item doesn't fit
        else:
            #return nothing
            return acc

    def populate_matrix():
        for current_cap in (range(0,capacity+1)):
            for current_item in (range(0,items+1)):
                #v3
                max_values[current_cap][current_item] = get_val_of_best_item(current_item,current_cap)

    def display_matrix_header():
        #debug - displays heding of matrix    
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

    def display_matrix():
        #debug - checks context of max_values matrix
        for r in range(0, len(max_values)):
            print 'cap '+str(r)+ ': ' + str(max_values[r])



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

    #builds matrix
    build_matrix()
    #adds zeros
    make_zero_col()

    #debug
    populate_matrix()

    #debug shows heading of max_vals matrix
    display_matrix_header()

    #debug
    display_matrix()

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

