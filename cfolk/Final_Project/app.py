from flask import Flask, render_template, redirect, request, session
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


@app.route('/all')
def read_all():
    users = mongo.db.stock_data.find()
    output = {'All': []}
    # cycle through users
    for user in users:
        symbol = user['symbol']
        historical = user['historical']
        predictions = user['prediction']
        # put symbol in symbol
        out_one = {'symbol': symbol, 'historical': [], 'prediction': []}
        # cycle through historical
        for h in historical:
            # append formatted data to output
            out_one['historical'].append(h)
        
        for p in predictions:
            # append formatted data to output
            out_one['prediction'].append(p)

        output['All'].append(out_one)

    # print(output)
    return output
    
    # , 'historical': user['historical']
if __name__ == '__main__':
    app.run(debug=True)