from flask import Flask, render_template, json,request,url_for,session,redirect
from flask_pymongo import PyMongo
# from keras import backend as K
from pymongo import MongoClient
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import bcrypt
from flask import *
from flask import session

app = Flask(__name__, template_folder='template')
# K.clear_session()

app.config['MONGO_DBNAME'] = 'user'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/user'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('login.html')


@app.route('/login1', methods=['POST','GET'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    print(request.form['username'])
    logged_user = request.form['username']
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return render_template("index.html")

    return render_template("index.html")

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            msg = '{ "html":"ok"}'
            msghtml = json.loads(msg)
            # return msg["html"]
            return msghtml["html"]
        else:
            msg = '{ "html":"user"}'
            msghtml = json.loads(msg)
            return msghtml["html"]

        # return 'That username already exists!'
    return render_template('signup.html')
    
@app.route('/after_login',methods=['POST','GET'])
def after_log():
    return render_template('after_login.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)