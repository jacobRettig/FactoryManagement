#The following forms file contains classes for all of the forms used in the application
#Primary Author: Salem Abuammer

#imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DecimalField, SelectField, validators, SelectField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from wtforms.fields.html5 import DateField
import phonenumbers

def getRegistrationForm(regions, countries):
    class RegistrationForm(FlaskForm):
        first_name = StringField('First Name', validators=[DataRequired()])
        last_name = StringField('Last Name', validators=[DataRequired()])
        dob = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
        phone = StringField('Phone', validators=[DataRequired()])
        """ 
        Leaving the line below commented for now because it breaks the registration page otherwise,
        since the database isn't fully functional yet. Uncomment when regions has the appropriate data
        queried from the database.

        """
       	region = SelectField('Region', choices=list(map(lambda x:(x, x), regions)), validators=[DataRequired()])
        country = SelectField('Country', choices=list(map(lambda x:(x, x), countries)), validators=[DataRequired()])
        
        addressFirstLine = StringField('1st Line Address', validators=[DataRequired()])
        addressSecondLine = StringField('2nd Line Address')
        email = StringField('Email', validators=[DataRequired(), Email()])
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
    return RegistrationForm()

class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

def getCreateProductForm(categories):
    class CreateProductForm(FlaskForm):
        product_name = StringField("Product Name", validators=[DataRequired()])
        """ The below are just a few exmaple default categories, there will also be a separate form that allows for the user to create a category
            The first thing in the tuple is the value of the category
            The second thing in the tuple is the actual label in the HTML page.
        """
        product_category = SelectMultipleField("Product Category", choices=list(map(lambda x:(x, x), categories)))
        product_desc = TextAreaField("Product Description")
        product_price = DecimalField("Product Price", validators=[DataRequired()])
        product_image = StringField("Product Image Link", validators=[DataRequired()])
        product_quantity = IntegerField('Product Quantity', validators=[DataRequired()])
        submit = SubmitField('Create Product')
    return CreateProductForm()

def getCreateCategoryForm(isAdmin):
    if isAdmin:
        class CreateCategoryForm(FlaskForm):
            name = StringField("Category Name", validators=[DataRequired()])
            description = TextAreaField("Category Description", validators=[DataRequired()])
            is_default = BooleanField('Default Category')
            submit = SubmitField('Create Category')
        return CreateCategoryForm()
    else:
        class CreateCategoryForm(FlaskForm):
            name = StringField("Category Name", validators=[DataRequired()])
            description = TextAreaField("Category Description", validators=[DataRequired()])
            submit = SubmitField('Create Category')
        return CreateCategoryForm()

def getDeleteProductForm(products):
    class DeleteProductForm(FlaskForm):
        names = SelectMultipleField("Product Name", choices=list(map(lambda x:(x, x), products)))
        submit = SubmitField('Delete Products')
    return DeleteProductForm()
