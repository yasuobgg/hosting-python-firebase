# from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# from send_mail import send_mail


# ENV = 'dev'

# # if ENV == 'dev':
# app.debug = True
# app.config['SQLALCHEMY_DATABASE_URI'] = ''
# # else:
# #     app.debug = False
# #     app.config['SQLALCHEMY_DATABASE_URI'] = ''

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


class Feedback():
    # __tablename__ = 'feedback'
    # id = db.Column(db.Integer, primary_key=True)
    # customer = db.Column(db.String(200), unique=True)
    # dealer = db.Column(db.String(200))
    # rating = db.Column(db.Integer)
    # comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments
    def to_json(self):
        return {
            'customer':self.customer,
            'dealerr':self.dealer,
            'rating':int(self.rating),
            'comments':self.comments
        }


from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS
import pymongo

from bson.json_util import dumps

app=Flask(__name__)
CORS(app)

con_str = 'mongodb+srv://datdatyasuo:25092001dat@beginner.fpt55lp.mongodb.net/?retryWrites=true&w=majority'
#connect to MongoDB Cloud
client = pymongo.MongoClient(con_str)
#connect to db name Football
db = client.get_database("Lexus")
#connect to collection name player(Football.player)
feb = db.feedback


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if customer and dealer and rating and comments:
            cn=Feedback(customer,dealer,rating,comments)
            feb.insert_one(cn.to_json())
            return render_template('success.html')
        # else:
        
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run(debug=True)
