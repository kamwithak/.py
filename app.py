# Flask-based backend for an encrypted user-registration/database web platform that manages project repositories
# Full stack application available upon request
# Database Technologies: SHA256 for data encryption and MySQL for server-side storing
# Developer: Kamran Choudhry

from flask import Flask, session, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import os

app = Flask(__name__)

# configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'insert_password'
app.config['MYSQL_DB'] = 'MYFLASKAPP'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# initialize MySQL
mysql = MySQL(app)

# init page
@app.route('/')
def init():
    return render_template('init.html')

# check if the user is currently logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if "logged_in" in session:
			return f(*args, **kwargs)
		else:
			flash("~ PLEASE LOGIN TO ACCESS THE K! REPOSITORY ~", "danger")
			return redirect(url_for('login'))
	return wrap
	
# dashboard page
@app.route('/dashboard')
@is_logged_in
def dashboard():
	cur = mysql.connection.cursor()		
	result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])
	articles = cur.fetchall()
	if result > 0: 							
		return render_template('dashboard.html', articles=articles)	
	else:
		msg_red = "~ EMPTY DASHBOARD ~"								
		return render_template('dashboard.html', msg_red=msg_red)				
	cur.close()														
 
# about
@app.route('/about')
def about():
	return render_template('about.html')						

# articles
@app.route('/repository')								
@is_logged_in
def articles():
	cur = mysql.connection.cursor()						
	result = cur.execute("SELECT * FROM articles")					
	articles = cur.fetchall()
	if result > 0: 							
		return render_template('articles.html', articles=articles)
	else:
		msg_red = "~ EMPTY REPOSITORY ~"								
		return render_template('articles.html', msg_red=msg_red)						# WLOG
	cur.close()																			

# inside each article
@app.route('/repository/<string:id>')
@is_logged_in
def article(id):
	cur = mysql.connection.cursor()														
	result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
	article = cur.fetchone()
	cur.close()																			
	return render_template("article.html", article=article)								

# register form class
class RegisterForm(Form):											
	name = StringField('Name', [validators.Length(min=1, max=50)])						
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', 
		message='Passwords do not match!')
	])
	confirm = PasswordField('Confirm Password')

# user register
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if form.validate() and request.method == 'POST':
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		cur = mysql.connection.cursor()
		cur.execute('INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)', (name, email, username, password))
		mysql.connection.commit()
		cur.close()
		flash("~ SUCCESSFULLY REGISTERED ~", "success")
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

# user log in
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']												
		password_entered = request.form['password']
		cur = mysql.connection.cursor()													 
		result = cur.execute("SELECT * FROM users WHERE username = %s", [username])		
		if result > 0: 																	
			data = cur.fetchone()									
			password_db = data['password']
			if sha256_crypt.verify(password_entered, password_db):					
				session["logged_in"] = True												
				session["username"] = username
				flash("~ GRANTED ACCESS ~", "success")
				return redirect(url_for('dashboard'))
			else:																		
				error = "~ PASSWORD INCORRECT ~"
				return render_template('login.html', error=error)
			cur.close()																	
		else:
			error = "~ USERNAME INVALID ~"
			return render_template('login.html', error=error)
	return render_template('login.html')

# logout page aka a redirect to the login page
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash("~ YOU'VE BEEN LOGGED OUT ~", "success")
	return redirect(url_for('login'))

# article class
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=200)])
	body = TextAreaField('Body', [validators.Length(min=30)])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# insertion(), edit(), delete() ~ std database operations below:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# add article ~ insertion()
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO articles(title, body, author) VALUES(%s,%s,%s)", (title, body, session['username']))
		mysql.connection.commit()
		cur.close()
		flash("~ FILE UPLOADED ~", "success")
		return redirect(url_for('dashboard'))
	return render_template('add_article.html', form=form)

# edit article ~ edit()
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
	article = cur.fetchone()
	cur.close()
	form = ArticleForm(request.form)
	form.title.data = article['title']
	form.body.data = article['body']
	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']
		cur = mysql.connection.cursor()
		app.logger.info(title)
		cur.execute("UPDATE articles SET title = %s, body = %s WHERE id = %s", (title, body, id))
		mysql.connection.commit()
		flash("~ FILE UPDATED ~", "success")
		cur.close()
		return redirect(url_for('dashboard'))
	return render_template('edit_article.html', form=form)

# delete article ~ delete()
@app.route("/delete_article/<string:id>", methods=['POST'])
@is_logged_in
def delete_article(id): 
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM articles WHERE id = %s", [id])
	result = cur.execute("SELECT * FROM articles WHERE author = %s", [session["username"]])
	mysql.connection.commit()
	if result > 0: 																					# aesthetics
		flash("~ FILE DELETED ~", "success")
	cur.close()
	return redirect(url_for('dashboard'))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	  MAIN
if __name__ == '__main__':
	app.secret_key='**************'
	app.run(debug=True)
