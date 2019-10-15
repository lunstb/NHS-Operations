from lib import db
import datetime
from datetime import timedelta
from flask_mail import Mail, Message
import random
import time


def initialize(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'moundsviewnhs@gmail.com'
    app.config['MAIL_PASSWORD'] = 'MVNHS.621!'
    app.config['MAIL_DEFAULT_SENDER'] = 'moundsviewnhs@gmail.com'
    app.config['MAIL_MAX_EMAILS'] = 1
    global mail
    mail = Mail(app)


def doesStudentExist(email):
    c = db.cursor()
    print("SELECT id FROM students WHERE email = \'%s\'" % email)
    rowsCount = c.execute(
        "SELECT id FROM students WHERE email = \'%s\'" % email)
    c.close()
    return rowsCount != 0


def studentHasPassword(email):
    c = db.cursor()
    rowsCount = c.execute(
        "SELECT id FROM students WHERE email = \'%s\' AND password IS NOT NULL" % email)
    if rowsCount > 0:
        c.close()
        return "Password Set"
    else:
        c.execute("SELECT code FROM students WHERE email = \'%s\'" % email)
        (code) = c.fetchone()
        c.close()
        return code[0]


def insertStudent(row):
    print("yeezy")
    c = db.cursor()
    salt = makeid(12)
    code = makeid(7)
    print(salt)
    print(code)
    # Salt First Last Code email
    print("INSERT INTO students (salt, first, last, year, coordinator, code, email, password, sid, login) VALUES(\'{0}\', \'{1}\', \'{2}\', 11, 0, \'{3}\', \'{4}\', NULL, NULL, CURRENT_TIMESTAMP)".format(
        salt, row[0], row[1], code, row[2]))
    c.execute("INSERT INTO students (salt, first, last, year, coordinator, code, email, password, sid, login) VALUES(\'{0}\', \'{1}\', \'{2}\', 11, 0, \'{3}\', \'{4}\', NULL, NULL, CURRENT_TIMESTAMP)".format(
        salt, row[0], row[1], code, row[2]))
    sendEmailCreateAccount(row, code)
    c.connection.commit()


def sendEmailWithCode(row, code):
    firstName = row[0]
    lastName = row[1]
    email = row[2]
    code = code

    msg = Message("NHS Account")
    msg.add_recipient(email)

    # This code doesn't work well yet but whatever
    msg.html = ("<p>Hello {0}, <br><br>  Please go log in to your NHS account so you can start getting and viewing your volunteering hours. The link is moundsviewnhs.com and your code is {1}. Let us know if you have any questions. <br><br> From, Berke and Peter</p>".format(firstName, code))
    print(msg.html)
    mail.send(msg)
    time.sleep(10)


def sendEmailCreateAccount(row, code):
    firstName = row[0]
    lastName = row[1]
    email = row[2]
    code = code

    msg = Message("NHS Account")
    msg.add_recipient(email)

    # This code doesn't work well yet but whatever
    msg.html = ("<p>Hello {0}, <br>  We created your NHS account, please go log into it so you can start getting and viewing your volunteering hours. The link is moundsviewnhs.com and your code is {1}. Let us know if you have any questions. <br> From, Berke and Peter</p>".format(firstName, code))
    mail.send(msg)
    time.sleep(10)


def makeid(l):
    text = ""
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    # This code generates a random id with a certain length, it could be a lot better
    for x in range(l):
        text += possible[random.randint(0, len(possible) - 1)]

    return text
