class Node:
    def __init__(self, data_dict):
        #need to refactor so that it takes an options dictionary called 'data'
        #item, room, value, current_best, parent, taken
        self.data = data_dict
        # self.data["item"] = data_dict["item"]
        # self.data["room"] = data_dict["room"]
        # self.data["value"] = data_dict["value"]
        # self.data["current_best"] = data_dict["current_best"]
        # self.data["parent"] = data_dict["parent"]
        # #is taken?
        # self.data["taken"] = data_dict["taken"]
        #creates an id for the node that corresponds to its position
        #in the all_nodes array
        # self.data["id"] = data_dict["id"]
        #adds node to all_nodes
        # all_nodes.append(self)
        if data_dict["current_best_node"] != False:
            self.data["current_best_node"] = self
        else:
            self.data["current_best_node"] = data_dict["current_best_node"]

    # def inorder(node):
    #   if node == null:
    #     # return node
    #     print node
    #   else: 
    #     # inorder(node.left)
    #     # visit(node)
    #     # inorder(node.right)
    #     print "Traversed"

    def get_path(self,acc_array,items):

        #make empty array for all item index
        if acc_array == []:
            for n in range(0,items):
                acc_array.append(0)

        if self.data["parent"] == None:
            return acc_array
        else:
            acc_array[self.data["item"]] = self.data["taken"]
            
            # print "At "+str(count)+"..."
            # print "Acc Array: "
            # print acc_array
            return self.data["parent"].get_path(acc_array,items)
            

    def left_taken(self,item):
        #make taken node
        next_node_data = {
                #item, room, value, current_best, parent, taken
                "item": item,
                "room" : self.data["room"]-weights[item],
                "value" : self.data["value"]+values[item],
                "current_best" : self.data["current_best"],
                "current_best_node" : self.data["current_best_node"],
                "parent" : self,
                "taken" : 1
        }
        return Node(next_node_data)

    def right_not_taken(self,item):
        #make taken node
        next_node_data = {
            #item, room, value, current_best, parent, taken
            "item": item,
            "room" : self.data["room"],
            "value" : self.data["value"],
            "current_best" : self.data["current_best"]-values[item],
            "current_best_node" : self.data["current_best_node"],
            "parent" : self,
            "taken" : 0
        }
        return Node(next_node_data)

    def to_s(self):
        print "================="
        print "My item index is " + str(self.data["item"])
        # print "My id is " + str(self.data["id"])
        print "My room is " + str(self.data["room"])
        print "My value is " + str(self.data["value"])
        print "My parent is " + str(self.data["parent"])
        print "================="

    def is_root():
        if self.data["parent"] == None:
            return True
        else:
            return False

    # def is_sibling_less_valuable(self):
    #     siblings_array = self.get_siblings
    #     if self.value > siblings_array[1]:
    #         return True
    #     else:
    #         return False