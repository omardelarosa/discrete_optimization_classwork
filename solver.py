#!/usr/bin/python
# -*- coding: utf-8 -*-

#timer start
from datetime import datetime
tstart = datetime.now()
#timer start

execfile("./node_lib.py")

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

    def run_alg_3():

        def make_list_of_item_dicts(values,weights):
            items_list = []
            for item in range(0,items):
                items_list.append({"id": item, "value" : values[item], "weight" : weights[item], "value_to_weight" : float(values[item])/float(weights[item])})
            return items_list

        # def make_ratios_list(values,weights):
        #     ratios_list = []
        #     for item in range(0,items):
        #         ratios_list.append(float(values[item])/float(weights[item]))
        #     return ratios_list

        list_of_item_dicts = make_list_of_item_dicts(values,weights)
        sorted_list_of_item_dicts = sorted(list_of_item_dicts, key=lambda k: k['value_to_weight'])

        print "Sorted items list: "
        print sorted_list_of_item_dicts

        #this could be more efficient
        def get_relaxed_estimate():
            room = capacity
            current_value = 0
            for item in sorted_list_of_item_dicts:
                if item["weight"] < room:
                    current_value += item["value"]
                    room -= item["weight"]
                else:
                    partial_val = room * item["value_to_weight"]
                    current_value += partial_val
            return current_value 

        # relaxed_estimate = get_relaxed_estimate()

        #Node(item, room, value, current_best, parent)

        #a few useful values
        # sum of all values in set
        # sigma_values = reduce(lambda x, y: x+y, values)

        # print "Sigma Values is: "
        # print sigma_values
        # sum of all weights in set
        # sigma_weights = reduce(lambda x, y: x+y, weights)
       
        # #current best
        current_best = get_relaxed_estimate()

        #make root node
        root_node = Node(-1,capacity,0,current_best,None,False)

        #debug
        root_node.to_s()

        #check plausibility of next tree
        def is_plausible(weight,room):
            if weight <= room:
                return True
            else:
                return False

        #check plausibility of value
        def is_continuing_worth_it(current_value,current_best):
            if current_value >= current_best:
                return True
            else:
                return False

        #build tree exhaustively
        def add_children(item,parent_node):
            #start at 0th item
            # item = 0

            #add_children
            if parent_node != False:
                #loop over each item (i.e. level of tree)
                while item < items:

                    #filter only what plausibly fits
                    if is_plausible(weights[item],parent_node.room):
                        #make taken node
                        taken_node = Node(item,parent_node.room-weights[item],parent_node.value+values[item],parent_node.current_best,parent_node,1)
                    else:
                        #dont make new node
                        taken_node = False
                    #filter out values 
                    if is_continuing_worth_it(parent_node.value,parent_node.current_best):
                        #make a not-taken node
                        not_taken_node = Node(item,parent_node.room,parent_node.value,parent_node.current_best-values[item],parent_node,0)
                    else:
                        #don't make new node
                        not_taken_node = False
                    
                    # no filter
                    # #make taken node
                    # taken_node = Node(item,parent_node.room-weights[item],parent_node.value+values[item],parent_node.current_best,parent_node,True)

                    # #make a not-taken node
                    # not_taken_node = Node(item,parent_node.room,parent_node.value,parent_node.current_best-values[item],parent_node,0)

                    #debug
                    # taken_node.to_s()
                    # #debug
                    # not_taken_node.to_s()
                    # increment by 1
                    item+=1
                    #stop building tree
                    add_children(item,not_taken_node)
                    #build rest of tree
                    add_children(item,taken_node)

                        
                        #make a tree for item taken
                        # item+=1
                        # add_children(item,taken_node)
                        # add_children(item,not_taken_node)

                        #make a tree for item not taken

                        # #check if item fits
                        # if weights[item] <= root_node.capacity:
                        #     #if it fits, create a node here
                    

        add_children(0,root_node)

        #debug
        # paths = map(lambda node: node.get_path([]), all_nodes)
        # print paths

        def get_max_value():
            #get all nodes at final level
            max_level_nodes_array = all_nodes[-1].get_all_nodes_at_same_level()

            plausible_maxes = map(lambda node: {'value': node.value, 'id': node.id} if node.room >= 0 else 0, max_level_nodes_array)
            # print plausible_maxes

            current_max = 0
            id_of_max = 0

            for i in plausible_maxes:
                if i["value"] > current_max:
                    current_max = i["value"]
                    id_of_max = i["id"]

            paths = map(lambda node: node.get_path([]), all_nodes)

            path_of_max = all_nodes[id_of_max].get_path([])

            print "Current Max is "+str(current_max)
            print "Current Max's ID is "+str(id_of_max)
            print "Path of Max is " +str(path_of_max)
            return current_max

        print "Current max list is "+str(get_max_value())
        print "Current nodes count is "+str(len(all_nodes))
        

        print "Relaxed estimate is: "
        print get_relaxed_estimate()
        
        # print "Sorted list of items (by ratio):"
        # print sorted_list

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
    print run_alg_3()

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