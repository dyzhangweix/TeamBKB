from werkzeug import generate_password_hash, check_password_hash
from intro_to_flask import app
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()




class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  is_teacher = db.Column(db.String(120))
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
    self.is_teacher = 'N'
    exsiting = PreList.query.filter_by(t_email = email).first()
    if exsiting is not None:
      self.is_teacher = 'Y'
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)


class Course(db.Model):
  __tablename__ = 'courses'
  cid = db.Column(db.Integer, primary_key = True)
  classroom = db.Column(db.String(45))
  code = db.Column(db.String(45))
  ins_id = db.Column(db.Integer)
  cname = db.Column(db.String(100))
  duration = db.Column(db.Integer)
  time = db.Column(db.String(100))


class Student(db.Model):
  __tablename__ = 'students'
  sid = db.Column(db.Integer, primary_key = True)
  sfirstname = db.Column(db.String(45))
  slastname = db.Column(db.String(45))

class Attendance(db.Model):
  __tablename__ = 'attendance'
  aid = db.Column(db.Integer, primary_key = True)
  checkin_time = db.Column(db.DateTime)
  checkout_time = db.Column(db.DateTime)
  date = db.Column(db.String(100))
  status = db.Column(db.String(45))
  stu_name = db.Column(db.String(100))
  stu_id = db.Column(db.Integer)
  course_code = db.Column(db.String(45))
  course_id = db.Column(db.String(45))
  additional = db.Column(db.String(500))

  def __init__(self, checkin_time, checkout_time, date, status, stu_name, stu_id, course_code, course_id, additional, aid = None):
    self.checkin_time = checkin_time
    self.checkout_time = checkout_time
    self.date = date
    self.status = status
    self.stu_id = stu_id
    self.stu_name = stu_name
    self.course_id = course_id
    self.course_code = course_code
    self.additional = additional
    self.aid = aid

class StudentCourseLink(db.Model):
  __tablename__ = 'courselink'
  cid = db.Column(db.Integer, primary_key = True)
  sid = db.Column(db.Integer, primary_key = True)

class PreList(db.Model):
  __tablename__ = 'pre_list'
  idpre_list = db.Column(db.Integer, primary_key = True)
  t_email = db.Column(db.String(100))

