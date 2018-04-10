#The following forms file contains classes for all of the forms used in the application
#Primary Author: Salem Abuammer

#imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, validators
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
		if not phone.data.isdigit() or len(phone.data) > 16:
			raise ValidationError('Invalid phone number.')
		try:
			input_number = phonenumbers.parse(phone.data)
			if not (phonenumbers.is_valid_number(input_number)):
				raise ValidationError('Invalid phone number.')
		except:
			raise ValidationError('Invalid phone number.')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')
