from flask import Blueprint, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

from main import *





