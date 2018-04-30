""" 
This is where all of the routes of the application go. So far, login and register have been added only 
for the purposes of rendering the static pages for testing the desgin. 
"""


from odc_app import app
from odc_app.forms import LoginForm, getRegistrationForm, CreateProductForm, CreateCategoryForm
from flask import render_template, url_for, redirect, abort
from flask_login import UserMixin, login_user, login_required
import odc_app.sqlHandler as DB


#Login User model
class User(UserMixin):
    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role
    def __repr__(self):
        return '<User (email:{}, password:{}, role:{})>'.format(self.email, self.password, self.role)

    @staticmethod
    def createUser(email, password):
        if DB.isValidLogin(email, password):
            return User(email, password, DB.getRole(email))
        return None



@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.createUser(form['Username'], form['Password'])
        if user is None:
            return abort(401)
        login_user(user, remember=form['Remember Me'])
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(DB.getRegions())
    if form.validate_on_submit():
        if DB.createUser('Customer', form['Email'], form['Password'], form['First Name'], form['Last Name'], form['Phone'], form['Date of Birth'], form['Country'], form['Region'], form['1st Line Address'], form['2nd Line Address']):
            login_user(User.createUser(form['Email'], form['Password']))
            return redirect(url_for('index'))
    return render_template('register.html', title='Registeration', form=form)


@app.route('/products/new', methods=['GET', 'POST'])
@login_required
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
@login_required
def products():
    # Query the products of current user
    # Store returned tuples as list
    # Pass in list as argument to render_template so that the products can be displayed
    return render_template('products.html')


@app.route('/categories/new', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CreateCategoryForm()
    if form.validate_on_submit():
        # Save new category to database
        return redirect(url_for('products'))
    return render_template('new_category.html', title='Create Category', form=form)

