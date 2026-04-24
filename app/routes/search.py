from flask import Blueprint, request, render_template
from utils import build_search_query, parse_arxiv_response
import requests

search_blueprint = Blueprint("search", __name__)

@search_blueprint.route("/", methods=["GET", "POST"])
def search():
    # Use request.values to support both GET and POST seamlessly
    form_data = {
        "query": request.values.get("query"),
        "author": request.values.get("author"),
        "organization": request.values.get("organization"),
        "published_from": request.values.get("published_from"),
        "published_to": request.values.get("published_to"),
        "keywords": request.values.get("keywords"),
    }
    
    # Try to grab max_results or default to 10 if missing
    max_results = int(request.values.get("max_results", 10))

    query = build_search_query(form_data)
    
    if not query.strip():
        # Fallback if query is completely empty
        return render_template("results.html", papers=[], error="No search terms provided.", query="", max_results=max_results)

    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        papers = parse_arxiv_response(response.text)
        return render_template("results.html", papers=papers, query=form_data["query"] or "", max_results=max_results)
    except Exception as e:
        return render_template("results.html", papers=[], error=f"An error occurred: {e}", query=form_data["query"] or "", max_results=max_results)
