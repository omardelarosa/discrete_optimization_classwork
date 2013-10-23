#!/usr/bin/python
# -*- coding: utf-8 -*-

#timer start
from datetime import datetime
tstart = datetime.now()
#timer start

execfile("node_lib.py")

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

    current_best_node = None

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
        root_data = {
            #item, room, value, current_best, parent, taken
            "item": -1,
            "room" : capacity,
            "value" : 0,
            "current_best" : current_best,
            "current_best_node" : None,
            "parent" : None,
            "taken" : False
            }

        root_node = Node(root_data)

        #keeps track of current best node
        current_best_node = root_node
        #keeps a stack of nodes
        node_stack = [root_node]

        #debug
        # root_node.to_s()

        # #check plausibility of next tree
        # def is_plausible(weight,room):
        #     if weight <= room:
        #         return True
        #     else:
        #         return False

        # #check plausibility of value
        # def is_continuing_worth_it(current_value,current_best):
        #     if current_value >= current_best:
        #         return True
        #     else:
        #         return False

        def add_node_to_stack(node):
            # if node_stack != []:

            #     node_stack.pop()
            node_stack.append(node)

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

        # def estimate_child(parent_node,item):
        #     child_data = {
        #         "next_node_taken_room" : parent_node.data["room"]-weights[item],
        #         "next_node_not_taken_room" : parent_node.data["room"],
        #         "next_node_taken_value" : parent_node.data["value"]+values[item],
        #         "next_node_not_taken_value" : parent_node.data["value"],
        #         "next_node_taken_current_best" : parent_node.data["current_best"],
        #         "next_node_not_taken_current_best" : parent_node.data["current_best"]-values[item]
        #     }
        #     return child_data
            

        #build tree exhaustively
        def add_children(item,parent_node):
            #start at 0th item
            # item = 0

            current_best_node = parent_node

            # if current_best_node != root_node and current_best_node == parent_node:
            #     return parent_node

            #if it is the root node, do not recurse and return
            if parent_node != parent_node.data["parent"]:
                #loop over each item (i.e. level of tree)
                while item < items:

                    #estimate values of next item
                    child_taken_node_data = make_child_taken_node(parent_node,item)
                    child_not_taken_node_data = make_child_not_taken_node(parent_node,item)

                    #if next item fits 
                    if child_taken_node_data["room"] >= 0:

                            #take item
                            new_node = Node(child_taken_node_data)
                            
                            if new_node.data["value"] >= parent_node.data["current_best_node"].data["value"]:
                                parent_node.data["current_best_node"] = new_node
                                # node_stack.append(new_node)

                            # new_node = Node(child_not_taken_node_data)
                            # node_stack.append(new_node)
                            # #check to see if item depth level is the end
                            # if item == items-1:
                            #     print "New Node is " + new_node.to_s()
                            
                        # if child_taken_node_data["current_best"] > current_best_node.data["value"]:
                        #     new_node = Node(child_not_taken_node_data)
                            # node_stack.append(new_node)
                            
                            

                    #check if not taking item is worth it
                    elif child_not_taken_node_data["current_best"] >= current_best:
                        #don't take item
                        new_node = Node(child_not_taken_node_data)
                        

                        if new_node.data["value"] >= parent_node.data["current_best_node"].data["value"]:
                            parent_node.data["current_best_node"] = new_node
                            # node_stack.append(new_node)
                        # #don't take item
                        # new_node = Node(child_not_taken_node_data)
                        # node_stack.append(new_node)

                    #else take best leaf
                    else:
                        new_node = parent_node
                        node_stack.append(new_node.data["current_best_node"])
                    
                    
                    # timer end
                    # if not (datetime.now() - tstart).total_seconds() > 18000 :
                        # build rest of tree

                    #no filtering
                    # add_children(item,new_node,current_best_node)
                    if new_node and new_node.data["value"] >= parent_node.data["current_best_node"].data["value"]:
                        parent_node.data["current_best_node"] = new_node
                            
                    item += 1
                    add_children(item,new_node)
                    
            
            if parent_node.data["current_best_node"].data["value"] >= current_best_node.data["value"]:
                current_best_node = parent_node

            
            return current_best_node
                 

                    
        new_best = add_children(0,root_node)

        print new_best.to_s()

        # def iterative_tree(node):
        #     taken_stack = []
        #     while taken_stack != [] or node != None:
        #         if node != None:
        #             taken_stack.push(node)
                    
        #             node = node.left
        #         else:
        #             node = taken_stack.pop()
        #             taken_node_data = {
        #                 #item, room, value, current_best, parent, taken
        #                 "item": item,
        #                 "room" : node.data["room"]-weights[item],
        #                 "value" : node.data["value"]+values[item],
        #                 "current_best" : node.data["current_best"],
        #                 "parent" : node,
        #                 "taken" : node.data["taken"].append(1)
        #             }
        #             new_taken_node = Node(taken_node_data)
        #             node = node.right

        # def get_branch(start_node,max_level):
        #     branch_stack = []
        #     for level in range(0,max_level):

        #         if start_node != None:



        # def add_child(item,items,node,current_best_node):
        #     if item > items-1:
        #         return False
        #     else:
        #         #useful local vars
        #         taken_value = node.data["value"]+values[item]
        #         room_if_taken = node.data["room"]-weights[item]
        #         best_value_if_not_taken = node.data["current_best"]-values[item]
        #         not_taken_value = node.data["value"]
        #         #if there's room...
        #         if room_if_taken >= 0:
        #             #then check if not taking would make negative value or 0
        #             # if best_value_if_not_taken > 0:

        #             taken_node_data = {
        #                 #item, room, value, current_best, parent, taken
        #                 "item": item,
        #                 "room" : node.data["room"],
        #                 "value" : node.data["value"],
        #                 "current_best" : node.data["current_best"]-values[item],
        #                 "parent" : node,
        #                 "taken" : 0
        #                 }
        #             #make a taken node
        #             new_taken_node = Node(taken_node_data) 

        #             #make a not taken node
        #             not_taken_node_data = {
        #                     #item, room, value, current_best, parent, taken
        #                     "item": item,
        #                     "room" : node.data["room"],
        #                     "value" : node.data["value"],
        #                     "current_best" : node.data["current_best"]-values[item],
        #                     "parent" : node,
        #                     "taken" : 0
        #                 }
        #             new_not_taken_node = Node(not_taken_node_data)
        #             add_node_to_stack(new_taken_node)
        #             add_node_to_stack(new_not_taken_node)
        #             # if new_taken_node.data["value"] > current_best_node.data["value"]:
        #             #     # current_best_node = new_taken_node

        #             if add_child(item+1,items,new_taken_node,current_best_node) and add_child(item+1,items,new_not_taken_node,current_best_node):
        #                 return True

        #         else:
        #             #inplausible outcome
        #             return False

        # add_child(0,items,root_node,current_best_node)


        def get_max_value_old():
            #get all nodes at final level
            max_level_nodes_array = all_nodes[-1].get_all_nodes_at_same_level()

            plausible_maxes = map(lambda node: {'value': node.data["value"], 'id': node.data["id"]} if node.data["room"] >= 0 else 0, max_level_nodes_array)
            # print plausible_maxes

            current_max = 0
            id_of_max = 0

            for i in plausible_maxes:
                if i["value"] > current_max:
                    current_max = i["value"]
                    id_of_max = i["id"]

            # paths = map(lambda node: node.get_path([],0), all_nodes)

            path_of_max = all_nodes[id_of_max].get_path(taken,items)

            # print "Current Max is "+str(current_max)
            # print "Current Max's ID is "+str(id_of_max)
            # print "Path of Max is " +str(path_of_max)
            return current_max

        def get_max_value():
            current_max = 0
            id_of_max = 0
            max_node = root_node

            # plausible_maxes = map(lambda node: {'value': node.data["value"], 'node': node} if node.data["room"] >= 0 else 0, node_stack)

            # print "Plausible Maxes"
            # print plausible_maxes

            for node in node_stack:
                # print node.to_s()
                if node.data["value"] > current_max:
                    current_max = node.data["value"]
                    max_node = node

            path_of_max = max_node.get_path(taken,items)
            return current_max

        # print "Node Stack Size: "+str(len(node_stack))

        return get_max_value()

        # def calc_bound(node):
        #     taken_value = node.

        # def add_children_2(node):
        #     parent_stack = []
        #     best_node = root_node

        #     while parent_stack != [] or node != None:
        #         if node != None:
        #             parent_stack.push(node)
        #         else:
        #             node = parent_stack.pop()
        #             if node.data["value"] > best_node 

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
    value = run_alg_3()
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

# # timer end
# tend = datetime.now()
# print (tend - tstart).total_seconds()  5.0