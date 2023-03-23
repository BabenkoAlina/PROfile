from flask import Flask, session, render_template, request, redirect
import pyrebase
from services.list import *
from services.goal import *
from datetime import datetime
import calendar
from csv import writer

app = Flask(__name__)
# TODO: get id dynamically
USER_ID=1

firebaseConfig = {
    'apiKey': "AIzaSyAXoO8gg9C8_osWeI3YgUoOZ5Y3_QndNiI",
    'authDomain': "profile-3403b.firebaseapp.com",
    'projectId': "profile-3403b",
    'storageBucket': "profile-3403b.appspot.com",
    'messagingSenderId': "346310265739",
    'appId': "1:346310265739:web:97398d6f17b6945147fd8e",
    'databaseURL': ""
  }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])
def main():
    print(session)
    if "email" not in session:
        return redirect('/login')
    else:
        return render_template('goals_home.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "email" in session:
        return "Logged in as " + session['email']
    if request.method == 'POST':
        email = request.json["email"]
        password = request.json["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['email'] = email
            return "", 302
        except:
            return '{"error": "Failed to login"}'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if ('email' in session):
        return "Logged in as " + session['email']
    if request.method == 'POST':
        email = request.json["email"]
        password = request.json["password"]

        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['email'] = email
            write_csv(user['localId'], email)
            return "", 302
        except Exception as e:
            return '{"error": "Failed to login"}', 200  
    return render_template('signup.html')

def write_csv(localId, email):
    with open('users.csv', 'a') as f:
        f.write(localId + ',' + email +'\n')
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

@app.get("/goals")
def index():
    """
    Get main page from templates.
    """
    return render_template("goals_home.html", lists=get_lists_by_user_id(USER_ID))

@app.route('/<name>')
def goals(name):
    """
    Redirect to the page with specific goals (weekly).
    """
    # if folder exists
    # if no - error page
    # get goals for current folder

    goals = [] #get_goals(user_id, name)
    return render_template('goals_list.html', list_name = name, goals = goals)

@app.post('/folder')
def add_folder():
    """
    Create new folder (list) for goals and save it for the user.
    """
    list_name = request.form.get('list')
    create_list_by_user_id(USER_ID, list_name)

    return redirect('/goals')

@app.route('/diary')
def page():
    dt = datetime.now()
    week = dt.strftime('%A')
    currentMonth = datetime.now().month
    return render_template('try.html', month=calendar.month_name[currentMonth], year=datetime.now().year, week=week)

@app.route('/write_csv', methods=['POST'])
def write_csv():
    day_info = [datetime.today().strftime('%Y-%m-%d'), request.form['module'], request.form['value'], \
        request.form['body'], request.form['km'], request.form['heart'], \
        request.form['emotion'], request.form['intelegance'], \
        request.form['action'], request.form['good'], request.form['bad'], \
        request.form['improve'], request.form['day'], request.form['rival']]
    with open('user_info.csv', 'a', encoding='utf-8') as file:
        writer_object = writer(file)
        writer_object.writerow(day_info)
    return render_template('response.html')

if __name__ == '__main__':
    app.run(port=1111, debug=True)