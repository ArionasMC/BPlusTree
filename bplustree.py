# B+ Tree Node can be either root, inner node or leaf
class Node:
    def __init__(self, is_leaf=False):
        # boolean to check if Node is a Leaf Node
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

# B+ Tree class
class BPlusTree:
    def __init__(self, order):
        # tree order
        self.order = order
        # tree root node
        self.root = Node(is_leaf=True)

    def search(self, key):
        current_node = self.__find_leaf(key)
        for i, k in enumerate(current_node.keys):
            if k == key:
                return (current_node, i)
        return None
        
    def __find_leaf(self, key):
        current_node = self.root
        while not current_node.is_leaf:
            i = 0
            while i < len(current_node.keys) and key > current_node.keys[i]:
                i+=1
            current_node = current_node.children[i]
        return current_node

    def insert(self, key):
        leaf = self.root
        if len(self.root.keys) == 0:
            self.root.keys.append(key)
        else:
            leaf = self.__find_leaf(key)
        
            if len(leaf.keys) < self.order-1:
                self.insert_in_leaf(leaf, key)
            else:
                print("Full not implemented yet!")

    def insert_in_leaf(self, leaf, key):
        if key < leaf.keys[0]:
            leaf.keys.insert(0, key)
        else:
            pos = 0
            for i in range(len(leaf.keys)):
                if leaf.keys[i] > key:
                    break
                pos+=1
            leaf.keys.insert(pos, key)

tree = BPlusTree(6)
tree.insert(1)
print(tree.root.keys)
tree.insert(3)
print(tree.root.keys)
tree.insert(5)
print(tree.root.keys)
tree.insert(4)
print(tree.root.keys)
tree.insert(2)
print(tree.root.keys)
tree.insert(8)

    
        


