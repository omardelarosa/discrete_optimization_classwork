all_nodes = []

class Node:
    def __init__(self, item, room, value, current_best, parent):
        self.item = item
        self.room = room
        self.value = value
        self.current_best = current_best
        self.parent = parent
        #creates an id for the node that corresponds to its position
        #in the all_nodes array
        self.id = len(all_nodes)
        #adds node to all_nodes
        all_nodes.append(self)

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