from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS


search = Blueprint('search', __name__)

@search.route('/')
def index(key='start'): 
    # initial page before first search is made
    return render_template("searchResults.html", res=[key]) 


@search.route('/getresults', methods=['GET','POST'])
def searchResults():
    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')

        '''

        able to make initial search using:
        item name (exact match for now. later: SQL SOUNDEX)
            SELECT *
            FROM Items
            WHERE id = %s


        add filters: by brand, by date, (by category, by transaction/person/region?)
        possible function for applying filters to query:
        
        query = ""
        for k, v in request.form:
            new_query = format( """ SELECT *
                                    FROM Items
                                    WHERE %s %s
                                """, k, v)
            query += new_query + 'INTERSECT\n' 

        '''

        search = request.form['search']

        try:
            query = """ SELECT *
                        FROM Items
                        WHERE itemName = %s %s
                    """

            cursor = cnx.cursor()
            cursor. execute(query, (search, ""))
            results = cursor.fetchall()
            print(results)
            if len(results) == 0:
                return render_template("searchResults.html", res=['none'])
            else:
                return render_template("searchResults.html", res=['results', results])

        except:
            print("SEARCH FAILED")
            return None

    # TODO: HOW TO REDIRECT WHEN REFRESHING PAGE?? (does another post instead of resetting search)
    if request.method == 'GET':
        return redirect('/search/')

