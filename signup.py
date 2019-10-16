from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template
from flask import Blueprint
import API_KEYS


signup  = Blueprint('signup', __name__)


@signup.route('/')
def index(): 
    #render HTML Here 
    return 'hi'



@signup.route('/create/user',  methods=['POST'])
def createUser(): 

    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')


    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    email = request.args.get('email')
    phoneNumber = request.args.get('phoneNumber')
    zipCode = request.args.get('zipCode')

    try: 
        insertion = "Insert INTO Users(firstName, lastName, email,phoneNumber,zipCode  ) values(%s, %s, %s,%s, %s);"
        cursor = cnx.cursor()
        cursor.execute(insertion, (firstName, lastName, email, phoneNumber, zipCode ))
        cnx.commit()
        return jsonify({"passed": True})
    except: 
        return "ERROR CREATING USER"
