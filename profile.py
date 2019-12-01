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


    print(profile)
    namequery = "SELECT firstname, lastName FROM Users WHERE Users.id = %s AND '1'=%s"
    namecursor = cnx.cursor()
    namecursor.execute(namequery, (profile, '1'))
    name = namecursor.fetchall()
    print(name)


    

    try: 
        query = """ SELECT retailerId, itemName, brandName, description, Items.id, firstname, lastName, email, phoneNumber, zipCode
                    from Items  Left Join Users on Items.retailerId = Users.id
                    where retailerID = %s and ItemName != %s; 
                """
        cursor = cnx.cursor()
        cursor.execute(query, (profile, ""))
        result = cursor.fetchall()
        print(result)
        return render_template("profile.html", userId=1, username = name, res= result );
    except:
        print("ERROR")



    return render_template("profile.html", userId=1 );



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