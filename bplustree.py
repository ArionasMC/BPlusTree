import math

# B+ Tree Node can be either root, inner node or leaf
class Node:
    def __init__(self, is_leaf=False):
        # boolean to check if Node is a Leaf Node
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.parent = None

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
                self.__insert_in_leaf(leaf, key)
            else:
                #print("Full not implemented yet!")
                leaf_t = Node(is_leaf=True)
                temp = self.__get_copy_temp(leaf)
                self.__insert_in_leaf(temp, key)
                
                leaf.keys.clear()
                leaf.children.clear()

                border = int(math.ceil(self.order/2))
                leaf.keys = temp.keys[:border]
                leaf.children = temp.children[:border]
                leaf_t.keys = temp.keys[border:]
                leaf_t.children = temp.children[border:]

                #print(f"leaf={leaf.keys}")
                #print(f"leaf_t={leaf_t.keys}")
                k_t = leaf_t.keys[0] 
                self.__insert_in_parent(leaf, k_t, leaf_t)


    def __get_copy_temp(self, node):
        temp = Node(is_leaf= node.is_leaf)
        for i in range(len(node.keys)):
            temp.keys.append(node.keys[i])
        for i in range(len(node.children)):
            temp.children.append(node.children[i])
        return temp

    def __insert_in_leaf(self, leaf, key):
        if key < leaf.keys[0]:
            leaf.keys.insert(0, key)
        else:
            pos = 0
            for i in range(len(leaf.keys)):
                if leaf.keys[i] > key:
                    break
                pos+=1
            leaf.keys.insert(pos, key)

    def __insert_in_parent(self, node, k_t, node_t):
        if node == self.root:
            #print("found root!")
            node_r = Node()
            node_r.keys = [k_t]
            node_r.children = [node, node_t]
            node.parent = node_r
            node_t.parent = node_r
            self.root = node_r
            return
        
        node_p = node.parent
        if len(node_p.children) < self.order:
            index = node_p.children.index(node)
            node_p.children.insert(index+1, node_t)
            node_t.parent = node_p
            node_p.keys.insert(index, k_t)
        else:
            print(f"Not implemented yet! {node_p==None}")
            temp = self.__get_copy_temp(node_p)
            index = temp.children.index(node)
            temp.children.insert(index+1, node_t)
            temp.keys.insert(index, k_t)

            node_p.keys.clear()
            node_p.children.clear()
            node_p_t = Node()
            border = int(math.ceil((self.order+1)/2))
            node_p.keys = temp.keys[:border]
            node_p.children = temp.children[:border]
            k_tt = node_p.keys[-1]
            node_p_t.keys = temp.keys[border:]
            node_p_t.children = temp.children[border:]

            if index+1<border:
                node_t.parent = node_p
            else:
                node_t.parent = node_p_t

            self.__insert_in_parent(node_p, k_tt, node_p_t)


    def print_tree(self):
        nodes = [(0, self.root)]

        last_level = 0
        while len(nodes) != 0:
            (level, node) = nodes.pop(0)
            if last_level != level:
                print()
            print(node.keys,end=' ')
            nodes += [(level+1, node.children[i]) for i in range(len(node.children))]
            last_level = level
            
tree = BPlusTree(4)
for i in range(1, 30):
    tree.insert(i)
tree.print_tree()