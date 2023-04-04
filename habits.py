from flask import Flask, render_template, request, session
import os
import csv
from flask import render_template
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import habits_add as ha

app = ha.Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'secret'
# userID = session["localID"]
# userID = 123


# function to read the habit data from CSV file
def read_csv():
    ha.read_habits()


# home page route to display the habits list
@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'datetime': datetime,
        # Other context variables...
    }
    today = datetime.datetime.now()
    today_str = today.strftime("%B %d, %Y")
    habits = ha.read_habits()
    return render_template('habits.html', habits=habits, today_str=today_str, **context)


@app.route('/add_habit', methods=['POST'])
def add_habit():
    task_form = ha.TaskForm()
    habit_name = task_form.task.data
    ha.write_new_habit(habit_name)

def write_csv():
    habits = ha.read_habits()
    ha.write_habits(habits)

# update habit route to update the count of a habit
@app.route('/update_habit', methods=['GET', 'POST'])
def update_habit():
    return ha.index()

if __name__ == '__main__':
    app.run(debug=True)