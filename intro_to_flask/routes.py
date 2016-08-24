from intro_to_flask import app
from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for, redirect
from forms import SignupForm, SigninForm, CheckinForm, CheckoutForm, ManagementForm, SummaryForm, ChangeStatusForm
from flask.ext.mail import Message, Mail
from models import db, User, Student, StudentCourseLink, Course, Attendance
from tables import EnrollTable, AttendanceTable
import json
import datetime
from pytz import timezone


mail = Mail()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/qrcode', methods=['GET', 'POST'])
def qrcode():
  return render_template('qr.html')
  
  
@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))

  form = CheckinForm()
  if request.method == 'POST':
    course_code = form.coursetext.data
    course = Course.query.filter_by(code = course_code).first()
    course_name = course.cname
    cid = course.cid
    studentLinks = StudentCourseLink.query.filter_by(cid=cid).all()
    for link in studentLinks:
      stu = Student.query.filter_by(sid=link.sid).first()
      stu_id = stu.sid
      stu_name = stu.sfirstname + ' ' + stu.slastname
      checkin_time = ''
      checkout_time = ''
      additional = ''
      status = 'No'
      date = datetime.datetime.now(timezone('US/Pacific'))
      date = date.date()
      exsiting = Attendance.query.filter_by(stu_id = stu_id, course_id = cid, date = date).first()
      if exsiting is not None:
        db.session.delete(exsiting)
        db.session.commit()
      newatt = Attendance(checkin_time, checkout_time, date, status, stu_name, stu_id, course_code, cid, additional)



      db.session.add(newatt)
      db.session.commit()
    #context = buildqrjson(True, form.time.data, course_code, course_name)
    context = buildcheckinurl(form.time.data, form.coursetext.data, form.studentid.data)
    return render_template('qr.html', qrStr=context)
  return render_template('checkin.html', form=form)
  
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))

  form = CheckoutForm()

  courses = Course.query.filter_by(ins_id = user.uid).all()
  courseChoices = []
  for course in courses:
    courseChoices.append((course.code, course.code + '-' + course.cname))
  form.course.choices = courseChoices

  if request.method == 'POST':
    course_code = form.course.data
    course_name = Course.query.filter_by(code = course_code).first().cname
    context = buildqrjson(False, form.time.data, course_code, course_name)
    return render_template('qr.html', qrStr=context)
  return render_template('checkout.html', form=form)

def buildqrjson(bCheckin, date, code, course):
  res = {}
  res["check"] = "In" if bCheckin else "Out"
  res["date"] = date
  res["course_code"] = code
  res["course"] = course
  return json.dumps(res)
def buildcheckinurl(date, code, sid):
  url = 'http://52.53.254.77:7777/checkinstudent/'
  url += code
  url += '?'
  url += 'sid='
  url += sid
  url += '&flag=deviceid&addi='
  #url += deviceid
  return url

	
@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

@app.route('/management')
def management():
  form = ManagementForm()
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    items = {}
    # Populate the table
    table = EnrollTable(items)

    return render_template('management.html', table =table)
	


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if 'email' in session:
    return redirect(url_for('home')) 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
       
      session['email'] = newuser.email
      return redirect(url_for('home'))
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if 'email' in session:
    return redirect(url_for('home')) 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      session['is_teacher'] = 'N'
      if form.is_teacher():
        session['is_teacher'] = 'Y'

      return redirect(url_for('home'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('home'))

@app.route('/changestatus', methods=['GET', 'POST'])
def changestatus():
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    form = ChangeStatusForm()
    courses = Course.query.filter_by(ins_id = user.uid).all()
    courseChoices = []
    for course in courses:
      courseChoices.append((course.code, course.code + '-' + course.cname))
    form.course.choices = courseChoices
    studentChoices = []
    studentLinks = StudentCourseLink.query.filter_by(cid=courses[0].cid).all()
    for link in studentLinks:
      stu = Student.query.filter_by(sid=link.sid).first()
      sname = stu.sfirstname + ' ' + stu.slastname
      studentChoices.append((link.sid, str(link.sid) + ' - ' + sname))
    form.student.choices = studentChoices

    if request.method == 'POST':
      status = form.att.data
      stu_id = form.student.data
      date = form.time.data
      course_code = form.course.data
      course_id = Course.query.filter_by(code = course_code).first().cid
      stu2 = Student.query.filter_by(sid=int(stu_id)).first()
      sname2 = stu2.sfirstname + ' ' + stu2.slastname
      exsiting = Attendance.query.filter_by(stu_id = stu_id, course_id = course_id, date = date).first()
      checkin_time = ''
      checkout_time = ''
      if exsiting is not None:
        checkin_time = exsiting.checkin_time
        checkout_time = exsiting.checkout_time
        db.session.delete(exsiting)
        db.session.commit()
      additional = 'manually checked in'
      newatt = Attendance(checkin_time, checkout_time, date, status, sname2, stu_id, course_code, course_id, additional)
      db.session.add(newatt)
      db.session.commit()

    return render_template('changestatus.html', form=form)


@app.route('/summary', methods=['GET', 'POST'])
def summary():
  form = SummaryForm()
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:

    courses = Course.query.filter_by(ins_id = user.uid).all()
    courseChoices = []
    for course in courses:
      courseChoices.append((course.code, course.code + '-' + course.cname))
    form.course.choices = courseChoices

    date = form.time.data
    ccode = courses[0].code
    if request.method == 'POST':
      ccode = form.course.data
      date = form.time.data
    course_name = Course.query.filter_by(code = ccode).first().cname
    attList = Attendance.query.filter_by(course_code=ccode, date=date).all()
    rows = []
    for att in attList:
      row = {}
      row['course_code'] = att.course_code
      row['course_name'] = course_name
      row['stu_id'] = att.stu_id
      row['stu_name'] = att.stu_name
      row['checkin_time'] = att.checkin_time
      row['checkout_time'] = att.checkout_time
      row['addi'] = att.additional
      row['status'] = att.status
      rows.append(row)
    sTable = AttendanceTable(rows)

    return render_template('summary.html', form=form, table=sTable)

@app.route('/signinstudent/<stuid>')
def signinstudent(stuid):
  signinstu = {}
  signinstu['success'] = False
  signinstu['error'] = 'Student ID / Name not matching'
  sid = stuid
  sname = request.args.get('name')
  sfirst = sname.split('_')[0]
  slast = sname.split('_')[1]
  student = Student.query.filter_by(sid = sid).first()
  if student is not None and sfirst == student.sfirstname and slast == student.slastname:
    signinstu['success'] = True
    signinstu['error'] = ''
  return jsonify(signinstu) 

@app.route('/checkinstudent/<coursecode>')
def checkinstudent(coursecode):
  checkinstu = {}
  checkinstu['success'] = False
  checkinstu['error'] = 'Student not registered for the course'
  ccode = coursecode
  stuid = request.args.get('sid')
  flag = request.args.get('flag')
  addi = request.args.get('addi')

  course = Course.query.filter_by(code = ccode).first()
  if course is None:
    checkinstu['error'] = 'Course not exists'
    return jsonify(checkinstu)
  cid = course.cid
  link = StudentCourseLink.query.filter_by(cid = cid, sid = stuid).first()
  if link is None:
    return jsonify(checkinstu) 

  #do checkin
  status = 'Yes'
  checkin_time = datetime.datetime.now(timezone('US/Pacific'));
  checkout_time = ''
  date = checkin_time.date()
  #date = date.astimezone(timezone('US/Pacific'))
  student = Student.query.filter_by(sid = stuid).first()
  if student is None:
    checkinstu['error'] = 'Student not exists'
    return jsonify(checkinstu)
  stu_name = student.sfirstname + ' ' + student.slastname
  stu_id = stuid
  course_code = ccode
  course_id = cid
  additional = ''
  if flag is not None and addi is not None:
    additional = flag + ': ' + addi
  newatt = Attendance(checkin_time, checkout_time, date, status, stu_name, stu_id, course_code, course_id, additional)
  try:
    exsiting = Attendance.query.filter_by(stu_id = stu_id, course_id = course_id, date = date).first()
    if exsiting is not None:
      db.session.delete(exsiting)
      db.session.commit()

    db.session.add(newatt)
    db.session.commit()
    checkinstu['success'] = True
    checkinstu['error'] = ''
  except:
    checkinstu['error'] = 'Server Error'
  return jsonify(checkinstu) 

@app.route('/checkoutstudent/<coursecode>')
def checkoutstudent(coursecode):
  checkoutstu = {}
  checkoutstu['success'] = False
  checkoutstu['error'] = 'Student not registered for the course'
  ccode = coursecode
  stuid = request.args.get('sid')
  flag = request.args.get('flag')
  addi = request.args.get('addi')

  course = Course.query.filter_by(code = ccode).first()
  if course is None:
    checkoutstu['error'] = 'Course not exists'
    return jsonify(checkoutstu)
  cid = course.cid
  link = StudentCourseLink.query.filter_by(cid = cid, sid = stuid).first
  if link is None:
    return jsonify(checkoutstu) 

  #do checkin
  status = 'No'
  checkin_time = ''
  checkout_time = datetime.datetime.now(timezone('US/Pacific'))
  date = checkout_time.date()
  #date = date.astimezone(timezone('US/Pacific'))
  student = Student.query.filter_by(sid = stuid).first()
  if student is None:
    checkoutstu['error'] = 'Student not exists'
    return jsonify(checkoutstu)
  stu_name = student.sfirstname + ' ' + student.slastname
  stu_id = stuid
  course_code = ccode
  course_id = cid
  additional = ''
  if flag is not None and addi is not None:
    additional = flag + ': ' + addi
  try:
    exsiting = Attendance.query.filter_by(stu_id = stu_id, course_id = course_id, date = date).first()
    if exsiting is None:
      newatt = Attendance(checkin_time, checkout_time, date, status, stu_name, stu_id, course_code, course_id, additional)
      db.session.add(newatt)
      db.session.commit()
      checkoutstu['success'] = True
      checkoutstu['error'] = ''
    else:
      checkin_time = exsiting.checkin_time
      aid = exsiting.aid
      status = exsiting.status
      db.session.delete(exsiting)
      db.session.commit()
      newatt = Attendance(checkin_time, checkout_time, date, status, stu_name, stu_id, course_code, course_id, additional, aid)
      db.session.add(newatt)
      db.session.commit()
      checkoutstu['success'] = True
      checkoutstu['error'] = ''

  except:
    return sys.exc_info()[0]
    checkoutstu['error'] = 'Server Error'
  return jsonify(checkoutstu) 


if __name__ == '__main__':
  app.run(debug=True)