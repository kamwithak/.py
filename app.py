# Flask-based backend for an encrypted user-registration/database platform that manages project repositories
# Database technology: SHA256 for encryption and MySQL for storing
# Developed by Kamran Choudhry

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

# init
@app.route('/')
def init():
    return render_template('init.html')

# check if user is logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if "logged_in" in session:
			return f(*args, **kwargs)
		else:
			flash("~ PLEASE LOGIN TO ACCESS THE K! REPOSITORY ~", "danger")
			return redirect(url_for('login'))
	return wrap
	
# dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	# create cursor
	cur = mysql.connection.cursor()
	# get articles
	result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])
	articles = cur.fetchall()
	if result > 0: #if there is any rows
		return render_template('dashboard.html', articles=articles)
	else:
		msg_red = "~ EMPTY DASHBOARD ~"
		return render_template('dashboard.html', msg_red=msg_red)
	# close connection
	cur.close()
 
# about
@app.route('/about')
def about():
	return render_template('about.html')

# articles
@app.route('/repository')
@is_logged_in
def articles():
	# create cursor
	cur = mysql.connection.cursor()
	# get articles
	result = cur.execute("SELECT * FROM articles")
	articles = cur.fetchall()
	if result > 0: #if there is any rows
		return render_template('articles.html', articles=articles)
	else:
		msg_red = "~ EMPTY REPOSITORY ~"
		return render_template('articles.html', msg_red=msg_red)
	# close connection
	cur.close()

# inside each article
@app.route('/repository/<string:id>')
@is_logged_in
def article(id):
	# create cursor
	cur = mysql.connection.cursor()
	# get articles then article
	result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
	article = cur.fetchone()
	# close connection
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
		# create the cursor
		cur = mysql.connection.cursor()
		# execute query statement
		cur.execute('INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)', (name, email, username, password))
		# commit to database 
		mysql.connection.commit()
		# close connection
		cur.close()
		flash("~ SUCCESSFULLY REGISTERED ~", "success")
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

# user log in
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		# get form fields
		username = request.form['username']
		password_entered = request.form['password']
		# create a cursor 
		cur = mysql.connection.cursor()
		# get username in db
		result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
		if result > 0: #if there is any rows
			# get stored hash / dictionary configuration
			data = cur.fetchone()
			password_db = data['password']
			# compare hashed passwords
			if sha256_crypt.verify(password_entered, password_db):
				# passed
				session["logged_in"] = True
				session["username"] = username
				flash("~ GRANTED ACCESS ~", "success")
				return redirect(url_for('dashboard'))
			else:
				error = "~ PASSWORD INCORRECT ~"
				return render_template('login.html', error=error)
			# close connection 
			cur.close()
		else:
			error = "~ USERNAME INVALID ~"
			return render_template('login.html', error=error)
	return render_template('login.html')

# logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash("~ YOU'VE BEEN LOGGED OUT ~", "success")
	return redirect(url_for('login'))

# article form class
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=200)])
	body = TextAreaField('Body', [validators.Length(min=30)])

# add article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data
		# create cursor
		cur = mysql.connection.cursor()
		# execute 
		cur.execute("INSERT INTO articles(title, body, author) VALUES(%s,%s,%s)", (title, body, session['username']))
		# commit 
		mysql.connection.commit()
		# close / flash
		cur.close()
		flash("~ FILE UPLOADED ~", "success")
		return redirect(url_for('dashboard'))
	return render_template('add_article.html', form=form)

# edit article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
	# create cursor
	cur = mysql.connection.cursor()
	# get the article by respective 'id'
	result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
	article = cur.fetchone()
	cur.close()
	# get correct form
	form = ArticleForm(request.form)
	# populate article form fields
	form.title.data = article['title']
	form.body.data = article['body']
	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']
		# create cursor
		cur = mysql.connection.cursor()
		app.logger.info(title)
		# execute 
		cur.execute("UPDATE articles SET title = %s, body = %s WHERE id = %s", (title, body, id))
		# commit 
		mysql.connection.commit()
		# close / flash
		flash("~ FILE UPDATED ~", "success")
		cur.close()
		return redirect(url_for('dashboard'))
	return render_template('edit_article.html', form=form)

# delete article
@app.route("/delete_article/<string:id>", methods=['POST'])
@is_logged_in
def delete_article(id):
	# create cursor 
	cur = mysql.connection.cursor()
	# execute
	cur.execute("DELETE FROM articles WHERE id = %s", [id])
	result = cur.execute("SELECT * FROM articles WHERE author = %s", [session["username"]])
	# commit
	mysql.connection.commit()
	if result > 0: # aesthetics
		flash("~ FILE DELETED ~", "success")
	# close / flash
	cur.close()
	return redirect(url_for('dashboard'))

# program starts here
if __name__ == '__main__':
	app.secret_key='**************'
	app.run(debug=True)
