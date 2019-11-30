from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS

import pymongo
from bson.code import Code
import pprint

mongotest = Blueprint('mongotest', __name__)
client = pymongo.MongoClient(API_KEYS.getMongoEndPoint())
db = client.cs411
prices = db.prices

@mongotest.route('/')
def testMongo():
    pipeline = [
        {"$group": {"_id": "$productName", "totalPrice": {"$sum": "$price"}, "count": {"$sum": 1}} },
        {"$project": {"_id": 0, "itemName":"$_id", "totalPrice": 1, "count":1}},
        {"$sort": {"itemName":1}}
    ]
    result = prices.aggregate(pipeline)
    suggestPrice = {}
    for doc in result:
        p = doc['totalPrice'] / doc['count']
        if doc['itemName'] is None:
            suggestPrice['hihi'] = p
        else:
            suggestPrice[doc['itemName']] = p
    # for doc in collection.find():
    #     pprint.pprint(doc)
    
    # print(suggestPrice)
    return render_template('mongotest.html', avgPrices = suggestPrice ) 

@mongotest.route('/additem', methods=['POST'])
def addmongoItem():
    if request.method == 'POST':
        print(request.form)
        prodName = request.form['prodname']
        rating = request.form['rating']
        price = request.form['price']
        details = request.form['details']

        prodname = prodName.lower().capitalize()
        try:
            rating = int(rating)
        except:
            rating = 0
        
        try:
            price = float(price)
        except:
            price = 0

        mydict = {'productName': prodName, 'condition': rating, 'price':price, 'notes': details}

        print(mydict)

        return redirect('/mongotest')

# @mongotest.route('/_suggestprice')
# def reqMongo():
    