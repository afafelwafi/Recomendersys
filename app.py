from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.Users import User
from models.Users import db
import re
import json
import traceback
import sys
from sklearn.metrics.pairwise import cosine_similarity
import six
import pandas as pd
import numpy as np 
import content_filtering 
import similarity
import product_filter
import db as ddb
import utils
import importlib.util
spec = importlib.util.spec_from_file_location("recommende-departement", "C:/Users/afafe/Desktop/stage/DF's recommender/recommender-departement.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
import similarity

# setup the app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
bcrypt = Bcrypt(app)

# setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# create the db structure
with app.app_context():
    db.create_all()


####  setup routes  ####
@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():

    # clear the inital flash message
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')

    # get the form data
    username = request.form['username']
    password = request.form['password']

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # query the user
    registered_user = User.query.filter_by(username=username).first()

    # check the passwords
    if registered_user is None and bcrypt.check_password_hash(registered_user.password, password) == False:
        flash('Invalid Username/Password')
        return render_template('login.html')

    # login the user
    login_user(registered_user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')

    # get the data from our form
    password = request.form['password']
    conf_password = request.form['confirm-password']
    username = request.form['username']
    email = request.form['email']

    # make sure the password match
    if conf_password != password:
        flash("Passwords do not match")
        return render_template('register.html')

    # check if it meets the right complexity
    check_password = password_check(password)

    # generate error messages if it doesnt pass
    if True in check_password.values():
        for k,v in check_password.items():
            if str(v) is "True":
                flash(k)

        return render_template('register.html')

    # hash the password for storage
    pw_hash = bcrypt.generate_password_hash(password)

    # create a user, and check if its unique
    user = User(username, pw_hash,'','','','',0,email,'','','','','','')
    u_unique = user.unique()

    # add the user
    if u_unique == 0:
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for('login'))

    # else error check what the problem is
    elif u_unique == -1:
        flash("Email address already in use.")
        return render_template('register.html')

    elif u_unique == -2:
        flash("Username already in use.")
        return render_template('register.html')

    else:
        flash("Username and Email already in use.")
        return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/charts',methods=["GET","POST"])

def charts():
    select_top=request.form.get("top_size")
    select_bottom=request.form.get("bottom_size")
    select_shoes=request.form.get("shoes_size")  
    select_basics=request.form.get("Basics")
    select_casual=request.form.get("Casual")
    select_work=request.form.get("Work")  
    select_creative=request.form.get("Creative")    
    current_user.sizes=str(select_top)+' '+str(select_bottom)+' '+str(select_shoes)
    current_user.style=str(select_basics)+' '+str(select_work)+' '+str(select_casual)+' '+str(select_creative)
    select_budget=request.form.get("budget")
    current_user.budget=str(select_budget)
    select_gender=request.form.get("genre")
    current_user.gender=str(select_gender)
    select_cat=request.form.get("category")
    current_user.categories=str(select_cat)
    
    
    ##recommendation part let's try Departement feminin  for an exemple, except the popular products the user hasn't seen any product yet 
    

    db.session.commit()
    flash("INFOS ADDED")
    
    return render_template('charts.html', user=current_user) 


@app.route('/tables')
def tables():
    reco=current_user.popular_products(6)
    RECO=[l['picture_url'] for l in reco]
    #SEEN=current_user.products_seen.split()
    #reco=list(set(RECO)-set(SEEN))
    current_user.reco=' '.join(RECO)
    current_user.products_seen+=' '+' '.join(RECO)
    db.session.commit()
    flash("INFOS ADDED")
    
    return render_template('tables.html', user=current_user)


@app.route('/preferences')
def forms():
    return render_template('prefernces.html', user=current_user)


@app.route('/bootstrap-elements')
def bootstrap_elements():
    return render_template('bootstrap-elements.html', user=current_user)


@app.route('/bootstrap-grid')
def bootstrap_grid():
    return render_template('bootstrap-grid.html', user=current_user)


@app.route('/Nos_Recommandations')
def Nos_Recommandations():
    user_data={}
    user_data['sizes_top']=current_user.sizes.split()[0]
    user_data['sizes_bottom']=current_user.sizes.split()[1]
    user_data['sizes_shoes']=current_user.sizes.split()[2]
    user_data['gender']='female'
    user_data['category']=current_user.categories 
   
    #user's dat
    product_seen=ddb.get_ids_form_url(current_user.products_seen.split(),6)
    product_seen=' '.join([p['product_id'] for p in  product_seen])
    similarity_matrix=foo.recommend(1,6,user_data,user_data['category'],product_seen,current_user.products_liked,current_user.products_disliked)
    similar=ddb.get_picture_url(similarity_matrix,6)
    similarity_matrix_url=[p['picture_url'] for p in similar]
    current_user.reco=' '.join(similarity_matrix_url)
    current_user.products_seen+=' '+current_user.reco
    

    current_user.nm_reco=current_user.nm_reco+1
        
    db.session.commit()
    flash("INFOS ADDED")
    return render_template('Nos_Recommandations.html', user=current_user)


@app.route('/profile')
def profile():
    #add a part where the user can write more infos about himself 
    return render_template('profile.html', user=current_user)


@app.route('/settings')
def settings():
    return render_template('settings.html', user=current_user)

####  end routes  ####


# required function for loading the right user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# check password complexity
def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
        credit to: ePi272314
        https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions
    """

    # calculating the length
    length_error = len(password) <= 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    ret = {
        'Password is less than 8 characters' : length_error,
        'Password does not contain a number' : digit_error,
        'Password does not contain a uppercase character' : uppercase_error,
        'Password does not contain a lowercase character' : lowercase_error,
        'Password does not contain a special character' : symbol_error,
    }

    return ret


if __name__ == "__main__":
	# change to app.run(host="0.0.0.0"), if you want other machines to be able to reach the webserver.
	app.run() 