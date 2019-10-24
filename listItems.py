from flask import jsonify
import mysql.connector
from flask_mail import Mail, Message
from flask import make_response
from flask import Flask, request, url_for, render_template, redirect
from flask import Blueprint
import API_KEYS


listItems = Blueprint('listItems', __name__)


@listItems.route('/<userId>')
def index(userId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')




    

    try: 
        query = """ SELECT retailerId, itemName, brandName, description, Items.id, firstname, lastName, email, phoneNumber, zipCode, price
                    from Items  Left Join Users on Items.retailerId = Users.id
                    where ItemName !="" and isCurrentlyAvailable = true; 
                """
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        # return render_template('listAll.html')
        return render_template("listAll.html", res= result, userId=userId );
    except:
        print("ERROR")



    return render_template('listAll.html')





@listItems.route('purchase/<userId>/<itemId>')
def purchaseItem(userId, itemId):
    cnx = mysql.connector.connect(user='root', password='RootRoot1',
                                  host=API_KEYS.getSQLEndPoint(),
                                  database='innodb')


    # ADD ITEM TO PURCHASES TABLE 
    # TRIGGER IN 

    price = request.args.get('price')
    

    try: 
        query = """ INSERT INTO Purchases(itemId, userId, purchasePrice) values (%s, %s, %s); 
                """
        query2 = """Update Items 
                    Set	isCurrentlyAvailable = %s
                    Where id = %s;
                """
        cursor = cnx.cursor()
        cursor.execute(query, (itemId, userId, price))
        cnx.commit()
        cursor.execute(query2, (False, itemId))
        cnx.commit()
        # result = cursor.fetchall()
        # print(result)
        # return render_template('listAll.html')

        print(itemId)

        return redirect('/items/completePurchase/'+ userId)
    except Exception as e:
        print(e)



    return render_template('listAll.html')



@listItems.route('/completePurchase/<userId>')
def completeTransaction(userId):
    return render_template("FinishTransaction.html", userId = userId)