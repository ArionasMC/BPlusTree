from bplustree import BPlusTree, Node

def print_keys(node):
    print(node.keys)
    if not(node.is_leaf):
        for n in node.pointers:
            print(n.keys,end=' ')
        print()

def create_tree(file_name):
    f = open(file_name, "r")
    order = int(f.readline())
    height = int(f.readline())
    tree = BPlusTree(order)
    rows = []
    for i in range(height):
        nodes = f.readline().split(",")
        row = []
        for n in nodes:
            keys = list(map(int, n.split("|")))
            node = Node(is_leaf=(i==0))
            node.keys = keys
            row.append(node)
        rows.append(row)

    for i in range(height):
        row = rows[i]
        if i == 0:
            for j in range(len(row)):
                node = row[j]
                for key in node.keys:
                    node.pointers.append(f"{key}")
                if j < len(row)-1:
                    node.pointers.append(row[j+1])
        else:
            offset = 0
            for j in range(len(row)):
                node = row[j]
                for k in range(len(node.keys)+1):
                    node.pointers.append(rows[i-1][offset+k])
                offset += len(node.keys)+1
                    
    tree.root = rows[-1][0]
    f.close()
    return tree

def run_test(id, in_file, out_file, tests):
    in_tree = create_tree(in_file)
    for test in tests:
        parts = test.split(" ")
        key = int(parts[1])
        pointer = f"{key}"
        if parts[0] == "i":
            in_tree.insert(key, pointer)
        elif parts[0] == "d":
            in_tree.delete(key, pointer)
    out_tree = create_tree(out_file)
    eq = str(in_tree) == str(out_tree)
    msg = "OK" if eq else "NOT OK"
    print(f"[TESTING] Test {id}: {msg}!")
    if not(eq):
        print("in_tree is:")
        in_tree.print_tree()
        print("out_tree is:")
        out_tree.print_tree()

if __name__ == "__main__":
    tree = "trees/tree.txt"
    run_test(1, tree, "trees/tree1.txt", ["i 9"])
    run_test(2, tree, "trees/tree2.txt", ["i 3"])
    run_test(3, tree, "trees/tree3.txt", ["d 8"])
    run_test(5, tree, "trees/tree5.txt", ["i 46", "d 52"])
    run_test(6, tree, "trees/tree6.txt", ["d 91"])
    run_test(7, tree, "trees/tree7.txt", ["i 59", "d 91"])
    run_test(8, tree, "trees/tree8.txt", ["d 32","d 39","d 41","d 45","d 73"])

    test_tree = create_tree("trees/tree.txt")
    print(test_tree.getDictTree())
    test_tree.print_tree()
    print(test_tree.getLevelSizes())

    test2 = BPlusTree(5)
    test2.insert(2, '2')
    test2.insert(3, '3')
    test2.insert(4, '4')
    test2.print_tree()
    print(test2.root)
    test2.delete(2, '2')
    test2.delete(3, '3')
    print(test2.root)
    test2.print_tree()