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

createitem = Blueprint('createitem', __name__)

client = pymongo.MongoClient(API_KEYS.getMongoEndPoint())
db = client.cs411
Recommender = db.Recommender


@createitem.route('/')
def login():
    return redirect("/login");


@createitem.route('/<userId>')
def index(userId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')
    try:
        query = """ SELECT categoryId, AVG(price)
                    from Items
                    GROUP BY categoryId;
                """
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return render_template("createItem.html", userId=userId, avgPrices=result)
    except:
        return "error"


@createitem.route('/update/create/<userId>/<itemId>', methods=["POST"])
def updateItem(userId, itemId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')



    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')
        itemName = request.form['productName']
        availabiltyStartDate = request.form['start']
        availabiltyEndDate = request.form['end']
        description = request.form['description']
        brandName = request.form['brandName']
        price = request.form['price']

        try:
            insertion = """ Update Items Set  itemName = %s,  availabiltyStartDate = %s, availabiltyEndDate = %s, description = %s, brandName = %s, price = %s where id = %s  """
            cursor = cnx.cursor()
            cursor.execute(insertion, (itemName, availabiltyStartDate, availabiltyEndDate, description, brandName, price, itemId ))
            cnx.commit()
            return redirect("/profile/" + userId)

        except:
            return "ERROR CREATING USER"
    return ""

@createitem.route('/update/<userId>/<item>')
def editItem(userId, item):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')



    try:
        query = """ SELECT *
                    from Items
                    Where id = %s %s;
                """
        cursor = cnx.cursor()
        cursor.execute(query, (item, ""))
        result = cursor.fetchall()
        print(result[0])
        return render_template("updateItem.html", userId=userId, res= result[0])

    except:
        return None



@createitem.route('/create/<userId>', methods=["POST"])
def createItem(userId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')


    if request.method == 'POST':

        retailerID = userId;
        itemName = request.form['productName']
        availabiltyStartDate = request.form['start']
        availabiltyEndDate = request.form['end']
        description = request.form['description']
        brandName = request.form['brandName']
        categoryId = request.form['category']
        price = request.form['price']
        print(price)
        try:
            insertion = """ Insert INTO Items(retailerID, itemName, availabiltyStartDate, availabiltyEndDate, isCurrentlyAvailable , brandName, categoryId, description, price  )
                                values(%s, %s, %s,%s, %s, %s, %s, %s, %s );"""
            cursor = cnx.cursor()
            ans = cursor.execute(insertion, (retailerID, itemName, availabiltyStartDate, availabiltyEndDate, True, brandName, categoryId, description, price ))
            cnx.commit()
            dictToInsert = { "newItem":str(cursor.lastrowid), "owner": int(userId) }
            Recommender.insert_one(dictToInsert)
            return redirect("/profile/"+str(userId))

        except:
            return "ERROR CREATING USER"
