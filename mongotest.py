from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template
from flask import Blueprint
import API_KEYS

from sshtunnel import SSHTunnelForwarder
import pymongo
import pprint

mongotest = Blueprint('mongotest', __name__)
client = pymongo.MongoClient('mongodb+srv://mohics411:BD5vJ0bAHNmqs04r@cluster0-cnmmg.mongodb.net/test?retryWrites=true&w=majority')
db = client.cs411
collection = db.prices
@mongotest.route('/')
def testMongo():
    for doc in collection.find():
        pprint.pprint(doc)
    return "mongotest"