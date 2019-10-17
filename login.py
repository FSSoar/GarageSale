from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template
from flask import Blueprint
import API_KEYS


login  = Blueprint('login', __name__)


@login.route('/')
def index(): 
    #render HTML Here 
    return 'hi'



@login.route('/validate')
def loginUser(): 

    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')


    email = request.args.get('email')
    password = request.args.get('password')

    

    try: 
        query = """ SELECT *
                    from Users 
                    Where email = %s and password = %s; 
                """
        cursor = cnx.cursor()
        cursor.execute(query, (email, password))
        result = cursor.fetchall()


        return jsonify(len(result) > 0)

    except:
        return jsonify(False)