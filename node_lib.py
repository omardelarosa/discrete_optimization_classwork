all_nodes = []

class Node:
    def __init__(self, item, room, value, current_best, parent, taken):
        #need to refactor so that it takes an options dictionary called 'data'
        self.item = item
        self.room = room
        self.value = value
        self.current_best = current_best
        self.parent = parent
        #is taken?
        self.taken = taken
        #creates an id for the node that corresponds to its position
        #in the all_nodes array
        self.id = len(all_nodes)
        #adds node to all_nodes
        all_nodes.append(self)

    def get_path(self,acc_array):
        if self.parent == None:
            return acc_array
        else:
            acc_array.append(self.taken)
            return self.parent.get_path(acc_array)
            

    def get_siblings(self):
        return filter(lambda node: True if node.item == self.item and node.parent == self.parent else False, all_nodes)

    def get_all_nodes_at_same_level(self):
        return filter(lambda node: True if node.item == self.item else False, all_nodes)

    def to_s(self):
        print "================="
        print "My item index is " + str(self.item)
        print "My id is " + str(self.id)
        print "My room is " + str(self.room)
        print "My value is " + str(self.value)
        print "My parent is " + str(self.parent)
        print "================="

    def is_root():
        if self.parent == None:
            return True
        else:
            return False

    # def is_sibling_less_valuable(self):
    #     siblings_array = self.get_siblings
    #     if self.value > siblings_array[1]:
    #         return True
    #     else:
    #         return False