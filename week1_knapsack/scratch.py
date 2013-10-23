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
        "parent" : None,
        "taken" : False
        }

    root_node = Node(root_data)

    #keeps track of current best node
    current_best_node = root_node
    #keeps a stack of nodes
    node_stack = []

    def iterative_tree(node):
        taken_stack = []
        while taken_stack != [] or node != None:
            if node != None:
                taken_stack.append(node)
                
                node = node.left
            else:
                node = taken_stack.pop()
                taken_node_data = {
                    #item, room, value, current_best, parent, taken
                    "item": item,
                    "room" : node.data["room"]-weights[item],
                    "value" : node.data["value"]+values[item],
                    "current_best" : node.data["current_best"],
                    "parent" : node,
                    "taken" : node.data["taken"].append(1)
                }
                new_taken_node = Node(taken_node_data)
                node = node.right

    for item in range(0,items-1):
        iterative_tree(root_node)

    return taken_stack

    #sets optimal value to result from running algorithm 1
    # print run_alg_3()
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
