from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template

from signup import signup
from login import login


application = Flask(__name__)
application.register_blueprint(signup, url_prefix="/signUp" )
application.register_blueprint(login, url_prefix="/login" )








@application.route('/')
def hello_world():

    return render_template("index.html");





if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
