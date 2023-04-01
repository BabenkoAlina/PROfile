from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret'

class TaskForm(FlaskForm):
    task = StringField('Habit', validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class HabitForm(FlaskForm):
    habits = []

def write_new_habit(habitName):
    dict_habit = {'User ID': 1, 'Habit ID': 1, 'Name': habitName, 'Count': 0}
    with open("habits.csv", mode="a", newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
        writer.writerow(dict_habit)

@app.route('/', methods=['GET', 'POST'])
def index():
    task_form = TaskForm()
    habit_form = HabitForm()

    if task_form.validate_on_submit():
        habit = {'userid': 1, 'habitid': 1, 'name': task_form.task.data, 'completed': False}
        habit_form.habits.append(habit)

        # Write the new habit to CSV
        write_new_habit(task_form.task.data)

        return redirect(url_for('index'))

    if request.method == 'POST':
        # Handle the "Update Habits" button
        if 'update' in request.form:
            # Read the CSV file
            with open("habits.csv", mode="r") as file:
                reader = csv.DictReader(file)
                habits = [row for row in reader]

            # Update the count for completed habits
            for habit in habit_form.habits:
                if habit['completed']:
                    for row in habits:
                        if row['Name'] == habit['name']:
                            row['Count'] = int(row['Count']) + 1

            # Write the updated data back to the CSV file
            with open("habits.csv", mode="w", newline='\n') as file:
                writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
                writer.writeheader()
                writer.writerows(habits)

    return render_template('habits_form.html', task_form=task_form, habit_form=habit_form)

if __name__ == '__main__':
    app.run(debug=True)
