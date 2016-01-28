#!../venv/bin/python

from differ import Differ
from flask import Flask, url_for, render_template, redirect, jsonify

app = Flask(__name__)

global globalDiffer
globalDiffer = Differ()

@app.route('/v1/index')
def index():
    return render_template('index.html', state=globalDiffer.getState())

@app.route('/info')
def get_info():
    return globalDiffer.getState()

@app.route('/v1/diff/setleft', methods=['GET'])
def set_left():
    return render_template('left.html', left=globalDiffer.left)

@app.route('/v1/diff/setright', methods=['GET'])
def set_right():
    return render_template('right.html', right=globalDiffer.right)

@app.route('/v1/diff/left/<string:leftjson>', methods=['GET'])
def left(leftjson):
    globalDiffer.left=leftjson
    return redirect("http://localhost:5000/v1/index", code=302)

@app.route('/v1/diff/right/<string:rightjson>', methods=['GET'])
def right(rightjson):
    globalDiffer.right=rightjson
    return redirect("http://localhost:5000/v1/index", code=302)

@app.route('/v1/diff', methods=['GET'])
def diff():
    #return jsonify(globalDiffer.Diff())
    #for now, I will return the json as plan-text..
    #for some reason jeasonify is not converting my json in text mode
    return globalDiffer.Diff()


if __name__ == '__main__':
        app.run(debug=True)

