from flask import Flask, request, g, render_template, flash, redirect, url_for, session
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from methodsApp import methodsMyApp
import word_select
from user_login import UserLogin


# Config.

DATABASE ='hangman_game.db'
DEBUG = True
SECRET_KEY = 'ad458sla69kdu574sc'

myapp = Flask(__name__)
myapp.config.from_object(__name__)

myapp.config.update(dict(DATABASE=os.path.join(myapp.root_path, 'hangman_game.db')))

login_manager = LoginManager(myapp)
login_manager.login_view = 'login'

imageFolder = os.path.join("static", "images")
myapp.config['UPLOAD_FOLDER'] = imageFolder

#Hangman Game config
secret_word = None
word_set = None
to_display = None
tries = None
blanks = None

# Uzkrauname klase, kaskart kai vykdoma vartotojo uzklausa (Flask login modulis nustato, koks useris sesijoje)
@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

# Jungiamasi su DB 
def conect_db():
    conn=sqlite3.connect(myapp.config['DATABASE'])
    conn.row_factory=sqlite3.Row
    return conn

def create_db():
    # Pagalbine priemone sukuriand db lenteles
    db = conect_db()
    with myapp.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

dbase = None
@myapp.before_request
def before_request():
    # Ryšio su DB nustatymas ir sujungimas prieš užklausos vykdymą (KREIPIAMASI I GLOBALU KINTAMAJI 'dbase')
    global dbase
    db = get_db()
    dbase = methodsMyApp(db)

def get_db():
    # Sujungti su DB jei tai dar nenustatyta, jei nera susijungta su db
    if not hasattr(g, 'link_db'):
        g.link_db=conect_db()
    return g.link_db

@myapp.teardown_appcontext
def close_db(error):
    # Klaidos atveju nutraukiame susijungima su DB
    if hasattr(g, 'link_db'):
        g.link_db.close()

#to game
@myapp.after_request
def set_response_headers(response):

    response.headers['Expires'] = '0'
    return response

# HTML PUSLAPIŲ DEKORATORIAI:
@myapp.route("/")
def welcome():   
    return render_template("index.html")

@myapp.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        if len (request.form['name']) >4 and len(request.form['surname'])>4 \
            and len(request.form['email'])>4 and len(request.form['pasword']) > 4 \
            and request.form['pasword']==request.form['pasword2']:
            hash = generate_password_hash(request.form['pasword'])
            res = dbase.add_user(request.form['name'], request.form['surname'], request.form['email'], hash)
            if res:
                flash ("Jūs sėkmingai užsiregistravote žaidimui", category="success")
                return redirect(url_for('login'))
            else:
                flash("Įvyko klaida atnaujinant duomenų bazę", category="error")
        else:
            flash("Neteisingai užpildyti laukai", category="error")

    return render_template("register.html")

@myapp.route("/login", methods= ["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['pasword'], request.form['pasword']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('hangman'))

        flash("Nesutampa slaptažodžiai", "error")

    return render_template("login.html")

@myapp.route("/hangman")
@login_required
def hangman():
	global secret_word
	global word_set
	global to_display
	global tries
	global blanks	
	secret_word = word_select.get_random_word()
	word_set = "aąbcčdeęėfghiįjklmnopqrsštuųūvzž"
	blanks = 0
	to_display = []
	for item,char in enumerate(secret_word):
		if char==" ":
			to_display.append(" ")
			
		else:
			to_display.append("_")
			blanks+=1

	tries = 0
	return render_template('hangman.html',to_display=to_display,word_set=word_set,tries="/static/images/images%d.png"%tries)


@myapp.route('/add_char',methods=["POST"])
def add_char():
	global secret_word
	global word_set
	global to_display
	global tries
	global blanks	

	letter = request.form["letter"]
	
	chance_lost = True
	for i,char in enumerate(secret_word):
		if char==letter:
			chance_lost = False
			to_display[i] = letter
			blanks-=1

	word_set = word_set.replace(letter,'')
	print("blanks",blanks)
	if chance_lost==True:
		tries += 1
		if tries==10:
			return redirect('/hang')

	if blanks==0:
		return redirect('/shot')

	return render_template('hangman.html',to_display=to_display,word_set=word_set,tries="/static/images/images%d.png"%tries)


@myapp.route('/hang')
def game_lost_landing():
	return render_template('finitohang.html')

@myapp.route('/shot')
def game_won_landing():
	return render_template('finitoshot.html')


if __name__ == "__main__":
    myapp.run()