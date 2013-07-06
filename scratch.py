all_nodes = []

class Node:
    def __init__(self, level, room, value, current_best, parent, taken_bool):
        self.level = level
        self.room = room
        self.value = value
        self.current_best = best
        self.parent = parent
        self.taken = taken_bool
        #creates an id for the node that corresponds to its position
        #in the all_nodes array
        self.id = len(all_nodes)
        #adds node to all_nodes
        all_nodes.append(self)

    def get_siblings(self):
        filter(lambda node: True if node.level == self.level and node.parent == self.parent else False, all_nodes)

    def to_s(self):
        print "My level is " + str(self.level)
        print "My room is " + str(self.room)
        print "My value is " + str(self.value)
        print "My parent is " + str(self.parent)

    def is_root():
        if self.parent == None:
            return True
        else:
            return False

