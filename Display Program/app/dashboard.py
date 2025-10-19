import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from .psn_client import PSNClient

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

_psn_client = PSNClient()


@app.route("/", methods=["GET"])
def index():
    online_id = os.environ.get("PSN_ONLINE_ID", "LN_Lenost")
    data = _psn_client.get_user_trophies_summary(online_id).to_dict()
    return render_template("index.html", data=data, online_id=online_id, real=_psn_client.available)


@app.route("/view", methods=["POST"]) 
def view():
    online_id = os.environ.get("PSN_ONLINE_ID", "LN_Lenost")
    data = _psn_client.get_user_trophies_summary(online_id).to_dict()
    return render_template("index.html", data=data, online_id=online_id, real=_psn_client.available)


@app.route("/user/<online_id>", methods=["GET"]) 
def user_view(online_id: str):
    online_id = (online_id or "").strip()
    if not online_id:
        flash("Missing Online ID.", "error")
        return redirect(url_for("index"))

    data = _psn_client.get_user_trophies_summary(online_id).to_dict()
    return render_template("index.html", data=data, online_id=online_id, real=_psn_client.available)


if __name__ == "__main__":
    app.run(debug=True)
