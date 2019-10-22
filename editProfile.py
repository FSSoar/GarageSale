from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS


editProfile = Blueprint('editProfile', __name__)



@editProfile.route('/<profile>')
def index(profile):

    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')



    try: 
        query = """ SELECT *
                    from Users 
                    Where id = %s %s; 
                """
        cursor = cnx.cursor()
        cursor.execute(query, (profile, ""))
        result = cursor.fetchall()
        print(result)


        return render_template("editProfile.html", res= result[0])

    except:
        return None



@editProfile.route('/update/<userId>', methods=["POST"])
def createItem(userId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')



    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')


        retailerID = userId; 
        first = request.form['first']
        last = request.form['last']
        email = request.form['email']
        phoneNum = request.form['phoneNum']
        zipC = request.form['zip']


        try: 
            insertion = """ Update Users Set  firstName = %s,  lastName = %s, email = %s, phoneNumber = %s, zipCode = %s where id = %s  """
            cursor = cnx.cursor()
            cursor.execute(insertion, (first, last, email, phoneNum, zipC, retailerID ))
            cnx.commit()
            return redirect("/profile/" + userId)
            
        except: 
            return "ERROR CREATING USER"




    
    