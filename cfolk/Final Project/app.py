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


# @app.route('/', methods = ['GET', 'POST'])
# def stock():

#     if 'stock' in session:
#         stock = session['stock']

#     if request.method == "POST": 
#         session['stock'] = request.form['stockInput']
#     return print(stock)


#     stock = request.form['stockInput']
#     # print(stock)
#     return stock
#     # stock = None


# #     return render_template('index.html', stock=stock)

                # @app.route('/', methods = ['GET', 'POST'])
                # def index():
                #     if 'stock' in session:
                #         stock = session['stock']


                #     if request.method == "POST": 
                #         stock = request.form['stockInput']
                #         print(stock)
                #     #     # return print(session['stock'])

                #     # if request.method == 'POST':
                #     #     stock = request.form
                #     #     print(stock)

                #     return render_template('index.html')


# @app.route('/read-one')
# def read_one():
#     # filt = {'symbol': stock}
#     # # filt = {'symbol' : 'GOOGL'}
#     # user = mongo.db.stock_data.find_one(filt)
#     # output = {'historical' : user['historical']}
#     # return output
#     return print(stock)

# @app.route('/all')
# def read_all():
#     # users = mongo.db.stock_data.find()
#     # output = {'symbol': users['symbol']}
#     # return jsonify(output)


# # , 'historical' : users['historical']

@app.route('/all')
def read_all():
    users = mongo.db.stock_data.find()
    output = {'All': []}
    # cycle through users
    for user in users:
        symbol = user['symbol']
        historical = user['historical']
        # put symbol in symbol
        out_one = {'symbol': symbol, 'historical': []}
        # cycle through historical
        for h in historical:
            # retrieve information from historical
            out_one['historical'].append(h)
        # append formatted data to output
        output['All'].append(out_one)

    # print(output)
    return output
    
    # , 'historical': user['historical']
if __name__ == '__main__':
    app.run(debug=True)