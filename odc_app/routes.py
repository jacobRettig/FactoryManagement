""" 
This is where all of the routes of the application go. So far, login and register have been added only 
for the purposes of rendering the static pages for testing the desgin. 
"""


from odc_app import app
from odc_app.forms import LoginForm, getRegistrationForm, getCreateProductForm, getCreateCategoryForm
from flask import render_template, url_for, redirect, abort
from flask_login import UserMixin, login_user, login_required, login_manager, current_user
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
    form = getRegistrationForm(DB.getRegions(), DB.getCountries())
    if form.validate_on_submit():
        if DB.createUser('Customer', form.email.data, form.password.data, form.first_name.data, form.last_name.data, form.phone.data, form.dob.data, form.country.data, form.region.data, form.addressFirstLine.data, form.addressSecondLine.data):
            login_user(User.createUser(form['Email'], form['Password']))
            return redirect(url_for('index'))
        flash('Failed to register...')
    else:
        return render_template('register.html', title='Registeration', form=form)


@app.route('/products/new', methods=['GET', 'POST'])
@login_required
def create_product():
    user = current_user()
    form = getCreateProductForm(DB.getCategories(user.email))
    
    if form.validate_on_submit():
        if createProduct(form.product_name.data, form.product_price.data, form.product_image.data, form.product_quantity.data, user.email, form.product_desc.data):
            return redirect(url_for('products'))
        flash('Failed to create product...')
    else:
        return render_template('new_product.html', title='Create Product', form=form)


@app.route('/products', methods=['GET'])
@login_required
def products():
    # Query the products of current user
    # Store returned tuples as list
    # Pass in list as argument to render_template so that the products can be displayed
    user = current_user()
    products = DB.getProducts(user.email)

    strTemplate = '''<div>
    <h3>{name}</h3>
    <img src="{src}" />
    <p><b>Price:</b> {price}</p>
    <p><b>Quantity:</b> {quantity}</p>
    <p><b>Description:</b> {desc}</p>
    </div>\n'''
    strResult = '<p>No products</p>' if len(products) == 0 else ''
    for product in products:
        desc = '[Missing Description]' if product.description is None else product.description
        strResult += strTemplate.format(name=product.productName, src=product.imageData, price=product.price, quantity=product.quantity, desc=desc)
    
    return render_template('products.html', content=strResult)


@app.route('/categories/new', methods=['GET', 'POST'])
@login_required
def create_category():
    user = current_user()
    isDefault = DB.getAccessLevel(DB.getRole(user.email), 'Default Category') == 'both'
    form = getCreateCategoryForm(isDefault)
    if form.validate_on_submit():
        if isDefault:
            isDefault = form.is_default.data
        if DB.createCategory(form.name.data, isDefault, form.description.data, user.email):
            return redirect(url_for('products'))
        else:
            flash('Failed to create category...')
    else:
        return render_template('new_category.html', title='Create Category', form=form)

@app.errorhandler(401)
def unauthorized_access(e):
    return render_template('401.html', title='Unauthorized Access'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Page Not Found'), 404
