from flask_table import Table, Col

# Declare your table
class EnrollTable(Table):
    stu_id = Col('Student ID')
    stu_name = Col('Student Name')

class AttendanceTable(Table):
	course_code = Col('Code')
	course_name = Col('Course Name')
	stu_id = Col('Student ID')
	stu_name = Col('Student Name')
	checkin_time = Col('Checkin Time')
	checkout_time = Col('Checkout Time')
	addi = Col('Additional Info')
	status = Col('Status')

