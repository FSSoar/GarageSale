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
    # TODO: get/send table info to generate filter options
    return render_template("searchResults.html", res=[key]) 


def buildQuery(form):

    query = 'SELECT * FROM Items'
    
    # if 'isCurrentlyAvailable' in request.form:
    #     query += ' SET isCurrentlyAvailable = 1'

    # TODO: enable query matches by one word (i.e. search=mower -> lawn mower)
    # query += format('WHERE itemName SOUNDS LIKE %s', form['search'])
    query += ' WHERE itemName SOUNDS LIKE \'{}\''.format(form['search'])
    
    for filter in form:
        if form[filter] != '':
            # note: relies on specific formatting for price range options
            if filter == 'search':
                continue
            elif filter == 'isCurrentlyAvailable':
                query += ' AND {} = 1'.format(filter)
            # elif filter == 'price':
            #     price_range = split(form[filter])
            #     if price_range[0] == '<' or price_range[0] == '>':
            #         query += ' AND {} {} {}'.format(filter, price_range[0], price_range[1])
            #     else:
            #         query += ' AND {} >= {}'.format(filter, price_range[0])
            #         query += ' AND {} <= {}'.format(filter, price_range[2])
            else: # assume follows WHERE filter = form[filter]
                query += ' OR {} = \'{}\''.format(filter, form[filter])

    return query


@search.route('/getresults', methods=['GET','POST'])
def searchResults():
    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')

        try:
            query = buildQuery(request.form)
            print(query)

            cursor = cnx.cursor()
            cursor. execute(query)
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

