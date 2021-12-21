from flask import request, render_template, redirect, flash, url_for, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from StarWars import db, bcrypt
from StarWars.users.forms import RegisterationForm, LoginForm, UpdateForm, RequestResetForm, ResetPasswordForm
from StarWars.Models import User, Article
from StarWars.users.utils import save_picture, send_reset_email



users = Blueprint('users', __name__)

@users.route("/register", methods = ['GET', 'POST'])
def registerpage():
    if current_user.is_authenticated:
        return redirect(url_for('main.homePage'))
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname = form.fullname.data, 
                    username=form.username.data, 
                    email = form.email.data,
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account was successfully created and you can now login!', "success")
        return redirect(url_for("users.loginpage"))
    return render_template("register.html", title = "Register", form = form)

@users.route("/login", methods = ['GET', 'POST'])
def loginpage():
    if current_user.is_authenticated:
        return redirect(url_for('main.homePage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash("You are now logged in!", 'success')
            return redirect(next_page) if next_page else redirect( url_for("main.homePage"))
        else:
            flash("Invalid Login. Confirm email and password", 'danger' )
    return render_template("login.html", title = "Login", form = form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect( url_for("main.homePage"))



@users.route("/dashboard", methods = ['GET', 'POST'])
@login_required
def dashboardPage():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            user_pic = save_picture(form.picture.data)
            current_user.prof_pic = user_pic
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash("Your account info has been updated", 'success')
        return redirect(url_for('users.dashboardPage'))
    elif request.method == 'GET':
        form.fullname.data = current_user.fullname
        form.username.data = current_user.username
        form.email.data = current_user.email
    user_img = "static/images/profile_pic/" + current_user.prof_pic
    return render_template('dashboard.html', title = "Dashboard", user_img = user_img, form = form)




@users.route('/user/<string:username>')
def User_Posts(username):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Article.query\
    .filter_by(author = user)\
    .order_by(Article.create_date.desc())\
    .paginate(per_page = 3, page = page)
    return render_template('userPosts.html', posts = posts, user = user)


@users.route('/reset_password', methods = ['GET', 'POST'])
def Reset_Request():
    if current_user.is_authenticated:
        return redirect(url_for('main.homePage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to the email provided with instructions on how to reset your password", 'info')
        return redirect(url_for('users.loginpage'))
    return render_template('resetRequest.html', title = "Reset Password", form = form)


@users.route('/reset_password/<token>', methods = ['GET', 'POST'])
def Reset_Password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.homePage'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid or expired reset password token", 'warning')
        return redirect(url_for('users.Reset_Request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been successively updated, you can now login with your new password!', "success")
        return redirect(url_for("users.loginpage"))
    return render_template('resetPassword.html', form = form, title = "Reset Password")