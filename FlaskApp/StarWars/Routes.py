import secrets, os
from PIL import Image
from flask import request, render_template, redirect, flash, url_for, abort
from StarWars import app, db, bcrypt, mail
from StarWars.Forms import RegisterationForm, LoginForm, UpdateForm, PostForm, RequestResetForm, ResetPasswordForm
from StarWars.Models import User, Article
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message









