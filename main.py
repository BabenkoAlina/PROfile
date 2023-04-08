from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
import pyrebase
from services.list import *
from services.goal import *
from datetime import datetime
import calendar
import csv
from csv import writer
import pandas as pd
import os
import numpy as np
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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

@app.route('/diary', methods=["GET", 'POST'])
def page():
    dt = datetime.datetime.now()
    week = dt.strftime('%A')
    currentMonth = datetime.datetime.now().month
    return render_template('diary.html', month=calendar.month_name[currentMonth], year=datetime.datetime.now().year, week=week)

@app.route('/write_csv', methods=['POST', 'GET'])
def write_csv():
    day_info = [session['localId'], datetime.datetime.today().strftime('%Y-%m-%d'), request.form['module'], request.form['value'], \
        request.form['body'], request.form['km'], request.form['heart'], \
        request.form['emotion'], request.form['intelegance'], \
        request.form['action'], request.form['good'], request.form['bad'], \
        request.form['improve'], request.form['rival'], request.form['victory']]
    with open('user_info.csv', 'a', encoding='utf-8') as file:
        writer_object = writer(file)
        writer_object.writerow(day_info)
    content = pd.read_csv("user_info.csv")
    content = content.loc[(content.user_id == session['localId']) & (content['date'].str.contains(f'{datetime.datetime.now().year}-{("0" + str(datetime.datetime.now().month)) if len(str(datetime.datetime.now().month))==1 else str(datetime.datetime.now().month)}'))]
    emotion = content['emotion'].value_counts().idxmax()
    session['emotion'] = emotion
    return redirect("/diary_home")

@app.route('/diary_info', methods=['GET', 'POST'])
def show_info():
    data = request.form['date']
    year = int(data[:4])
    month = calendar.month_name[int(data[5:7])]
    my_date = datetime(int(data[:4]), int(data[5:7]), int(data[-2:]))
    weekday= pd.to_datetime(my_date).day_name()
    content = pd.read_csv("user_info.csv")
    content = content.loc[(content.user_id == session['localId']) & (content['date'].str.contains(data))].iloc[0]
    return render_template('diary_info.html', content=content, month=month, year=year, week=weekday)

@app.route('/diary_home', methods=['GET', 'POST'])
def choice():
    return render_template('response3.html')

@app.route('/progress', methods=['GET'])
def progress():
    if 'localId' not in session:
        return redirect('/login')
    df = pd.read_csv('user_info.csv')
    df = df[df.user_id == session['localId']]
    df = df[['date', 'km' ,'emotion', 'action']]
    if not df.empty:
        df.date = np.vectorize(datetime.date.fromisoformat)(df.date)
    days = len(set(df.date))
    today = datetime.date.today()
    last_month_df = df[df.date > today - datetime.timedelta(30)]
    last_week_df = df[df.date > today - datetime.timedelta(7)]
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
        days=days
    )

@app.route('/habits', methods=['GET', 'POST'])
def habits_main():
    if "email" not in session:
        return redirect('/login')
    else:
        context = {
        'datetime': datetime,
        }
        today = datetime.datetime.now()
        today_str = today.strftime("%B %d, %Y")
        habits = read_habits()
        task_form = TaskForm()
        habit_form = HabitForm()
        return render_template('habits.html', task_form=task_form, habit_form=habit_form, habits=habits, today_str=today_str, **context)

class TaskForm(FlaskForm):
    task = StringField('Habit', validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class HabitForm(FlaskForm):
    habits = []

def read_habits():
    with open("habits.csv", mode="r") as file:
        reader = csv.DictReader(file)
        habits = [row for row in reader]
        return habits

def write_habits(habits):
    with open("habits.csv", mode="w", newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
        writer.writeheader()
        writer.writerows(habits)

def write_new_habit(habitName):
    userid = session['localId']
    with open("habits.csv", mode="r+", newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
        # Check if the file is empty
        next(file)
        first_char = file.read(1)
        if not first_char:
            # File is empty, start habitid at 1
            habitid = 1
        else:
            # Read the file to find the maximum habitid
            file.seek(0)
            reader = csv.DictReader(file)
            habitid_list = [int(row['Habit ID']) for row in reader]
            habitid = max(habitid_list) + 1 if habitid_list else 1
        dict_habit = {'User ID': userid, 'Habit ID': habitid, 'Name': habitName, 'Count': 0}
        writer.writerow(dict_habit)

        return habitid


@app.route('/habits', methods=['GET', 'POST'])
def index():
    habits = read_habits()
    task_form = TaskForm()
    habit_form = HabitForm()
    userid = session['localId']
    context = {
        'datetime': datetime,
        }
    today = datetime.datetime.now()
    today_str = today.strftime("%B %d, %Y")

    if task_form.validate_on_submit():
        habit_name = task_form.task.data
        habitid = write_new_habit(habit_name)
        habit = {'userid': userid, 'habitid': habitid, 'name': habit_name, 'completed': False, 'count': 0}
        habit_form.habits.append(habit)
        
        return render_template('habits.html', task_form=task_form, habit_form=habit_form, habits=habits, today_str=today_str, **context)

    if request.method == 'POST':
        # Handle the "Update Habits" button
        if 'update' in request.form:
        # Read the CSV file
            habits = read_habits()
            # Update the count for completed habits
            for habit in habit_form.habits:
                habitid = str(habit['habitid'])
                habit_name = 'completed-' + habitid # Define habit_name here
                if habit_name in request.form:
                    for row in habits:
                        if row['Habit ID'] == habitid:
                            row['Count'] = int(row['Count']) + 1
                            # Update the habit count in the habit_form.habits list
                            habit['completed'] = True
                            habit['count'] = int(row['Count'])
                            break # Exit the inner loop
            # Write the updated data back to the CSV file
            write_habits(habits)
        return render_template('habits.html', task_form=task_form, habit_form=habit_form, habits=habits, today_str=today_str, **context)


if __name__ == '__main__':
    app.run(port=1111, debug=True)