from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv
import datetime

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'secret'
# userID = session["localID"]
# userID = 123

class TaskForm(FlaskForm):
    task = StringField('Habit', validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class HabitForm(FlaskForm):
    habits = []

# function to read the habit data from CSV file
def read_csv():
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
        dict_habit = {'User ID': 1, 'Habit ID': habitid, 'Name': habitName, 'Count': 0}
        writer.writerow(dict_habit)

        return habitid

# home page route to display the habits list
@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'datetime': datetime,
        # Other context variables...
    }
    today = datetime.datetime.now()
    today_str = today.strftime("%B %d, %Y")
    habits = read_csv()
    return render_template('habits.html', habits=habits, today_str=today_str, **context)


@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    task_form = TaskForm()
    habit_name = task_form.task.data
    write_new_habit(habit_name)

def write_csv():
    habits = read_csv()
    write_habits(habits)

# update habit route to update the count of a habit
@app.route('/update_habit', methods=['GET', 'POST'])
def update_habit():
    task_form = TaskForm()
    habit_form = HabitForm()

    if task_form.validate_on_submit():
        habit_name = task_form.task.data
        habitid = write_new_habit(habit_name)
        habit = {'userid': 1, 'habitid': habitid, 'name': habit_name, 'completed': False, 'count': 0}
        habit_form.habits.append(habit)

        return redirect(url_for('index'))

    if request.method == 'POST':
        # Handle the "Update Habits" button
        if 'update' in request.form:
        # Read the CSV file
            habits = read_csv()
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

    return render_template('habits.html', habit_form=habit_form)

if __name__ == '__main__':
    app.run(debug=True)