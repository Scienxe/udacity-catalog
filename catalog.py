from flask import Flask, render_template, make_response, request, redirect, url_for, flash, jsonify
from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Instrument

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import httplib2
import json
import requests
import random, string


app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Udacious Musical Instruments"

engine = create_engine('sqlite:///musicalinstruments.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='', redirect_uri='postmessage')
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there's an error in access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        #return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    if getUserID(login_session['email']) is None:
        createUser(login_session)

    login_session['user_id'] = getUserID(data['email'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')

    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Success: revoked user's oauth token

        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showCatalog'))
    else:
        # Failed to log out
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).order_by(Category.name.asc()).all()
    return render_template('catalog.html', categories=categories, 
                            current_user=getCurrentUser())


@app.route('/catalog/<int:category_id>/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    instruments = session.query(Instrument).filter_by(category_id=category_id)
    return render_template('instruments.html', category=category, instruments=instruments, 
                            manager=getUserInfo(category.user_id), 
                            current_user=getCurrentUser())


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newInstrument():
    pass

@app.route('/catalog/<int:category_id>/new/', methods=['GET', 'POST'])
def newInstrumentWithCategory(category_id):
    if 'user_id' not in login_session:
        return redirect('/login')
    
    if request.method == 'POST':
        print request.form
        newInstrument = Instrument(name=request.form['name'], description=request.form['description'],
                                    picture=request.form['picture'], price=request.form['price'], 
                                    low_note=request.form['low_note'], high_note=request.form['high_note'], 
                                    category_id=request.form['category_id'],
                                    current_user=getCurrentUser())

        session.add(newInstrument)
        session.commit()
        flash(request.form['name'] + " has been edited.")
        return redirect(url_for('showCategory', category_id=request.form['category_id']))
    else:
        categories = session.query(Category).order_by(Category.name.asc()).all()
        return render_template('editInstrument.html', categories=categories, category_id=category_id, 
                                instrument_id=None, item=None, 
                                current_user=getCurrentUser())


@app.route('/catalog/<int:category_id>/edit/<int:instrument_id>/', methods=['GET', 'POST'])
def editInstrument(category_id, instrument_id):
    editedItem = session.query(Instrument).filter_by(id=instrument_id).one()
    if 'user_id' not in login_session or editedItem.user_id != login_session['user_id']:
        return redirect('/login')
    print editedItem.user_id, login_session['user_id']

    if request.method == 'POST':
        for key in request.form.keys():
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
            editedItem.price = request.form['price']
            editedItem.picture = request.form['picture']
            editedItem.low_note = request.form['low_note']
            editedItem.high_note = request.form['high_note']
            editedItem.category_id = request.form['category_id']

        session.add(editedItem)
        session.commit()
        flash(editedItem.name + " has been edited.")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        categories = session.query(Category).order_by(Category.name.asc()).all()
        return render_template('editInstrument.html', categories=categories, category_id=category_id, 
                                instrument=editedItem, item=editedItem, 
                                current_user=getCurrentUser())


@app.route('/catalog/<int:category_id>/delete/<int:instrument_id>/', methods=['GET', 'POST'])
def deleteInstrument(category_id, instrument_id):
    deletedItem = session.query(MenuItem).filter_by(id=instrument_id).one()
    if 'user_id' not in login_session or deletedItem.user_id != login_session['user_id']:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash(deletedItem.name + " has been deleted.")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteInstrument.html', category_id=category_id, 
                                instrument_id=instrument_id, item=deletedItem, 
                                current_user=getCurrentUser())




@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


@app.route('/showUsers/')
def showUsers():
    users = session.query(User).all()
    output = [x.name for x in users]
    return str(output)


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], 
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    print 'User ' + str(user.id) + ' added.'
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getCurrentUser():
    if 'user_id' in login_session:
        return getUserInfo(login_session['user_id'])
    else:
        return User(name="Guest", id=0)

if __name__ == '__main__':
    app.secret_key = "make_more_secreter"
    app.debug = True
    app.run(host='0.0.0.0', port=8000)





