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

profile = Blueprint('profile', __name__)

client = pymongo.MongoClient(API_KEYS.getMongoEndPoint())
db = client.cs411
Recommender = db.Recommender

@profile.route('/<profile>')
def index(profile):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')


    namequery = "SELECT firstname, lastName FROM Users WHERE Users.id = %s"
    namecursor = cnx.cursor()
    namecursor.execute(namequery, (profile,))
    name = namecursor.fetchall()
    

    try: 
        query = """ SELECT retailerId, itemName, brandName, description, Items.id, firstname, lastName, email, phoneNumber, zipCode
                    from Items  Left Join Users on Items.retailerId = Users.id
                    where retailerID = %s and ItemName != %s; 
                """
        cursor = cnx.cursor()
        cursor.execute(query, (profile, ""))
        result = cursor.fetchall()

        tquery = """ SELECT retailer.firstName as ownerFirstName, retailer.lastName as ownerLastName, purchase_date, purchasePrice, Items.itemName, Items.brandName, Items.availabiltyEndDate as endTime, Items.availabiltyStartDate as startTime
                    FROM Users as retailer, (Users Inner Join Purchases on Users.id = Purchases.userId) Inner Join Items on Purchases.itemId = Items.id
                    Where Users.id = %s AND retailer.id = retailerID

                """

        tcursor = cnx.cursor()
        tdata = (str(profile), )
        tcursor.execute(tquery, tdata)
        result2 = tcursor.fetchall()
        print(result2)

        return render_template("profile.html", userId=profile, username = name, res= result, transList=result2 );
    except:
        print("ERROR")
        return "error"





@profile.route('/deleteItem/<userID>/<itemID>')
def deleteItem(userID, itemID):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')
    delete = """ Delete from Items where id = %s %s"""
    cursor = cnx.cursor()
    cursor.execute(delete, (itemID, ""))
    cnx.commit()
    ret = Recommender.delete_many( {"itemId" : str(itemID)} )
    
    return redirect("/profile/" + userID)