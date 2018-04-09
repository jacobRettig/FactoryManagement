""" 
This is where all of the routes of the application go. So far, login and register have been added only 
for the purposes of rendering the static pages for testing the desgin. 
"""

from odc_app import app
from odc_app.forms import LoginForm, RegistrationForm
from flask import render_template, url_for

@app.route('/login', methods=['GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		pass
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		pass
	return render_template('register.html', title='Registeration', form=form)