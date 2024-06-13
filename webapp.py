from flask import Flask, redirect, url_for, request, render_template
from bplustree import BPlusTree
app = Flask(__name__)

tree = None
ttype = True # True for numeric, False for string

@app.route('/tree', methods = ['POST', 'GET'])
def tree_page():
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
    return render_template('tree.html', tree_data=tree.getDictTree())

@app.route('/', methods = ['POST', 'GET'])
def index():
    global tree
    global ttype
    if request.method == 'POST':
        tree_order = request.form['treeOrder']
        tree_type = request.form['treeType']
        if tree_order != None and tree_type != None:
            tree = BPlusTree(int(tree_order))
            ttype = str(tree_type) == 'numeric'
            return redirect(url_for('tree_page'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)