<<<<<<< Updated upstream
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/pythonseo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    url = db.Column(db.String(255))
    title_tag = db.Column(db.String(255))
    internal_links = db.Column(db.Integer)
    external_links = db.Column(db.Integer)
    broken_internal_links = db.Column(db.Integer)
    broken_external_links = db.Column(db.Integer)
    h1_tag = db.Column(db.String(255))
    h2_tags = db.Column(db.Integer)
    h3_tags = db.Column(db.Integer)
    img_without_alt = db.Column(db.Integer)
    header_tag = db.Column(db.Boolean)
    main_tag = db.Column(db.Boolean)
    footer_tag = db.Column(db.Boolean)
    nav_tags = db.Column(db.Integer)
    div_nesting = db.Column(db.Integer)

with app.app_context():
    db.create_all()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


if __name__ == "__main__":
=======
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/pythonseo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    url = db.Column(db.String(255))
    title_tag = db.Column(db.String(255))
    internal_links = db.Column(db.Integer)
    external_links = db.Column(db.Integer)
    broken_internal_links = db.Column(db.Integer)
    broken_external_links = db.Column(db.Integer)
    h1_tag = db.Column(db.String(255))
    h2_tags = db.Column(db.Integer)
    h3_tags = db.Column(db.Integer)
    img_without_alt = db.Column(db.Integer)
    header_tag = db.Column(db.Boolean)
    main_tag = db.Column(db.Boolean)
    footer_tag = db.Column(db.Boolean)
    nav_tags = db.Column(db.Integer)
    div_nesting = db.Column(db.Integer)

with app.app_context():
    db.create_all()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


if __name__ == "__main__":
>>>>>>> Stashed changes
    app.run(debug=True)