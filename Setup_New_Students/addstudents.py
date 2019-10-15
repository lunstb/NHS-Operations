import csv
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flaskext.mysql import MySQL
from lib import db
from lib import util

app = Flask(__name__)
# CORS(app)
db.initialize(app)
util.initialize(app)
#data = []


def convCSVToList():
    data = list(csv.reader(open("lib/members.csv")))


def checkStudent(row):
    firstName = row[0]
    lastName = row[1]
    email = row[2]
    if email == "" or email == "Email":
        print("Blank email")
    else:
        studentExists = util.doesStudentExist(email)
        print(row[0] + " " + str(studentExists))
        if(studentExists):
            studentHasSetPassword = util.studentHasPassword(email)
            print(studentHasSetPassword)
            if(studentHasSetPassword != "Password Set"):
                print("Student would be emailed here")
                util.sendEmailWithCode(row, studentHasSetPassword)

        else:
            print("Student Would be inserted here")
            util.insertStudent(row)


@app.route('/')
def yay():
    data = list(csv.reader(open("lib/members.csv")))
    for row in data:
        checkStudent(row)
    return "Finished Succesfully"


if __name__ == "__main__":
    app.run()
