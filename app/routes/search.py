from flask import Blueprint, request, render_template
from utils import build_search_query, parse_arxiv_response
import requests

search_blueprint = Blueprint("search", __name__)


@search_blueprint.route("/", methods=["POST"])
def search():
    form_data = {
        "query": request.form.get("query"),
        "author": request.form.get("author"),
        "organization": request.form.get("organization"),
        "published_from": request.form.get("published_from"),
        "published_to": request.form.get("published_to"),
        "keywords": request.form.get("keywords"),
    }

    query = build_search_query(form_data)

    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results=5"

    response = requests.get(url)
    papers = parse_arxiv_response(response.text)

    return render_template("results.html", papers=papers)
