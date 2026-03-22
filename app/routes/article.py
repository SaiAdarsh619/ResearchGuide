from flask import Blueprint, render_template
from utils import fetch_full_article

view_article_blueprint = Blueprint("view_article", __name__)


@view_article_blueprint.route("/<article_id>")
def view_article(article_id):
    article = fetch_full_article(article_id)
    return render_template("article.html", content=article)
