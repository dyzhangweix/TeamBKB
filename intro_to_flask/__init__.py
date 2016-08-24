from flask import Flask
 
app = Flask(__name__)
 
app.secret_key = 'development key'
 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'dyzhangweix@gmail.com'
app.config["MAIL_PASSWORD"] = 'jasonzwx123'


from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dmonkey:123456@52.53.254.77:3306/development'
 
from models import db
db.init_app(app)

from flask.ext.qrcode import QRcode
QRcode(app)

import intro_to_flask.routes