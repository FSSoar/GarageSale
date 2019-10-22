from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS


createitem = Blueprint('createitem', __name__)



@createitem.route('/')
def index():
    return render_template("createItem.html", userId=1);




@createitem.route('/create/<userId>', methods=["POST"])
def createItem(userId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')



    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')


        retailerID = userId; 
        itemName = request.form['productName']
        availabiltyStartDate = request.form['start']
        availabiltyEndDate = request.form['end']
        description = request.form['description']
        brandName = request.form['brandName']
        categoryId = 1


        
        print(retailerID)
        print(itemName)
        try: 
            insertion = """ Insert INTO Items(retailerID, itemName, availabiltyStartDate, availabiltyEndDate, isCurrentlyAvailable , brandName, categoryId, description  ) 
                                values(%s, %s, %s,%s, %s, %s, %s, %s );"""
            cursor = cnx.cursor()
            cursor.execute(insertion, (retailerID, itemName, availabiltyStartDate, availabiltyEndDate, True, brandName, categoryId, description ))
            cnx.commit()
            return redirect("/")
            
        except: 
            return "ERROR CREATING USER"





