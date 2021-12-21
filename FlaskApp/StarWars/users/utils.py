import secrets, os
from PIL import Image
from flask import url_for, current_app
from StarWars import mail
from flask_mail import Message


def save_picture(form_picture):
    randomn_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = randomn_hex + file_ext
    picture_path = os.path.join(current_app.root_path, "static/images/profile_pic", picture_fn)
    
    output_size = (125, 125)
    resized_img = Image.open(form_picture)
    resized_img.thumbnail(output_size)
    resized_img.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('PASSWORD RESET REQUEST', sender = 'noreply@demo.com', recipients = [user.email])
    msg.body = f'''To reset your password, visit the link:{url_for('users.Reset_Password', token = token, _external = True)}.

If you did not make this request, then ignore this email and no changes will be made to your account. 
'''
    mail.send(msg)