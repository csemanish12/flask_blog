from blog import app, db
from flask import render_template, redirect, flash

from blog.forms import RegistrationForm, LoginForm
from blog.models import User


@app.route("/")
def home():
    posts = [
    {
        'author': 'User first',
        'title': 'blog post one',
        'content': 'These are the contents for the first post',
        'date_posted': '2020-09-19'
    },
    {
        'author': 'User Second',
        'title': 'blog post two',
        'content': 'second post content',
        'date_posted': '2020-09-20'
    }
]
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title_name='about-page')


@app.route("/registration", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'your account has been created! you can now log in', 'success')
        return redirect("/")
    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)