""" 
This is where all of the routes of the application go. So far, login and register have been added only 
for the purposes of rendering the static pages for testing the desgin. 
"""

from odc_app import app
from odc_app.forms import LoginForm, RegistrationForm, CreateProductForm, CreateCategoryForm
from flask import render_template, url_for, redirect

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		pass
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		pass
	return render_template('register.html', title='Registeration', form=form)

@app.route('/products/new', methods=['GET', 'POST'])
def create_product():
	form = CreateProductForm()
	""" form.product_category.choices must be equal to a list of tuples as seen in the choices attribute in the SelectField in forms.py.
		This is so we can dynamically load any created categories by the current userfrom the database into 
		the select field on the html page via a query.
	"""
	if form.validate_on_submit():
		# Save new product to database
		return redirect(url_for('products'))
	return render_template('new_product.html', title='Create Product', form=form)

@app.route('/products', methods=['GET'])
def products():
	# Query the products of current user
	# Store returned tuples as list
	# Pass in list as argument to render_template so that the products can be displayed
	return render_template('products.html')

@app.route('/categories/new', methods=['GET', 'POST'])
def create_category():
	form = CreateCategoryForm()
	if form.validate_on_submit():
		# Save new category to database
		return redirect(url_for('products'))
	return render_template('new_category.html', title='Create Category', form=form)

