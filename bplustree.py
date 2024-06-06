import math

# B+ Tree Node can be either root, inner node or leaf
class Node:
    def __init__(self, is_leaf=False):
        # boolean to check if Node is a Leaf Node
        self.is_leaf = is_leaf
        self.keys = []
        # pointers are children nodes for the non-leaf nodes
        # and records for the leaf nodes except the last
        # one which is the next leaf node
        # in general len(pointers) = len(keys)+1
        self.pointers = []
        #self.parent = None

# B+ Tree class
class BPlusTree:
    def __init__(self, order):
        # tree order
        self.order = order
        # tree root node
        #self.root = Node(is_leaf=True)
        self.root = None

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
            current_node = current_node.pointers[i]
        return current_node

    def insert(self, key, pointer):
        leaf = None
        if self.root == None:
            self.root = Node(is_leaf=True)
            leaf = self.root
        else:
            leaf = self.__find_leaf(key)

        if len(leaf.keys) < self.order-1:
            self.__insert_in_leaf(leaf, key, pointer)
        else:
            #print("Full not implemented yet!")
            leaf_t = Node(is_leaf=True)
            temp = self.__get_copy_temp(leaf)
            self.__insert_in_leaf(temp, key, pointer)
            
            lpn = leaf.pointers[-1]
            leaf.keys.clear()
            leaf.pointers.clear()

            border = int(math.ceil(self.order/2))
            leaf.keys = temp.keys[:border]
            leaf.pointers = temp.pointers[:border]
            leaf.pointers.append(leaf_t)                # L.Pn = L'

            leaf_t.keys = temp.keys[border:]
            leaf_t.pointers = temp.pointers[border:]
            leaf_t.pointers.append(lpn)                # L'.Pn = L.Pn

            #print(f"leaf={leaf.keys}")
            #print(f"leaf_t={leaf_t.keys}")
            k_t = leaf_t.keys[0] 
            self.__insert_in_parent(leaf, k_t, leaf_t)


    def __get_copy_temp(self, node, full=False):
        temp = Node(is_leaf= node.is_leaf)
        c = 0 if full else 1
        for i in range(len(node.keys)):
            temp.keys.append(node.keys[i])
        for i in range(len(node.pointers)-c): # algo says until Kn-1 no Pn
            temp.pointers.append(node.pointers[i])
        return temp

    def __insert_in_leaf(self, leaf, key, pointer):
        if len(leaf.keys) == 0 or key < leaf.keys[0]:
            leaf.keys.insert(0, key)
            leaf.pointers.insert(0, pointer)
        else:
            pos = 0
            for i in range(len(leaf.keys)):
                if leaf.keys[i] > key:
                    break
                pos+=1
            leaf.keys.insert(pos, key)
            leaf.pointers.insert(pos, pointer) # test this line

    def __insert_in_parent(self, node, k_t, node_t):
        if node == self.root:
            #print("found root!")
            node_r = Node()
            node_r.keys = [k_t]
            node_r.pointers = [node, node_t]
            #node.parent = node_r
            #node_t.parent = node_r
            self.root = node_r
            return
        
        #node_p = node.parent
        node_p = self.parent(node)
        if len(node_p.pointers) < self.order:
            index = node_p.pointers.index(node)
            node_p.pointers.insert(index+1, node_t)
            node_t.parent = node_p
            node_p.keys.insert(index, k_t)
        else:
            #print(f"Not implemented yet! {node_p==None}")
            temp = self.__get_copy_temp(node_p, full=True)
            index = temp.pointers.index(node)
            temp.pointers.insert(index+1, node_t) # test if +1 is needed
            temp.keys.insert(index+1, k_t)

            node_p.keys.clear()
            node_p.pointers.clear()
            node_p_t = Node()
            border = int(math.ceil((self.order+1)/2))
            node_p.keys = temp.keys[:border]
            node_p.pointers = temp.pointers[:border]
            k_tt = node_p.keys[-1]
            node_p_t.keys = temp.keys[border:]
            node_p_t.pointers = temp.pointers[border:]
            '''
            if index+1<border:
                node_t.parent = node_p
            else:
                node_t.parent = node_p_t
            '''
            self.__insert_in_parent(node_p, k_tt, node_p_t)

    def parent(self, node):
        if self.root == node:
            return None
        return self.__find_parent(self.root, node)

    def __find_parent(self, current_node, child_node):
        if current_node.is_leaf:
            return None
        for child in current_node.pointers:
            if child == child_node:
                return current_node
            parent = self.__find_parent(child, child_node)
            if parent:
                return parent
        return None

    def delete(self, key):
        leaf = self.__find_leaf(key)
        self.__delete_entry(leaf, key)

    def __delete_entry(self, node, key, pointer=None):
        node.keys.remove(key)
        if pointer != None:
            node.pointers.remove(pointer)

        if node == self.root and len(node.pointers) == 1:
            self.root = node.pointers[0]
            self.root.parent = None
            del node
        

    def print_tree(self):
        nodes = [(0, self.root)]

        last_level = 0
        while len(nodes) != 0:
            (level, node) = nodes.pop(0)
            if last_level != level:
                print()
            print(node.keys,end=' ')
            if not(node.is_leaf):
                nodes += [(level+1, node.pointers[i]) for i in range(len(node.pointers))]
            last_level = level
            
tree = BPlusTree(4)
for i in range(1, 30):
    tree.insert(i, f"value{i}")
tree.print_tree()
print()
print(tree.parent(tree.root.pointers[0].pointers[-1]).keys)