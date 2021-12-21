from flask import request, render_template, redirect, flash, url_for, abort, Blueprint
from flask_login import current_user, login_required
from StarWars import db
from StarWars.Models import Article
from StarWars.posts.forms import PostForm




posts = Blueprint('posts', __name__)

@posts.route("/New Post", methods=['GET', 'POST'])
@login_required
def PostPage():
    form = PostForm()
    if form.validate_on_submit():
        post = Article(title = form.title.data, content = form.content.data, author = current_user )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('main.homePage'))
    return render_template('post.html', form = form, title = 'New Post', legend = 'Create Post')

@posts.route("/Post/<int:post_id>")
def View_Post(post_id):
    post = Article.query.get_or_404(post_id)
    return render_template("ViewPost.html", title = post.title, post = post)


@posts.route("/Post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def Update_Post(post_id):
    post = Article.query.get_or_404(post_id)
    if post.author == current_user:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Your post has been updated!", 'success')
            return redirect(url_for('posts.View_Post', post_id = post.id))
        elif request.method == "GET":
            form.title.data = post.title
            form.content.data = post.content
        return render_template("post.html", post = post, form = form, title = 'Update Post', legend = "Update Post")
    else:
        abort(403)
       

@posts.route("/Post/<int:post_id>/delete", methods = ["GET", "POST"])
@login_required
def Delete_Post(post_id):
    post = Article.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', "success")
    return redirect(url_for('main.homePage'))
