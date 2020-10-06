from blog import app, db
from flask import render_template, redirect, flash, session, get_flashed_messages
from flask_login import login_user, current_user, logout_user, login_required
from blog.forms import RegistrationForm, LoginForm, ProfileUpdateForm, PostForm
from blog.models import User, Post
from blog.utils import save_image


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
    if current_user.is_authenticated:
        return redirect("/")
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
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash(f'Login Successful', 'success')
            return redirect("/")
        else:
            flash(f'Incorrect email/password', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            current_user.image_file = save_image(form.picture.data)
        db.session.commit()
        flash('Your profile was updated', 'success')
        return redirect("/profile")
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('profile.html', title_name='profile', form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('You post has been created', 'success')
        return redirect("/")
    return render_template('create_post.html', title_name='New Post', form=form)