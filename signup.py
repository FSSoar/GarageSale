from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS


signup  = Blueprint('signup', __name__)


@signup.route('/')
def index(): 
    #render HTML Here 
    return render_template("signUp.html");



@signup.route('/create/user', methods=['POST'])
def createUser(): 
    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')


        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        zipCode = request.form['zipCode']
        password = request.form['password']

        try: 
            insertion = "Insert INTO Users(firstName, lastName, email,phoneNumber,zipCode, password  ) values(%s, %s, %s,%s, %s, %s);"
            cursor = cnx.cursor()
            cursor.execute(insertion, (firstName, lastName, email, phoneNumber, zipCode, password ))
            cnx.commit()

            userId = cursor.lastrowid
            print(userId)
            print("/profile/" + str(userId))
            ret = Recommender.find_one({"personId": str(userId)})
            if ret == None:
                dictToInsert = {"personId": str(userId)}
                Recommender.insert_one(dictToInsert)
            
            return redirect("/profile/" + str(userId))
        except: 
            return "ERROR CREATING USER. Refresh the page and try again"
