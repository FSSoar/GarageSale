from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for

application = Flask(__name__)


@application.route('/')
def hello_world():

    return "/"



if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
