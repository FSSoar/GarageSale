from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect, abort
from flask import Blueprint
import API_KEYS

# from profile import profile

login  = Blueprint('login', __name__)

@login.route('/')
def index(): 
    #render HTML Here 
    return render_template("login.html")



@login.route('/validate', methods=['POST'])
def loginUser(): 
    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')

        email = request.form['email']
        password = request.form['password']
        print(request.form)
        try: 
            query = """ SELECT *
                        from Users 
                        Where email = %s and password = %s; 
                    """
            cursor = cnx.cursor()
            cursor.execute(query, (email, password))
            result = cursor.fetchall()
            
            success = len(result) > 0

            if success:
                info = result[0]
                userid = info[0]
                return redirect('/profile/' + str(userid))
            else:
                abort(401)

        except:
            print('ERROR')
            abort(401)