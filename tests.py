from bplustree import BPlusTree

def print_keys(node):
    print(node.keys)
    if not(node.is_leaf):
        for n in node.pointers:
            print(n.keys,end=' ')
        print()

tree = BPlusTree(order=4)
nodes = 30
for i in range(1, nodes):
    tree.insert(i, f'value{i}')
tree.print_tree()

print_keys(tree.root.pointers[0])
print_keys(tree.root.pointers[1])

for i in range(1, nodes):
    print(tree.test_find(i).keys, end=' ')
print()