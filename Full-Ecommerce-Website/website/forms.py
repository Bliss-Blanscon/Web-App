
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, FloatField, DateField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class signUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

class logInForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=6)])
    change_password = SubmitField('Change Password')


class AddProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    product_picture = FileField('Product Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only!')])
    flash_sale =    BooleanField('Flash Sale')

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update Product')

class AddEmployeeForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    employee_name = StringField('Employee Name', validators=[DataRequired(), Length(min=2)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    date_added = DateField('Date Added', validators=[DataRequired()])  # Renamed to match query
    add = SubmitField('Add Employee')
    delete = SubmitField('Delete Employee')


    add = SubmitField('Add Employee')
    delete = SubmitField('Delete Employee')