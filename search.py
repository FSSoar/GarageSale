from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS


search = Blueprint('search', __name__)

@search.route('/<userId>')
def index(userId, key='start'): 
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



def searchPlainText(queryStr):

        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')

        try:

            queryPopularity = """ 
                            CREATE OR REPLACE View Popularity as
                            Select itemId, count(itemId) as itemCount
                            From Purchases Left Join  Items On Purchases.itemId = Items.id
                            Where Items.retailerID = 1 and Items.itemName is Not NULL and Items.itemName != "" and Items.id is Not NULL
                            Group By itemId;
                            
                            """

            # cursor = cnx.cursor()
            # cursor.execute(queryPopularity)
            # cursor.commit()

            cursor = cnx.cursor()
            cursor.execute(queryPopularity)
            cnx.commit()

            query = """
            
            
                Select itemID, itemName, brandName, price, count(itemId)
                From  

                    (
                        (Select *
                        From Items Left Join Popularity On Popularity.itemId = Items.id
                        Where (SOUNDEX(Items.itemName) like SOUNDEX(%s) or Items.itemName Like %s) and Items.itemName != '' and Items.isCurrentlyAvailable = true
                        order By Popularity.itemCount)
                        Union
                        (Select *
                        From Items Left Join Popularity On Popularity.itemId = Items.id
                        Where (SOUNDEX(Items.brandName) like SOUNDEX(%s) or Items.brandName Like %s) and Items.itemName != '' and Items.isCurrentlyAvailable = true
                        order By Popularity.itemCount)
                        Union
                        (Select *
                        From Items Left Join Popularity On Popularity.itemId = Items.id
                        Where (SOUNDEX(Items.description) like SOUNDEX(%s) or Items.description Like %s) and Items.itemName != '' and Items.isCurrentlyAvailable = true
                        order By Popularity.itemCount)
                        Union
                        (
                        Select *
                        From	(
                            Select Items.id as id, retailerID, itemName, availabiltyStartDate, availabiltyEndDate, isCurrentlyAvailable, brandName, description, categoryId, price 
                            from Metadata Left Join Items on Metadata.itemId = Items.id
                            Where (SOUNDEX(Items.description) like SOUNDEX(%s) or Items.description Like %s) and Items.isCurrentlyAvailable = true
                            ) as metadata  Left Join Popularity On Popularity.itemId = metadata.id

                        ) 
                        
                    )  as allReturned 
                Group by itemId, itemName, brandName, price


            
            
            
            
            

                """

                # query.replace()
            print(query % (queryStr,queryStr + '%',queryStr,queryStr+ '%',queryStr,queryStr+ '%',queryStr,queryStr+ '%'))

            cursor = cnx.cursor()
            cursor. execute(query, (queryStr, queryStr+ '%',  queryStr, queryStr+ '%', queryStr, queryStr+ '%', queryStr, queryStr+ '%'))
            results = cursor.fetchall()
            print(results)
            if len(results) == 0:
                return results
            else:
                return results # render_template("searchResults.html", res=['results', results])
        except Exception as e:
            print("SEARCH FAILED ", e)
            return None



@search.route('/getresults/<userId>', methods=['GET','POST'])
def searchResults(userId):
    if request.method == 'GET':
        cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                    host=API_KEYS.getSQLEndPoint(),
                                    database='innodb')

        try:
            # query = buildQuery(request.form)
            # print(request.form)
            # print(query)

            # cursor = cnx.cursor()
            # cursor. execute(query)
            # results = cursor.fetchall()
            # 
            results = searchPlainText(request.args.get('search'))
            print(results)
            if len(results) == 0:
                print("ZERO RES")
                return render_template("searchResults.html", res=['none'], userId= userId)
            else:
                print("RESULTS ")
                return render_template("searchResults.html", res=['results', results], userId= userId)

        except Exception as e:
            print("SEARCH FAILED  ", e)
            return str(e)

    # TODO: HOW TO REDIRECT WHEN REFRESHING PAGE?? (does another post instead of resetting search)
    if request.method == 'POST':
        return redirect('/search/')

# searchPlainText("dyson")