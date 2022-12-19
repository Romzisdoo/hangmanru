from flask import Flask, request, g, render_template, flash, redirect, url_for, session
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from methods_app import MethodsMyApp
import word_select
from user_login import UserLogin


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

secret_word = None
word_set = None
to_display = None
tries = None
blanks = None


@login_manager.user_loader
def load_user(user_id):
    print("load_user") 
    return UserLogin().from_db(user_id, dbase)

def conect_db():
    conn=sqlite3.connect(myapp.config['DATABASE'])
    conn.row_factory=sqlite3.Row
    return conn

def create_db():
    db = conect_db()
    with myapp.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

dbase = None
@myapp.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = MethodsMyApp(db)

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db=conect_db()
    return g.link_db

@myapp.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@myapp.after_request
def set_response_headers(response):

    response.headers['Expires'] = '0'
    return response


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

@myapp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Jūs atsijungėte", "succes")
    return redirect(url_for('login'))

@myapp.route('/profile')
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Atsijungti</a>
    <p>Sveikinam prisijungus:{current_user.get_name()} {current_user.get_surname()}
    <p> Jūsų spėjamas žodis: {secret_word}
    <p> Jūsų atspėtos raidės žaidime: {to_display}
    <p> Liko atspėti: {blanks} raid'es(-žių)
    <p> Jūsų neteisingi spėjimai: {tries}
    <p> Jūsų nepanaudotos spėjimams raidės: {word_set}
    <p> """

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