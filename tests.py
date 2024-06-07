from bplustree import BPlusTree

def print_keys(node):
    print(node.keys)
    if not(node.is_leaf):
        for n in node.pointers:
            print(n.keys,end=' ')
        print()

tree = BPlusTree(order=4)
nodes = 11
for i in range(1, nodes):
    tree.insert(i, f'value{i}')
for i in range(1, nodes):
        print(tree.test_find(i).pointers)
#tree.delete(12, "value12")
#tree.delete(9, "value9")
#tree.insert(4, "value4")
#for i in range(1, nodes+1):
#        print(tree.test_find(i).pointers)
tree.print_tree(showPointers=True)
print(tree.root.pointers)

#tree.delete(7, "value7")
tree.delete(6, "value6")
tree.print_tree(showPointers=True)
tree.delete(8, "value8")
tree.print_tree(showPointers=True)

tree.delete(1, "value1")
tree.print_tree(showPointers=True)
tree.delete(7, "value7")
tree.delete(9, "value9")
tree.print_tree()
tree.print_tree(showPointers=True)
#print_keys(tree.root.pointers[0])
#print_keys(tree.root.pointers[1])

#for i in range(1, nodes):
#    print(tree.test_find(i).keys, end=' ')
#print()