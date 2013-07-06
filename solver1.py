#!/usr/bin/python
# -*- coding: utf-8 -*-

#timer start
from datetime import datetime
tstart = datetime.now()
#timer start

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    #--------------------------
    #-- START PREPARE INPUT ---
    #--------------------------

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

    #------------------------
    #--- END PREPARE INPUT --
    #------------------------
    #========================
    #------------------------
    #-- BEGIN ALGORITHM 1 ---
    #------------------------

    def run_alg_1():

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

        def compare_item_to_left(current_item,current_cap):
            #store data as variables, or default them to 0
            val_of_item = values[current_item] if values[current_item] else 0
            val_to_left = max_values[current_cap][current_item-1] if max_values[current_cap][current_item-1] else 0
            val_to_left_down = max_values[current_cap-weights[current_item]][current_item-1] if max_values[current_cap-weights[current_item]][current_item-1] else 0
            
            #check if current item is better than item to its left (last item at same capacity)
            if(val_of_item < val_to_left):
                #if it is....
                #check if val to left_down + cu
                if((val_to_left_down + val_of_item) > val_to_left):
                    #just return their sum
                    return val_to_left_down + val_of_item
                #otherwise
                else:
                    #return val_to_left
                    return val_to_left
            #if it's not...
            #check if current item + val of diag left item are great
            else:
                #return the item to its left instead
                return val_of_item

        def which_items(cap,item,acc):
            #identifies index of which items are taken and populates
            #the 'taken' array as 'acc' by traversign the max_values matrix
            #in reverse

            if(item == 0):
                return acc
            elif(cap < 0 or item < 0):
                return acc
            elif(max_values[cap][item] == max_values[cap][item-1]):
                #not taken
                #add item value to array
                acc.insert(0,0)
                return which_items(cap,item-1,acc)
            elif(max_values[cap][item] != max_values[cap][item-1]):
                #taken
                #adds item value to array
                acc.insert(0,1)
                return which_items(cap-weights[item],item-1,acc)

        def get_val_of_best_item(current_item,current_cap):
            #if there's no space, take the 0th item (no item)
            if(current_cap == 0):
                return 0
            #if current item doesn't fit and something is to the left
            elif(not item_fits(current_item,current_cap) and max_values[current_cap][current_item-1]):
                #get value of item to the left
                return max_values[current_cap][current_item-1]
            #else if current item fits
            elif(item_fits(current_item,current_cap)):
                return compare_item_to_left(current_item,current_cap)
            else:
                return 0
                # return 'y'

        def populate_matrix():
            for current_cap in (range(0,capacity+1)):
                for current_item in (range(0,items+1)):
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

        #runs the first algorithm

        #builds matrix
        build_matrix()
        #adds zeros
        make_zero_col()

        #debug
        populate_matrix()

        #debug - shows heading of max_values matrix with key
        # display_matrix_header()

        # #debug - visualizes max_values matrix
        # display_matrix()

        
        # populates 'taken' array of which items were taken
        which_items(capacity,items,taken)

        # print taken

        #returns best value
        return max_values[capacity][items]

    #------------------------
    #--- END ALGORITHM 1 ----
    #------------------------
    #========================
    #------------------------
    #-- BEGIN ALGORITHM 2 ---
    #------------------------

    #use the bound and branch method

    value = 0
    weight = 0
    taken = []
    
    #------------------------
    #-- RUN ALGORITHM 1 ---
    #------------------------

    #sets optimal value to result from running algorithm 1
    # value = run_alg_1()

    #-------------------------
    #--- STOP ALGORITHM 1 ----
    #-------------------------

    #=========================

    #------------------------
    #-- RUN ALGORITHM 3 ---
    #------------------------

    #sets optimal value to result from running algorithm 1
    value = run_alg_1()
    # print value

    #-------------------------
    #--- STOP ALGORITHM 3 ----
    #-------------------------

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

#timer end
tend = datetime.now()
print tend - tstart