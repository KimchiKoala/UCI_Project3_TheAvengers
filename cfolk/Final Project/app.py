from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from datetime import date
from pymongo import MongoClient
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/stock_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read-one')
def read_one():
    filt = {'Name' : 'ZM'}
    user = db.find_one(filt)
    output = {'historical' : user['historical']}
    #print(output)
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)