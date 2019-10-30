from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template("home.html", userId=1)

@home.route('/home/search/<userId>/')
def searchItem(userId, itemName):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')
    itemName = request.form('Search')
    return redirect()


# must redirect to Home, Buy Item, Sell Item, Profile
# must redirect after searching for an item
