# app lib
from flask import Flask, request, render_template

# db lib and connect
import firebase_admin

cred_obj = firebase_admin.credentials.Certificate(
    "pythoneverywhere-data-firebase-adminsdk-nmn5v-b4906d67a0.json"
)
default_app = firebase_admin.initialize_app(
    cred_obj,
    {
        "databaseURL": "https://pythoneverywhere-data-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)

from firebase_admin import db

ref = db.reference("/")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        customer = request.form["customer"]
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]

        if customer == "" or dealer == "":
            return render_template("index.html", message="Please enter required fields")
        if customer and dealer and rating and comments:  # neu nhap du thong tin
            ref.push(
                {
                    "Feedback": {
                        "customer": customer,
                        "dealer": dealer,
                        "rating": int(rating),
                        "comments": comments,
                    }
                }
            )

            return render_template("success.html")

        return render_template(
            "index.html", message="You have already submitted feedback"
        )


if __name__ == "__main__":
    app.run(debug=True)
