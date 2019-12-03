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

application = Flask(__name__)
application.register_blueprint(signup, url_prefix="/signUp" )
application.register_blueprint(login, url_prefix="/login" )
application.register_blueprint(createitem, url_prefix="/createItem" )
application.register_blueprint(profile, url_prefix="/profile" )
application.register_blueprint(editProfile, url_prefix="/editProfile" )
application.register_blueprint(listItems, url_prefix="/items" )
application.register_blueprint(search, url_prefix="/search" )
application.register_blueprint(mongotest, url_prefix='/mongotest')





@application.route('/')
def hello_world():

    return redirect("/login");





if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
