from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template
from flask import Blueprint

signup  = Blueprint('signup', __name__)


@signup.route('/')
def index(): 
    return 'hi'



@signup.route('/create/user')
def createUser(): 
    return -1