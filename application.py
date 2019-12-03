from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect

from signup import signup
from login import login
from createitem import createitem
from profile import profile 
from editProfile import editProfile
from listItems import listItems
from search import search
from mongotest import mongotest
from flask import redirect
import requests
import API_KEYS

application = Flask(__name__)
application.register_blueprint(signup, url_prefix="/signUp" )
application.register_blueprint(login, url_prefix="/login" )
application.register_blueprint(createitem, url_prefix="/createItem" )
application.register_blueprint(profile, url_prefix="/profile" )
application.register_blueprint(editProfile, url_prefix="/editProfile" )
application.register_blueprint(listItems, url_prefix="/items" )
application.register_blueprint(search, url_prefix="/search" )
application.register_blueprint(mongotest, url_prefix='/mongotest')

# global mail.init_app(application)



@application.route('/')
def hello_world():

    return redirect("/login");



application.config['MAIL_SERVER']= 'smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'garagesalecs411@gmail.com'
application.config['MAIL_PASSWORD'] = 'rootroot'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
mail = Mail(application)

@application.route('/mail/<userId>/<productId>/<price>')
def sendMail(userId, productId, price):
    print(userId)
    print(productId)

    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')

    query = """ Select email, itemName, description, firstName
                    From 
                    (Select * 
                    From Items 
                    Where id = %s) as a Left Join Users on retailerId = Users.id;"""

    queryBuyer = """Select * from Users where id = %s; """

    cursor = cnx.cursor()
    cursor.execute(query, (productId, ))
    sellerData = cursor.fetchall()[0]

    cursor = cnx.cursor()
    cursor.execute(queryBuyer, (userId, ) )
    buyerData = cursor.fetchall()[0]
    print(buyerData)

    msg = Message("New Transaction Alert",
                    sender=("Garage Sale", "inquiry@octtone.com"),
                    recipients=["manshu4@gmail.com"])






    msg.html = "Hi " + sellerData[3] + "<br>" \
               "We would like to inform you that you have made a sale for <b> " + price + "</b>" \
               " The item you sold is " + sellerData[1]  + "</b>" \
                   " You sold it to " + buyerData[1] + " " + buyerData[2] + " Who can be contacted at " + buyerData[3]
    
    # msg.html = 'Hi ' +  '</br> We would like to inform you that you have made a sale for <b> ' + price "</b>"
    mail.send(msg)
    print("sending mail")
    return "TRUE"


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # # removed before deploying a production app.
    # sendMail()
    application.debug = True
    application.run()
    
