import datetime
from flask import Flask, session, render_template, request, redirect, url_for
import pyrebase
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv



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
app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])
def main():
    print(session)
    if "email" not in session:
        return redirect('/login')
    else:
        # Тут треба зарендити свій основний шаблон
        context = {
        'datetime': datetime,
        }
        today = datetime.datetime.now()
        today_str = today.strftime("%B %d, %Y")
        habits = read_habits()
        task_form = TaskForm()
        habit_form = HabitForm()
        return render_template('habits.html', task_form=task_form, habit_form=habit_form, habits=habits, today_str=today_str, **context)

    
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
            # session['localId'] - це і є токен
            session['localId'] = user['localId']
            return "", 302
        except Exception as e:
            return '{"error": "Failed to login"}', 200  
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

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