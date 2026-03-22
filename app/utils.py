import requests
from xml.etree import ElementTree

ARXIV_API_URL = "http://export.arxiv.org/api/query"


def build_search_query(form_data):
    query_parts = []

    if form_data.get("query"):
        query_parts.append(f"all:{form_data['query']}")

    if form_data.get("author"):
        query_parts.append(f"author:{form_data['author']}")

    if form_data.get("organization"):
        query_parts.append(f"affil:{form_data['organization']}")

    if form_data.get("published_from") and form_data.get("published_to"):
        query_parts.append(
            f"submittedDate:[{form_data['published_from']} TO {form_data['published_to']}]"
        )

    if form_data.get("keywords"):
        query_parts.append(f"abs:{form_data['keywords']}")

    return " AND ".join(query_parts)


def parse_arxiv_response(response_text):
    root = ElementTree.fromstring(response_text)
    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        paper = {
            "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
            "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
            "authors": ", ".join(
                author.find("{http://www.w3.org/2005/Atom}name").text
                for author in entry.findall("{http://www.w3.org/2005/Atom}author")
            ),
            "published": entry.find("{http://www.w3.org/2005/Atom}published").text,
            "id": entry.find("{http://www.w3.org/2005/Atom}id").text,
        }
        papers.append(paper)

    return papers


def fetch_full_article(article_id):
    params = {"id_list": article_id}

    response = requests.get(ARXIV_API_URL, params=params, timeout=30)
    response.raise_for_status()

    root = ElementTree.fromstring(response.text)
    entry = root.find("{http://www.w3.org/2005/Atom}entry")

    if entry is None:
        return {"error": "Article not found"}

    return {
        "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
        "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
    }
