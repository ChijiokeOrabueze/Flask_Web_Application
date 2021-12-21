from flask import request, render_template, Blueprint
from StarWars.Models import Article


main = Blueprint('main', __name__)

@main.route("/")
def homePage():
    page = request.args.get('page', 1 , type = int)
    posts = Article.query.order_by(Article.create_date.desc()).paginate(page = page, per_page = 3)
    return render_template("index.html", posts = posts)

@main.route("/aboutUs")
def aboutPage():
    return render_template("about.html", title = "About")