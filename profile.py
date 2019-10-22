from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS


profile = Blueprint('profile', __name__)



@profile.route('/<profile>')
def index(profile):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')




    

    try: 
        query = """ SELECT retailerId, itemName, brandName, description, Items.id, firstname, lastName, email, phoneNumber, zipCode
                    from Items  Left Join Users on Items.retailerId = Users.id
                    where retailerID = %s and ItemName != %s; 
                """
        cursor = cnx.cursor()
        cursor.execute(query, (profile, ""))
        result = cursor.fetchall()
        print(result)
        return render_template("profile.html", userId=1, res= result );
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
    
    
    return redirect("/profile/" + userID)