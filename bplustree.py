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

    def __repr__(self):
        return f"Node({self.keys})"

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

    def test_find(self, key):
        return self.__find_leaf(key)

    def __find_leaf(self, key):
        current_node = self.root
        while not current_node.is_leaf:
            i = 0
            while i < len(current_node.keys) and key >= current_node.keys[i]:
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
        #    print(f"temp={temp},{temp.pointers}")

            leaf_t.pointers.append(leaf.pointers[-1])
            leaf.pointers = [leaf_t]
            leaf.keys.clear()

            border = int(math.ceil(self.order/2))
            leaf.keys = temp.keys[:border]
            leaf.pointers = temp.pointers[:border] + leaf.pointers

            leaf_t.keys = temp.keys[border:]
            leaf_t.pointers += temp.pointers[border:]   # changed this from book
            #leaf_t.pointers = temp.pointers[border:]+leaf_t.pointers
        #    print(f"leaf={leaf},{leaf.pointers},leaf_t={leaf_t},{leaf_t.pointers}")
            '''
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
            '''
            #print(f"leaf={leaf.keys}")
            #print(f"leaf_t={leaf_t.keys}")
            k_t = leaf_t.keys[0] 
            self.__insert_in_parent(leaf, k_t, leaf_t)


    def __get_copy_temp(self, node, full=False):
        temp = Node(is_leaf= node.is_leaf)
        c = 0 if full else 1
        temp.keys = node.keys[:]
        temp.pointers = node.pointers[:len(node.pointers)-c]
        '''
        for i in range(len(node.keys)):
            temp.keys.append(node.keys[i])
        for i in range(len(node.pointers)-c): # algo says until Kn-1 no Pn
            temp.pointers.append(node.pointers[i])
        '''
        return temp

    def __insert_in_leaf(self, leaf, key, pointer):
        if leaf == self.root and len(leaf.keys) == 0:
            leaf.keys = [key]
            leaf.pointers = [pointer]
            return

        if key < leaf.keys[0]:
            leaf.keys.insert(0, key)
            leaf.pointers.insert(0, pointer)
        else:
            self.__add_key_pointer(leaf, key, pointer)
            '''
            pos = 0
            for i in range(len(leaf.keys)):
                if leaf.keys[i] > key:
                    break
                pos+=1
            leaf.keys.insert(pos, key)
            leaf.pointers.insert(pos, pointer) # test this line
            '''

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
            #node_t.parent = node_p
            node_p.keys.insert(index, k_t)                # check that again
            #self.__add_key_pointer(node_p, k_t, node_t)
        else:
            #print(f"Not implemented yet! {node_p==None}")
            temp = self.__get_copy_temp(node_p, full=True)
            index = temp.pointers.index(node)
            temp.pointers.insert(index+1, node_t) # test if +1 is needed
            temp.keys.insert(index, k_t)
            #self.__add_key_pointer(temp, k_t, node_t)            
        #    print(f"parent temp = {temp} from node={node}, node_t={node_t}")

            node_p.keys.clear()
            node_p.pointers.clear()
            node_p_t = Node()
            border = int(math.ceil((self.order+1)/2))
            node_p.keys = temp.keys[:border-1]
            node_p.pointers = temp.pointers[:border]
            #k_tt = node_p.keys[-1]
            k_tt = temp.keys[border-1]
            node_p_t.keys = temp.keys[border:]
            node_p_t.pointers = temp.pointers[border:]
            '''
            if index+1<border:
                node_t.parent = node_p
            else:
                node_t.parent = node_p_t
            '''
        #    print(f"node_p={node_p} - node_p_t={node_p_t}")
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

    def delete(self, key, pointer):
        leaf = self.__find_leaf(key)
        self.__delete_entry(leaf, key, pointer)

    def __add_last_merge_pointer(self, node_t, pointer):
        # node_t is not leaf => pointers are Nodes
        elem = pointer.keys[-1]
        pos = 0
        for node in node_t.pointers:
            comp = node.keys[0]
            if elem < comp:
                break
            pos += 1
        node_t.pointers.insert(pos, pointer)

    def __merge(self, node_t, node, k_t):
        #print(f"before merge{node.is_leaf}: n_t={node_t}:{node_t.pointers}, n={node}:{node.pointers}")
        if not(node.is_leaf): # edo gamietai arketa
        #    print(f"gamietai me {k_t}")
            self.__add_only_key(node_t, k_t)
            #node_t.pointers.insert(node_t.keys.index(k_t)+1, node.pointers[-1]) # index was +1
            test_pos = 0
            for i in range(0, len(node.keys)):
                test_pos = self.__add_key_pointer(node_t, node.keys[i], node.pointers[i])
            #node_t.pointers.insert(test_pos+1, node.pointers[-1])
            self.__add_last_merge_pointer(node_t, node.pointers[-1])

            #node_t.pointers.append(node.pointers[-1])
        else: # edo gamietai ligotero
            #for i in range(0, len(node.keys)):
            #    self.__add_key_pointer(node_t, node.keys[i], node.pointers[i])
            self.__merge_leaf_nodes(node_t, node)
        #    print(f"nt1={node_t.pointers}")
            node_t.pointers[-1] = node.pointers[-1]
            

            # for right edge because there is no pointer, not even None we have to fix this
            if self.__is_right_edge(node):
        #        print("[RIGHT EDGE] Got you!")
                node_t.pointers.pop()

        #    print(f"nt2={node_t.pointers}")
            #if 27 in node.keys: 
            #    print(f"gamiese {node},{node.pointers}-> {node_t},{node_t.pointers}")
        #print(f"after merge: {node_t}:{node_t.pointers}")
    
    def __is_right_edge(self, node):
        cur = self.root
        while not(cur.is_leaf):
            cur = cur.pointers[-1]
        return cur == node

    def __merge_leaf_nodes(self, node_t, node):
        index = 0
        while index < len(node_t.keys):
            if node_t.keys[index] > node.keys[0]:
                break
            index+=1
        for i in range(0, len(node.keys)):
            node_t.keys.insert(index+i, node.keys[i])
            node_t.pointers.insert(index+i, node.pointers[i])
        
    
    def __add_only_key(self, node, key):
        i = 0
        while i < len(node.keys):
            if node.keys[i] > key:
                node.keys.insert(i, key)
                return
            i += 1
        node.keys.append(key)

    def __add_key_pointer(self, node, key, pointer):
        i = 0
        #s = len(node.keys)
        while i < len(node.keys):
            if node.keys[i] > key:
                node.keys.insert(i, key)
                node.pointers.insert(i, pointer)
                return i
            i+=1
        node.keys.append(key)
        #if not(node.is_leaf):
        node.pointers.append(pointer)
        #print("__add_key_pointer append case")
        return i
        #else:
        #    pos = len(node.pointers)-1
        #    node.pointers.insert(pos, pointer)

    def __delete_entry(self, node, key, pointer):
        #print(node.keys)
        node.keys.remove(key)
        node.pointers.remove(pointer)

        elif_cond = len(node.pointers) < int(math.ceil(self.order/2))
        if node.is_leaf:
            elif_cond = len(node.keys) < int(math.ceil((self.order-1)/2))

        if node == self.root and len(node.pointers) == 1:
            self.root = node.pointers[0]
            #self.root.parent = None
            del node
        elif elif_cond:
            node_t, left_sibling = self.__get_sibling(node)
            parent = self.parent(node)
            index = parent.pointers.index(node_t)
            index2 = parent.pointers.index(node)
            k_t = parent.keys[index] if index < index2 else parent.keys[index2] # questionable!!!
            #k_t = parent.keys[index] if left_sibling else parent.keys[index+1]
            if len(node.keys)+len(node_t.keys) <= self.order-1:
                # merging 
                if self.is_pred(node, node_t):
                    #print(f"swapping: {node},{node.pointers} <-> {node_t},{node_t.pointers}")
                    node, node_t = node_t, node
                    #print("=====[Swapped]=====")
                    #print(f"node: {node}, {node.pointers}")
                    #print(f"node_t: {node_t}, {node_t.pointers}")
                    #print("===================")

                #print(f"before __merge: node_t({index}), node({index2}), k_t={k_t}")
                self.__merge(node_t, node, k_t)

                # start of code with issues
                '''
                i = parent.pointers.index(node)
                i_t = parent.pointers.index(node_t)
                if not(node.is_leaf):
                    if i < i_t:
                        node_t.keys.insert(0, k_t)
                        node_t.keys = node.keys + node_t.keys
                        node_t.pointers = node.pointers + node_t.pointers
                    else:
                        node_t.keys.append(k_t)
                        node_t.keys += node.keys
                        node_t.pointers += node.pointers
                else:
                    if i < i_t:
                        node_t.keys = node.keys + node_t.keys
                        node_t.pointers = node.pointers[:self.order-1] + node_t.pointers
                        node_t.pointers.append(node.pointers[-1])
                    else:
                        node_t.keys += node.keys
                        node_t.pointers += node.pointers
                '''
                # end of code with issues (???)
                self.__delete_entry(self.parent(node), k_t, node)
                del node
            else:
                # borrowing
                if self.is_pred(node_t, node): # borrow from left
                    #print(f"borrowing from right: n={node}:{node.pointers}, n_t={node_t}:{node_t.pointers}")
                    if not(node.is_leaf) and not(node == self.root):
                        m_key = node_t.keys.pop()
                        m = node_t.pointers.pop()
                        
                        node.keys.insert(0, k_t)
                        node.pointers.insert(0, m)

                        parent.keys[parent.keys.index(k_t)] = m_key #node_t.keys[-1]
                    else:
                        m_key = node_t.keys.pop()
                        m_pointer = node_t.pointers.pop()
                        
                        node.keys.insert(0, m_key)
                        node.pointers.insert(0, m_pointer)

                        parent.keys[parent.keys.index(k_t)] = m_key
                else: # borrow from right
                    #print(f"Not implemented yet! (symmetric) n={node.keys}, n_t={node_t.keys}")
                    #print(f"borrowing from left: n={node}:{node.pointers}, n_t={node_t}:{node_t.pointers}")
                    if not(node.is_leaf) and not(node == self.root):
                        node_t.keys.pop(0)
                        m = node_t.pointers.pop(0)

                        node.keys.append(k_t)
                        node.pointers.append(m)

                        parent.keys[parent.keys.index(k_t)] =  node_t.keys[0]
                    else:
                        m_key = node_t.keys.pop(0)
                        m_pointer = node_t.pointers.pop(0)

                        node.keys.append(m_key)
                        node.pointers.append(m_pointer)

                        parent.keys[parent.keys.index(k_t)] = node_t.keys[0]
        
    def is_pred(self, node, node_t):
        """
        Returns True if `node` is the predecessor of `node_t`.
        """
        # Find the immediate left sibling of the subtree rooted at node_t
        cur = self.root
        while cur is not node_t:
            idx = self.__find_key(cur, node_t.keys[0])
            if idx > 0 and cur.pointers[idx - 1] is node:
                return True
            cur = cur.pointers[idx]
        
        return False

    def __find_key(self, x, k):
        idx = 0
        while idx < len(x.keys) and x.keys[idx] <= k:
            idx += 1
        return idx

    def __is_predecessor(self, node, node_t):
        return node in self.__get_predecessors(node_t)
        
    def __get_predecessors(self, node):
        pre = []
        parent = self.parent(node)
        while parent != None:
            pre.append(parent)
            parent = self.parent(parent)
        return pre
        
    # Returns a second value: True if sibling is at the left of node otherwise False
    def __get_sibling(self, node):
        parent = self.parent(node) # we are sure the node is not the root
        #print(parent == None, node == None)
        index = parent.pointers.index(node)
        if index > 0:
            return parent.pointers[index-1], True
        else:
            return parent.pointers[index+1], False

    def print_tree(self, debugLeaves = False, showPointers = False):
        nodes = [(0, self.root)]
        leaves = []
        print("=====[Tree]=====")
        last_level = 0
        while len(nodes) != 0:
            (level, node) = nodes.pop(0)
            if last_level != level:
                print()
            if not(showPointers):
                print(node.keys,end=' ')
            else:
                print(node, node.pointers, end=' ')
            if not(node.is_leaf):
                nodes += [(level+1, node.pointers[i]) for i in range(len(node.pointers))]
            else:
                leaves += node.pointers
            last_level = level

        print()
        if debugLeaves:
            print(leaves)

    # for testing purposes
    def __str__(self):
        result = ""
        nodes = [(0, self.root)]
        last_level = 0
        while len(nodes) != 0:
            (level, node) = nodes.pop(0)
            if last_level != level:
                result += "\n"
            result += f"{node.keys} "
            if not(node.is_leaf):
                nodes += [(level+1, node.pointers[i]) for i in range(len(node.pointers))]
            last_level = level
        return result

if __name__ == '__main__':      
    tree = BPlusTree(4)
    nodes = 29
    for i in range(1, nodes):
        tree.insert(i, f"value{i}")
    tree.print_tree(debugLeaves=False)

    for i in range(1, nodes):
        print(tree.test_find(i).pointers)
    print("---> 27 pointers:",tree.test_find(27).pointers)
    tree.delete(28, "value28")
    
    tree.print_tree(showPointers=False)

    #print(tree.test_find(13).keys)
    #node = tree.root.pointers[0].pointers[1]
    #print(node.keys)
    #print(tree.root.pointers[-1].pointers[-1].pointers[0].keys, tree.root.pointers[-1].pointers[-1].pointers[1].keys)
    #print(tree.test_find(26).keys, tree.test_find(28).keys, tree.is_pred(tree.test_find(26), tree.test_find(28)))

    #tree.delete(6, "value6")
    #tree.delete(8, "value8")
    #tree.delete(2, "value2")
    #tree.delete(26, "value26") # borrowing!
    
    #tree.insert(26.1, "value26.1")
    #print(f"before: {tree.test_find(25).pointers}, {tree.test_find(28).pointers}")
    #print(tree.is_pred(tree.test_find(26), tree.test_find(28)))

    #tree.delete(28, "value28")
    #print(f"after del 28: {tree.test_find(25).pointers}")

    #tree.delete(25, "value25")
    #tree.print_tree()
    
    #print(tree.test_find(25).pointers) # issues!!!!!!
    #print(tree.test_find(1).pointers)
    #print(tree.parent(tree.test_find(25)).keys, tree.parent(tree.test_find(25)).pointers)

    '''
    tree.insert(12.1, "value12.1")
    tree.insert(16.1, "value16.1")
    tree.print_tree()
    tree.delete(13, "value13")
    tree.print_tree()
    '''
    #print(tree.is_pred(tree.root.pointers[0].pointers[0], tree.root.pointers[1].pointers[0]))
    
    #print()
    #print(tree.parent(tree.root.pointers[0].pointers[-1]).keys)