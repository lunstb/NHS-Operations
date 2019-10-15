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
    rowsCount1 = c.execute(
        "SELECT id FROM students WHERE email = \'%s\'" % email)
    rowsCount2 = c.execute(
        "SELECT studentID FROM non_nhs WHERE email = \'%s\'" % email)
    c.close()
    return (rowsCount1 + rowsCount2) != 0


def insertStudent(row):
    c = db.cursor()
    studentID = row[0]
    email = row[1]
    code = makeid(12)
    print(email)
    print(code)
    # Salt First Last Code email
    print("INSERT INTO non_nhs (studentID, email, password, score, code, verified, timeCode) VALUES(\'{0}\', \'{1}\', NULL, 0, \'{2}\',0, CURRENT_TIMESTAMP)".format(
        studentID, email, code))
    c.execute("INSERT INTO non_nhs (studentID, email, password, score, code, verified, timeCode) VALUES(\'{0}\', \'{1}\', NULL, 0, \'{2}\',0, CURRENT_TIMESTAMP)".format(
        studentID, email, code))
    sendEmailCreateAccount(email, code)
    c.connection.commit()


def sendEmailCreateAccount(email, code):
    print(email)
    #msg = Message("NHS Account")
    # msg.add_recipient(email)

    # This code doesn't work well yet but whatever
    #msg.html = ("<p>Hello {0}, <br>  We created your NHS account, please go log into it so you can start getting and viewing your volunteering hours. The link is moundsviewnhs.com and your code is {1}. Let us know if you have any questions. <br> From, Berke and Peter</p>".format(firstName, code))
    # mail.send(msg)
    # time.sleep(10)


def makeid(l):
    text = ""
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    # This code generates a random id with a certain length, it could be a lot better
    for x in range(l):
        text += possible[random.randint(0, len(possible) - 1)]

    return text
