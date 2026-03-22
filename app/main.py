from flask import Flask, render_template
from routes.search import search_blueprint
from routes.summarize import summarize_blueprint

app = Flask(__name__, template_folder="../templates")

app.register_blueprint(search_blueprint, url_prefix="/search")
app.register_blueprint(summarize_blueprint, url_prefix="/summarize")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
