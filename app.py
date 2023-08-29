import datetime
import os
from flask import Flask, render_template, request, Response,redirect
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    client = MongoClient(os.getenv('MONGODB_URI')) #Copy it from mongo compass application
    app.db = client.Microblog #Name should be same as name of data base in MongoDB
    @app.route("/", methods=['GET','POST'])
    def home():
        if request.method=='POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({'content':entry_content,'date':formatted_date}) ## .insert_many() > for inserting a multiple documents/entries <https://pymongo.readthedocs.io/en/stable/changelog.html#breaking-changes-in-4-0>
        entries_with_date=[
        (
            entry['content'],
            entry['date'],
            datetime.datetime.strptime(entry['date'],"%Y-%m-%d").strftime("%b %d")
        )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html",entries=entries_with_date)
        

    @app.route('/entries')
    def view_entries():
        entries_with_date=[
            (
                entry['content'],
                entry['date'],
                datetime.datetime.strptime(entry['date'],"%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template('entries.html',entries=entries_with_date)
    

    @app.route('/login',methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            # app.db.users.insert_one({'user':[{'username':username,'password':password}]})
            user_check=[
                (
                    user['username'],
                    user['password']
                )
                for user in app.db.users.find({})
            ]
            print(f'user_check >> {user_check}')
            try:
                if username==user_check[0] and password==user_check[1]:
                    return home()
            except:
                print('try again')

        return render_template('login.html')

    return app
