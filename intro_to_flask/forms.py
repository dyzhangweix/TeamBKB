from flask.ext.wtf import Form
from flask import session
from wtforms import SelectField, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, DateField
from models import db, User, Course
import datetime
from pytz import timezone




class CheckinForm(Form):
  default_choices = []
  default_time = datetime.datetime.now(timezone('US/Pacific'))
  default_time = default_time.date()
  coursetext = TextField("Course")
  time = TextField("Time (yyyy-mm-dd)", default=default_time)
  studentid = TextField("Stuent ID")
  checkin = SubmitField("Check In")


class CheckoutForm(Form):
  default_choices = []
  default_time = datetime.datetime.now(timezone('US/Pacific'))
  default_time = default_time.date()
  course = SelectField("Course", choices=default_choices)
  time = TextField("Time (yyyy-mm-dd)", default=default_time)
  checkout = SubmitField("Check Out")

class ManagementForm(Form):
  default_choices = []
  default_time = datetime.datetime.now(timezone('US/Pacific'))
  default_time = default_time.date()
  name = TextField("Instructor Name")
  course = SelectField("Course", choices=default_choices)
  time = TextField("Time (yyyy-mm-dd)", default=default_time)

class SummaryForm(Form):
  default_choices = []
  default_time = datetime.datetime.now(timezone('US/Pacific'))
  default_time = default_time.date()
  course = SelectField("Course", choices=default_choices)
  time = TextField("Time (yyyy-mm-dd)", default=default_time)
  update = SubmitField("Show")
  
class ChangeStatusForm(Form):
  default_choices = []
  default_time = datetime.datetime.now(timezone('US/Pacific'))
  default_time = default_time.date()
  course = SelectField("Course", choices=default_choices)
  student = SelectField("Student", choices=default_choices)
  att = SelectField("Attendance", choices=[('Yes', 'Yes'), ('No', 'No')])
  time = TextField("Time (yyyy-mm-dd)", default=default_time)
  change = SubmitField("Submit")

class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True


class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
  def is_teacher(self):
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.is_teacher == 'Y':
      return True
    else:
      return False