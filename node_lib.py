class Node:
    def __init__(self, data_dict):
        #need to refactor so that it takes an options dictionary called 'data'
        #item, room, value, current_best, parent, taken
        self.data = {}
        self.data["item"] = data_dict["item"]
        self.data["room"] = data_dict["room"]
        self.data["value"] = data_dict["value"]
        self.data["current_best"] = data_dict["current_best"]
        self.data["parent"] = data_dict["parent"]
        #is taken?
        self.data["taken"] = data_dict["taken"]
        #creates an id for the node that corresponds to its position
        #in the all_nodes array
        # self.data["id"] = data_dict["id"]
        #adds node to all_nodes
        # all_nodes.append(self)

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
            

    # def get_siblings(self):
    #     return filter(lambda node: True if node.data["item"] == self.data["item"] and node.data["parent"] == self.data["parent"] else False, all_nodes)

    # def get_all_nodes_at_same_level(self):
    #     return filter(lambda node: True if node.data["item"] == self.data["item"] else False, all_nodes)

    def to_s(self):
        print "================="
        print "My item index is " + str(self.data["item"])
        print "My id is " + str(self.data["id"])
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