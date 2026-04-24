from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from routes.search import search_blueprint
from routes.summarize import summarize_blueprint
import os

app = Flask(__name__, template_folder="../templates")

# Tell Flask it is behind a proxy to ensure HTTPS redirects
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

app.register_blueprint(search_blueprint, url_prefix="/search")
app.register_blueprint(summarize_blueprint, url_prefix="/summarize")


@app.route("/")
def index():
    return render_template("index.html")

PORT = os.getenv("PORT") or 5000

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
