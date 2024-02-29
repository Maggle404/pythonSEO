from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
from itertools import islice
from urllib.parse import urlparse, urljoin

bcrypt = Bcrypt()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/pythonseo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

def connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pythonseo'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

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
    broken_internal_links = db.Column(db.String(255))
    broken_external_links = db.Column(db.String(255))
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

class UserUrl(FlaskForm):
    url = StringField('URL à analyser', validators=[DataRequired()])

class UserForm(FlaskForm):
    email = StringField('Votre mail', validators=[DataRequired()])
    password = PasswordField('Votre mot de passe', validators=[DataRequired()])


@app.route('/inscription', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.add(Users(email=email, password=hashed))
        db.session.commit()
        return redirect(url_for('login')) #remplacer par une bonne url
    return render_template('/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home.html')) #remplacer par une bonne url
        else:
            return "Invalid"

    return render_template('/login.html', form=form)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
        form = UserUrl()
        if form.validate_on_submit():
            url = form.url.data
            # Appelez la fonction d'analyse avec l'URL fournie
            analyze_url(url)
            return redirect(url_for('result'))  # ou une autre page de votre choix
        return render_template('analyze_form.html', form=form)

@app.route('/result')
def result():
    # Supposons que vous récupériez les données d'analyse depuis la base de données
    analysis_data = Analysis.query.first()  # Cela récupère la première ligne de la table Analysis, vous devrez ajuster cela selon votre logique

    return render_template('result.html', analysis_data=analysis_data)
def extract_domain_name(url):
    if 'www' in url:
        www_domain = url.split('.')
        return www_domain[1]
    else:
        domain = urlparse(url).netloc
        domain_parts = domain.split('.')
        return domain_parts[0]
def get_links(url, soup):
    links = soup.find_all('a')
    domain_name = extract_domain_name(url)
    internal_links = list(islice((link for link in links if domain_name in urlparse(link.get('href')).netloc or link.get('href').startswith(('/', '#'))), 10))
    external_links = list(islice((link for link in links if link.get('href') and not link.get('href').startswith(('/', '#')) and domain_name not in urlparse(link.get('href')).netloc), 10))

    broken_internal_links = []
    broken_external_links = []

    for link in internal_links:
        href = link.get("href")
        full_url = urljoin(url, href)
        response = requests.get(full_url)
        if response.status_code == 404:
            broken_internal_links.append(href)

    for link in external_links:
        href = link.get("href")
        full_url = urljoin(url, href)
        response = requests.get(full_url)
        if response.status_code == 404:
            broken_external_links.append(href)

    return links, internal_links, external_links, broken_internal_links, broken_external_links


def analyze_url(url):
    conn = connection()
    cursor = None
    if conn is not None:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.title
            links, internal_links, external_links, broken_internal_links, broken_external_links = get_links(url, soup)
            h1_tag = soup.h1
            h2_tags = soup.find_all('h2')
            h3_tags = soup.find_all('h3')
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            header_tag = soup.header is not None
            main_tag = soup.main is not None
            footer_tag = soup.footer is not None
            nav_tags = soup.find_all('nav')
            div_tags = soup.find_all('div')

            cursor = conn.cursor()
            query = ("INSERT INTO analysis (user_id, url, title_tag,"
                     "internal_links, external_links, broken_internal_links,"
                     "broken_external_links, h1_tag, h2_tags, h3_tags, img_without_alt,"
                     "header_tag, main_tag, footer_tag, nav_tags, div_nesting)"
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            params = [
                1,
                url if url is not None else None,
                title_tag.string if title_tag and title_tag.string is not None else None,
                len(internal_links) if internal_links is not None else None,
                len(external_links) if external_links is not None else None,
                ', '.join(broken_internal_links) if broken_internal_links is not None else None,
                ', '.join(broken_external_links) if broken_external_links is not None else None,
                h1_tag.string if h1_tag and h1_tag.string is not None else None,
                len(h2_tags) if h2_tags is not None else None,
                len(h3_tags) if h3_tags is not None else None,
                len(images_without_alt) if images_without_alt is not None else None,
                header_tag if header_tag is not None else None,
                main_tag if main_tag is not None else None,
                footer_tag if footer_tag is not None else None,
                len(nav_tags) if nav_tags is not None else None,
                len(div_tags) if div_tags is not None else None
            ]

            cursor.execute(query, params)
            conn.commit()
        except Error as e:
            print(f"Erreur lors de l'ajout de l'analyse : {e}")
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)