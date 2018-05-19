# User Registration // Login System
# Kamran Choudhry
# -> written for py 3

import os, sqlite3
from flask import Flask, render_template, redirect, request, url_for, flash

app = Flask(__name__)

# registration system
@app.route('/registration', methods=['GET', 'POST'])
def registration():
	if request.method == 'POST':
		# get form parameters
		firstname = request.form.get('firstname')
		lastname = request.form.get('lastname')
		email = request.form.get('email')
		username = request.form.get('username')
		pw = request.form.get('password')
		pw_confirm = request.form.get('password_confirm')
		# create access to the db // check if username is already in db
		db = sqlite3.connect('encrypted_registration.db')
		cur = db.cursor()
		cur.execute("SELECT * FROM encrypted_registration WHERE username = ?", (username,))

		if not cur.fetchall():
			if pw == pw_confirm:
				if len(username) > 6:
					if '@' in email:
						# insert registration parameters into db
						cur.execute("INSERT INTO encrypted_registration VALUES (?,?,?,?,?)", (firstname, lastname, email, username, pw))
						# query everything and print db contents
						cur.execute("SELECT * FROM encrypted_registration")
						print(cur.fetchall())
						db.commit()
						db.close()

						return render_template('extra/success.html')
					else:
						print("invalid email")
						return render_template('extra/reg_confirm_email.html')
				else:
					print("len(username) < 6")
					return render_template('extra/reg_confirm_username.html')
			else:
				print("passwords are incompatible")
				return render_template('extra/reg_confirm_pw.html')
		else:
			print("username is already in db")
			return render_template('extra/username_original.html')

	return render_template('registration.html')
	
# WRITE WITH PROPER STRUCTURE LIKE ABOVE FUNCTION
# login system
@app.route('/login', methods=['GET', 'POST'])
def login():
	# get form values
	username = request.form.get('username')
	pw = request.form.get('password')
	# connect to the db
	db = sqlite3.connect('encrypted_registration.db')
	cur = db.cursor()
	# query the db for so 
	cur.execute("SELECT * FROM encrypted_registration WHERE username = ? AND password = ?", (username, pw))

	# granted access
	if cur.fetchall():
		print("Welcome " + username)
		# createApplication()
	# denied access
	else:
		print("Incorrect username or password")

	return render_template('login.html')

# automated init to login page
@app.route('/') 
def init():
    return redirect(url_for('login'))

if __name__ == '__main__':
	app.secret_key='secret_key'
	app.run(debug=True)