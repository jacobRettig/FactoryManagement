#The following forms file contains classes for all of the forms used in the application
#Primary Author: Salem Abuammer

#imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DecimalField, SelectField, validators
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from wtforms.fields.html5 import DateField
import phonenumbers

class RegistrationForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])
	dob = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
	phone = StringField('Phone', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_phone(self, phone):
		if len(phone.data) > 16:
			raise ValidationError('Invalid phone number.')
		try:
			input_number = phonenumbers.parse(phone.data)
			if not (phonenumbers.is_valid_number(input_number)):
				raise ValidationError('Invalid phone number.')
		except:
			input_number = phonenumbers.parse("+1{}".format(phone.data))
			if not (phonenumbers.is_valid_number(input_number)):
				raise ValidationError('Invalid phone number.')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class CreateProductForm(FlaskForm):
	product_name = StringField("Product Name", validators=[DataRequired()])
	""" The below are just a few exmaple default categories, there will also be a separate form that allows for the user to create a category
		The first thing in the tuple is the value of the category
		The second thing in the tuple is the actual label in the HTML page.
	"""
	product_category = SelectField("Product Category", choices=[('beauty', 'Beauty'), ('electronics', 'Electronics'), ('clothing', 'Clothing'), ('toys', 'Toys'), ('office', 'Office Products')])
	product_desc = TextAreaField("Product Description", validators=[DataRequired()])
	product_price = DecimalField("Product Price", validators=[DataRequired()])
	product_image = StringField("Product Image Link", validators=[DataRequired()])
	submit = SubmitField('Create Product')

class CreateCategoryForm(FlaskForm):
	category_name = StringField("Category Name", validators=[DataRequired()])
	category_description = TextAreaField("Category Description", validators=[DataRequired()])
	submit = SubmitField('Create Category')


