#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    def run_alg_2():
        
        #grab 'defaultdict' from 'collections' module
        from collections import defaultdict

        # sum of all values in set
        sigma_values = reduce(lambda x, y: x+y, values)

        # sum of all weights in set
        sigma_weights = reduce(lambda x, y: x+y, weights)

        #a dict to hold item's weights and values
        weights_values = {}
        weights_values['weights'] = weights
        weights_values['values'] = values

        #tree-maker
        def tree(): return defaultdict(tree)

        #convert tree to dict of dicts
        def dicts(t): return {k: dicts(t[k]) for k in t}

        #add or append a new node, returns its key
        def add_child_node(tree,new_key,last_key,val):
            tree[last_key][new_key] = val
            return new_key

        root = tree()

        #make tree
        def make_tree_of_items(weights_values,items,init,root):
            #takes a set of items' values and weights as 2D array and size of set
            array = []
            
            #iterates over array and turns it into a binary tree
            for i in range(init,items)
                array.append(i)
                if(i % 2 == 0):
                    root[1] = [weights[i],values[i]]
                    add_child_node(root[1],1,[weights[i],values[i]])
                    init+=1
                    # return make_tree_of_items(weights_values,items,init,)
                else:
                    print 'odd!'
                    # add_child_node(root,0,[weights[init],values[init]])
                    init+=1
                    # return make_tree_of_items(weights_values,items,init,add_child_node(root,0,[weights[init],values[init]]))
                # #if item weighs
                # if (weights_values['weights'][i]):
                #     add_node(a_tree,1,[weights_values['weights'][i],weights_values['values'][i]])
                # else:
                #     add_node(a_tree,0,[0,0])
            
            print array
            #returns a tree made by their contents
            return root

        #creates a demo tree structure
        #each node represents an item
        #each item's key is either 1 or 0 for taken or not taken respectively
        #the value of each node is an array whose first item is the remaining weight
        #the second item is the current value

        #need a function that appends a node

        #creates

        # def sort_list_by_vals(list):
        #     #get unsorted list -> sorted list

        # def get_estimate_for_best_total_val():
        #     # -> best total value if 'capacity' is relaxed

        # def compare_estimate_to_current_val(current_val,best_val):
        #     # -> boolean re: whther it's better (true) or if it's not (false)

        #----------ALG 2 Recipe---------

        # make_tree_of_values

        # return node with highest value

        return make_tree_of_items(weights_values,items,0,root)

        # return root

    #-------------------------
    #--- END ALGORITHM 2 -----
    #-------------------------

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
    #-- RUN ALGORITHM 2 ---
    #------------------------

    #sets optimal value to result from running algorithm 1
    print run_alg_2()

    #-------------------------
    #--- STOP ALGORITHM 2 ----
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

