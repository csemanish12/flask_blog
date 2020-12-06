from marshmallow import EXCLUDE, ValidationError

from blog import app, db
from flask import render_template, redirect, flash, abort, url_for, request, session, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from blog.forms import RegistrationForm, LoginForm, ProfileUpdateForm, PostForm
from blog.models import User, Post
from blog.schemas import PostSchema, PostPlainSchema
from blog.utils import save_image


@app.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    print('beforre dumpoing===', type(posts.items[0]))
    response = PostSchema(many=True).dump(posts.items)
    print(type(response[0]))
    print(posts.__dict__)
    return jsonify(response)
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
#@login_required
def new_post():
    # try:
    #     post_dict = PostPlainSchema().load(request.json)
    #     post_obj = Post(title=post_dict['my-title'], content=post_dict['my-content'], user_id=1)
    #     db.session.add(post_obj)
    #     db.session.commit()
    # except Exception as e:
    #     print(e)
    # print('plain schema====',type(post))

    try:
        posts = PostSchema(many=True).load(request.json, session=db.session, unknown=EXCLUDE)
        for post in posts:
            post.user_id = None
            db.session.add(post)
            db.session.commit()
    except ValidationError as e:

        exception_object = e.__dict__
        return {'error':exception_object ['messages']}, 400
    except Exception as e:
        print(e)
        return {'error': str(e)}
    return {}, 200


    return {'errors': e.messages}, 400

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('You post has been created', 'success')
        return redirect("/")
    return render_template('create_post.html', title_name='New Post', form=form, legend="New Post")


@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post was updated", "success")
        return redirect(url_for('post', post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title_name="Update Post", form=form, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post was deleted", "success")
    return redirect(url_for('home'))


@app.route("/search", methods=["GET", "POST"])
def search():
    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        search_word = request.form['search']
        session['search'] = search_word
    if 'search' in session:
        posts = Post.query.filter(Post.title.ilike(F'%{session["search"]}%')).paginate(per_page=3, page=page)
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template('search_page.html', posts=posts, title_name="Search", search_word=session.get('search'))
