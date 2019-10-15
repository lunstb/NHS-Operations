import csv
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flaskext.mysql import MySQL
from lib import db
from lib import util

app = Flask(__name__)
db.initialize(app)
util.initialize(app)


def convCSVToList():
    data = list(csv.reader(open("lib/students.csv")))


def addStudent(row):
    studentID = row[0]
    email = row[1]
    grade = row[2]
    if email == "" or email == "Email":
        print("Blank email")
    else:
        studentExists = util.doesStudentExist(email)
        print(row[0] + " " + str(studentExists))
        if(studentExists == False):
            print("Student Would be inserted here")
            util.insertStudent(row)


@app.route('/')
def runProgram():
    data = list(csv.reader(open("lib/students.csv")))
    for row in data:
        addStudent(row)
    return "Finished Succesfully"


if __name__ == "__main__":
    app.run()
