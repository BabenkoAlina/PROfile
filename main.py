from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
import pyrebase
from services.list import *
from services.goal import *
from datetime import datetime
import calendar
from csv import writer
import pandas as pd
import os
import numpy as np
import datetime as datet

app = Flask(__name__)

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
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def main():
    if "email" not in session:
        return redirect('/login')
    else:
        return render_template('goals_home.html', lists=get_lists_by_user_id(session['localId']))

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
            session['localId'] = user['localId']
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
            session['localId'] = user['localId']
            return "", 302
        except Exception as e:
            return '{"error": "Failed to login"}', 200  
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

@app.get('/about')
def index_about():
    """
    Get the "about" page from templates.
    """
    return render_template("about.html")

@app.get('/goals')
def index_goals():
    """
    Get main page from templates.
    """
    return render_template("goals_home.html", lists=get_lists_by_user_id(session['localId']))

@app.route('/goals/<name>')
def goals(name):
    """
    Redirect to the page with specific goals (weekly).
    """
    goals = get_goals_by_user_id(session['localId'], name)
    return render_template('goals_list.html', list_name = name, goals = goals)

@app.post('/goals')
def add_list():
    """
    Create new folder (list) for goals and save it for the user.
    """
    try:
        list_name = request.form.get('list')
        if list_name == '' or list_name is None: 
            raise ValueError('A folder with no name cannot be created!')
        create_list_by_user_id(session['localId'], list_name)
    except ValueError as error:
        flash(str(error), 'error')
    finally:
        return redirect('/goals')
    
@app.delete('/goals/<list_id>')
def delete_list(list_id):
    try:
        if list_id == '' or list_id is None:
            raise ValueError('There is already no such list!')
        delete_particular_list(session['localId'], int(list_id))
        return jsonify({"code": 200, "message": "Successfully deleted the list!"})
    except ValueError:
        return jsonify({"code": 400, "message": "Failed to delete the list!"})

@app.post('/goals/goal')
def add_goal():
    """
    Create new goal and save it for the user.
    """
    try:
        list_name = request.form.get('list_name')
        goal = request.form.get('goal')
        if list_name == '' or list_name is None:
            raise ValueError('There is no such list!')
        if goal == '' or goal is None:
            raise ValueError('A goal cannot be created without description!')
        create_goal_by_user_id(session['localId'], goal, list_name)
    except ValueError as error:
        flash(str(error), 'error')
    finally:
        return redirect(url_for('goals', name=list_name))

@app.delete('/goals/goal/<goal_id>')
def delete_goal(goal_id):
    try:
        if goal_id == '' or goal_id is None:
            raise ValueError('There is already no such goal in the list!')
        change_goal_status(session['localId'], int(goal_id), 'deleted')
        return jsonify({"code": 200, "message": "Successfully deleted the goal!"})
    except ValueError:
        return jsonify({"code": 400, "message": "Failed to delete the goal!"})

@app.put('/goals/goal/<goal_id>')
def complete_goal(goal_id):
    try:
        if goal_id == '' or goal_id is None:
            raise ValueError('There is no such goal in the list!')
        change_goal_status(session['localId'], int(goal_id), 'completed')
        return jsonify({"code": 200, "message": "Successfully completed the goal!"})
    except ValueError:
        return jsonify({"code": 400, "message": "Failed to update the goal!"})

@app.route('/diary')
def page():
    dt = datetime.now()
    week = dt.strftime('%A')
    currentMonth = datetime.now().month
    return render_template('diary.html', month=calendar.month_name[currentMonth], year=datetime.now().year, week=week)

@app.route('/write_csv', methods=['GET', 'POST'])
def write_csv():
    day_info = [session['localId'], datetime.today().strftime('%Y-%m-%d'), request.form['module'], request.form['value'], \
        request.form['body'], request.form['km'], request.form['heart'], \
        request.form['emotion'], request.form['intelegance'], \
        request.form['action'], request.form['good'], request.form['bad'], \
        request.form['improve'], request.form['day'], request.form['rival']]
    with open('user_info.csv', 'a', encoding='utf-8') as file:
        writer_object = writer(file)
        writer_object.writerow(day_info)
    content = pd.read_csv("user_info.csv")
    content = content.loc[(content.user_id == session['localId']) & (content['date'].str.contains(f'{datetime.now().year}-{("0" + str(datetime.now().month)) if len(str(datetime.now().month))==1 else str(datetime.now().month)}'))]
    emotion = content['emotion'].value_counts().idxmax()
    session['emotion'] = emotion
    return render_template('response.html')

@app.route('/diary_info', methods=['GET', 'POST'])
def show_info():
    data = request.form['date']
    year = int(data[:4])
    month = calendar.month_name[int(data[5:7])]
    my_date = datetime(int(data[:4]), int(data[5:7]), int(data[8:]))
    weekday= pd.to_datetime(my_date).day_name()
    content = pd.read_csv("user_info.csv")
    content = content.loc[(content.user_id == session['localId']) & (content['date'].str.contains(data))].fillna('Info not given').iloc[0]
    return render_template('diary_info.html', content=content, month=month, year=year, week=weekday)


@app.route('/progress', methods=['GET'])
def progress():
    if 'localId' not in session:
        return redirect('/login')
    df = pd.read_csv('user_info.csv')
    df = df[df.user_id == session['localId']]
    df = df[['date', 'km' ,'emotion', 'action']]
    df.date = np.vectorize(datet.date.fromisoformat)(df.date)
    today = datet.date.today()
    last_month_df = df[df.date > today - datet.timedelta(30)]
    last_week_df = df[df.date > today - datet.timedelta(7)]
    last_month_km = last_month_df.km.sum()
    last_week_km = last_week_df.km.sum()
    try:
        last_month_emotion = last_month_df.emotion.value_counts().idxmax()
    except ValueError:
        last_month_emotion = ''
    try:
        last_week_emotion = last_week_df.emotion.value_counts().idxmax()
    except ValueError:
        last_week_emotion = ''
    try:
        last_month_action = last_month_df.action.value_counts().idxmax()
    except ValueError:
        last_month_action = ''
    try:
        last_week_action = last_week_df.action.value_counts().idxmax()
    except ValueError:
        last_week_action = ''
    
    goals = pd.read_csv('data/goals.csv')
    goals = goals[goals.user_id == session['localId']]
    goals = goals.status.value_counts().sort_index()

    return render_template(
        'progress.html',
        last_month_km=last_month_km,
        last_month_emotion=last_month_emotion,
        last_month_action=last_month_action,
        last_week_km=last_week_km,
        last_week_emotion=last_week_emotion,
        last_week_action=last_week_action,
    )



if __name__ == '__main__':
    app.run(port=1111, debug=True)
