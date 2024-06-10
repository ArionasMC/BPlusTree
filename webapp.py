from flask import Flask, redirect, url_for, request, render_template
from bplustree import BPlusTree
app = Flask(__name__)

tree = BPlusTree(4)

@app.route('/', methods = ['POST', 'GET'])
def index():
    txt = ''
    if request.method == 'POST':
        txt = str(request.form['insert'])
    else:
        txt = str(request.args.get('insert'))
    
    print(f"txt is:{txt}")
    if tree.search(txt) == None:
        tree.insert(txt, txt)
    
    return render_template('index.html', tree_str = str(tree).split('\n'))

if __name__ == '__main__':
    app.run(debug = True)