from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config
import models

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Конфигурация базы данных PostgreSQL
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/add_user')
def add_user():
    new_user = models.User(id='123', username='user123', email='newuser@example.com')
    db.session.add(new_user)
    db.session.commit()
    return 'User added!'


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == "__main__":
    u = models.User(id='123', username='susan', email='susan@example.com')
    db.session.add(u)
    db.session.commit()
    app.run(host="0.0.0.0", debug=True)
