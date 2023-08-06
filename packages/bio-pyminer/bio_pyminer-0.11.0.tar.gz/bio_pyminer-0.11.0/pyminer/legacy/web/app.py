from flask import Flask
from flask import render_template

app = Flask(__name__)

# Ignore trailing slash in URL routes
app.url_map.strict_slashes = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/status")
@app.route("/status/<id>")
def status(id=None):
    return render_template("status.html", id = id)

if __name__ == "__main__":
    app.run(host="0.0.0.0")