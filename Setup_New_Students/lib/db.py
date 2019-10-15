from flaskext.mysql import MySQL
import pymysql.cursors

# avoid NameError prior to execution of `initialize`
mysql = None

# prepare application to connect to the database


def initialize(app):
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'Mustangs19!'
    app.config['MYSQL_DATABASE_DB'] = 'nhs'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_PORT'] = 33066
    global mysql
    mysql = MySQL()
    mysql.init_app(app)
# create database connection


def cursor():
    global mysql
    return mysql.connect().cursor()
