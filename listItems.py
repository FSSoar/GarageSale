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

listItems = Blueprint('listItems', __name__)

client = pymongo.MongoClient(API_KEYS.getMongoEndPoint())
db = client.cs411
Recommender = db.Recommender

def stringifyarray(a):
    ans = ""
    for astring in a:
        ans += astring
        ans += " "
    return ans


@listItems.route('/')
def login():
    return redirect("/login");


@listItems.route('/<userId>')
def index(userId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')

    try: 
        query = """ SELECT retailerId, itemName, brandName, description, Items.id, firstname, lastName, email, phoneNumber, zipCode, price
                    from Items  Left Join Users on Items.retailerId = Users.id
                    where ItemName !="" and isCurrentlyAvailable = true; 
                """
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        ret = Recommender.find_one({"personId": str(userId)})
        itemsToCompare = ret['items']
        compString = stringifyarray(itemsToCompare)
        recs = Recommender.find({"$text": {"$search": compString}}, {"score": {'$meta': 'textScore'}}).sort([('score', {'$meta':'textScore'})])
        idlist = []
        n = recs.count()
        count = 0
        orString = ""
        for doc in recs:
            count += 1
            currId = doc['personId']
            if currId == str(userId):
                continue 
        
            if count == n:
                orString += doc['personId']
            else:
                orString += str(doc['personId'])+","

        namequery = (""" SELECT firstname, lastName 
                        FROM Users 
                        WHERE id IN ( """+orString+""" )
                    """) 
        namecursor = cnx.cursor()
        namecursor.execute(namequery)
        thename = namecursor.fetchall()
        return render_template("listAll.html", res= result, userId=userId, names = thename );
    except:
        print("ERROR")



    return render_template('listAll.html', userId=userId)





@listItems.route('purchase/<userId>/<itemId>')
def purchaseItem(userId, itemId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')


    # ADD ITEM TO PURCHASES TABLE 
    # TRIGGER IN 

    price = request.args.get('price')
    

    try: 
        query = """ INSERT INTO Purchases(itemId, userId, purchasePrice) values (%s, %s, %s); 
                """
        query2 = """Update Items 
                    Set	isCurrentlyAvailable = %s
                    Where id = %s;
                """
        cursor = cnx.cursor()
        cursor.execute(query, (itemId, userId, price))
        cnx.commit()
        cursor.execute(query2, (False, itemId))
        cnx.commit()

        # print(itemId)
        ret = Recommender.find_one({"personId": str(userId)})
        if ret == None:
            print("here!")
            dictToInsert = {"personId": str(userId)}
            Recommender.insert_one(dictToInsert)
        Recommender.update_one(
            {"personId": str(userId)},
            {
                "$push": {
                    "items": {
                        "$each": [str(itemId)],
                        "$sort": 1
                    }
                }
            }
        )

        return redirect('/items/completePurchase/'+ userId)
    except Exception as e:
        print(e)



    return render_template('listAll.html', userId=userId)



@listItems.route('/completePurchase/<userId>')
def completeTransaction(userId):
    return render_template("FinishTransaction.html", userId = userId)