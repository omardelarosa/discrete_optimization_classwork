#!/usr/bin/python
# -*- coding: utf-8 -*-

#timer start
from datetime import datetime
tstart = datetime.now()
#timer start

#loads node class def
execfile("node_lib.py")

values = []
weights = []

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

    

    for i in range(1, items+1):
        line = lines[i]

        #debug - checks contents of line
        #print(str(line))
        
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

    

    def compute_max():

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

        # print "Sorted items list: "
        # print sorted_list_of_item_dicts

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

        def make_child_taken_node(node,item):
            #make taken node
            next_node_data = {
                #item, room, value, current_best, parent, taken
                "item": item,
                "room" : node.data["room"]-weights[item],
                "value" : node.data["value"]+values[item],
                "current_best" : node.data["current_best"],
                "current_best_node" : node.data["current_best_node"],
                "parent" : node,
                "taken" : 1
            }
            return next_node_data

        def make_child_not_taken_node(node,item):
            #make taken node
            next_node_data = {
                #item, room, value, current_best, parent, taken
                "item": item,
                "room" : node.data["room"],
                "value" : node.data["value"],
                "current_best" : node.data["current_best"]-values[item],
                "parent" : node,
                "current_best_node" : node.data["current_best_node"],
                "taken" : 0
            }
            return next_node_data
        

        root_data = {
                #item, room, value, current_best, parent, taken
                "item": -1,
                "room" : capacity,
                "value" : 0,
                "current_best" : get_relaxed_estimate(),
                "parent" : None,
                "current_best_node" : False,
                "taken" : False
                }

        root_node = Node(root_data)

        root_node.data["current_best_node"] = root_node

        stacks = []
        current_best_node = root_node
        current_best = get_relaxed_estimate()

        def iterative_function(node,item,items):
            
            # stack = []
            # current_room = capacity

            #if max depth has been reached and current item fits
            if item == items-1 and weights[item] <= node.data["room"]:
                #make new taken node
                new_node = Node(make_child_taken_node(node,item))

                if new_node.data["value"] < node.data["current_best_node"].data["value"]:
                    node.data["current_best_node"] = new_node.data["value"]
                    # print "Best Changed! 1"
                    # print new_node.to_s()
                    return new_node

                #stop recursion
                return node.data["current_best_node"]
            #if max depth and current item doesn't fit
            elif item == items-1 and weights[item] > node.data["room"]:
                #make new not taken node
                new_node = Node(make_child_not_taken_node(node,item))
                #check 
                if new_node.data["value"] < node.data["current_best_node"].data["value"]:
                    node.data["current_best_node"] = new_node
                    # print "Best Changed! 2"
                    # print new_node.to_s()
                    return new_node

                #stop recursion
                return node

            else:
                #if current item doesn't fit
                if weights[item] > node.data["room"]:
                    #check if not-branch is worth exploring
                    if node.data["current_best"]-values[item] > node.data["current_best_node"].data["value"]:
                        #make new node
                        new_node = node.right_not_taken(item)
                        #don't take item and keep exploring
                        return iterative_function(new_node,item+1,items)
                    else:
                        #return current best node
                        return node
                #if it fits
                else:
                    #make new node and take item
                    new_node = node.left_taken(item)

                    if new_node.data["value"] > node.data["current_best_node"].data["value"]:
                        node.data["current_best_node"] = new_node
                        # print "Best Changed! 3"
                        # print new_node.to_s()
                    #don't take item and keep exploring
                    return iterative_function(new_node,item+1,items)


            # print(root_node.to_s());

            # print(root_node.left_taken(1).to_s());

            # print(root_node.right_not_taken(1).to_s());

        item = 0
        best_node = root_node
        stack = []
        current_max = 0

        while item < items:
            new_node = iterative_function(root_node,item,items)
            #search stack thus far for best node
            # for node in stack:
            #     # print node.to_s()
            #     if node.data["value"] >= current_max:
            #         current_max = node.data["value"]
                    
            if new_node and new_node.data["value"] >= best_node.data["current_best_node"].data["value"]:
                best_node = new_node
            
            # stack.append(new_node)
            item+=1

        # print best_node.to_s()
        # for node in stack:
        #     node.to_s()

        return best_node

        # print(stacks)


        #pseudo code of solution
        # iterativeInorder(node)
        #   parentStack = empty stack
        #   while not parentStack.isEmpty() or node != null
        #     if node != null then
        #       parentStack.push(node)
        #       node = node.left
        #     else
        #       node = parentStack.pop()
        #       visit(node)
        #       node = node.right

        # def iterative_function(node,item):
        #     parentStack = []
        #     while parentStack == [] or node != None or item < items:
        #         if node != None:
        #             parentStack.append(node)
        #             node = node.left_taken(item+1)
        #         else:
        #             node = parentStack.pop()
        #             node = node.right_not_taken(item+1)
        #     return parentStack

        # print(iterative_function(root_node,0))

        # return False

    #------------------------
    #--- END ALGORITHM 1 ----
    #------------------------
    #========================
    best_node = compute_max()
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
    value = best_node.data["value"]
    taken = best_node.get_path([],items)
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