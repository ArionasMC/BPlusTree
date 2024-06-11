from flask import Flask, redirect, url_for, request, render_template
from bplustree import BPlusTree
from tests import create_tree
app = Flask(__name__)

tree = BPlusTree(4)

test_tree = create_tree("trees/tree.txt")

@app.route('/')
def test():
    # Example tree data to be passed to the template
    '''
    tree_data = {
        'root': {
            'keys': [10, 20],
            'children': [
                {'keys': [5], 'children': [], 'is_leaf': True},
                {'keys': [15], 'children': [], 'is_leaf': True},
                {'keys': [25], 'children': [], 'is_leaf': True}
            ],
            'is_leaf': False
        }
    }
    '''
    return render_template('test.html', tree_data=test_tree.getDictTree(), tree_levels=test_tree.getLevelSizes())

@app.route('/index', methods = ['POST', 'GET'])
def index():
    ins = ''
    d = ''
    if request.method == 'POST':
        ins = request.form['insert']
        d = request.form['delete']
    else:
        ins = request.args.get('insert')
        d = request.args.get('delete')
    
    txt = str(ins)
    txt_d = str(d)
    #print(f"ins is:{ins}")
    
    # Process input submission
    if tree.search(txt) == None and txt != '' and ins != None:
        tree.insert(txt, txt)

    # Process delete submission
    if tree.search(txt_d) != None and txt_d != '' and d != None:
        tree.delete(txt_d, txt_d)
    
    return render_template('index.html', tree_str = str(tree).split('\n'))

if __name__ == '__main__':
    app.run(debug = True)