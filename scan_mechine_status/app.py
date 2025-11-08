from flask import Flask, render_template
from db import HostStatusDB

app = Flask(__name__)


@app.route("/")
def index():
    with HostStatusDB() as conn:
        hosts = conn.query_status()

    return render_template("index.html", hosts=hosts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
