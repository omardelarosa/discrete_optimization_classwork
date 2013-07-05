# from collections import defaultdict

# values = [3,8,1,7]
# weights = [5,2,11,4]

# # sum of all values in set
# sigma_values = reduce(lambda x, y: x+y, values)

# # sum of all weights in set
# sigma_weights = reduce(lambda x, y: x+y, weights)

# #a dict to hold item's weights and values
# weights_values = {}
# weights_values['weights'] = weights
# weights_values['values'] = values

# #tree-maker
# def tree(): return defaultdict(tree)

# #convert tree to dict of dicts
# def dicts(t): return {k: dicts(t[k]) for k in t}

# #add or append a new node
# def add_child_node(tree,new_key,new_val):
#     tree[new_key] = new_val
#     return tree[new_key]

# #node 
# other node
# http://www.laurentluce.com/posts/binary-search-tree-library-in-python/

class Node:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        """
        Insert new node with data

        @param data node data object to insert
        """
        if data < self.data:
            if self.left is None:
                self.left = Node(data)
            else:
                self.left.insert(data)
        else:
            if self.right is None:
                self.right = Node(data)
            else:
                self.right.insert(data)

    def lookup(self, data, parent=None):
        """
        Lookup node containing data

        @param data node data object to look up
        @param parent node's parent
        @returns node and node's parent if found or None, None
        """
        if data < self.data:
            if self.left is None:
                return None, None
            return self.left.lookup(data, self)
        elif data > self.data:
            if self.right is None:
                return None, None
            return self.right.lookup(data, self)
        else:
            return self, parent

    
