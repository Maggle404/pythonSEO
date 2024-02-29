from flask import render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired
from main import *
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
class UserForm(FlaskForm):
    email = StringField('Votre mail', validators=[DataRequired()])
    password = PasswordField('Votre mot de passe', validators=[DataRequired()])


@app.route('/inscription', methods=['GET', 'POST'])
def Register():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.add(Users(email=email, password=hashed))
        db.session.commit()
        return redirect(url_for(''))  # remplacer par une bonne url
    return render_template('inscription.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for(''))  # remplacer par une bonne url
        else:
            return "Invalid"

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect(url_for('login'))