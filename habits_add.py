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
        print(request.form)
    # Handle the "Update Habits" button
        if 'update' in request.form:
            # Read the CSV file
            with open("habits.csv", mode="r") as file:
                reader = csv.DictReader(file)
                habits = [row for row in reader]

            # Update the count for completed habits
            counter = []
            for habit in habit_form.habits:
                habitid = str(habit['habitid'])
                habit_name = 'completed-' + habitid
                if habit_name in request.form:
                    for row in habits:
                        value = request.form[habit_name]
                        if row['Name'] == value and not habit in counter:
                            row['Count'] = int(row['Count']) + 1
                            counter.append(habit)

                           

            # for habit in habit_form.habits:
            #     i = 0
            #     habitid = str(habit['habitid'])
            #     habit_name = 'completed-' + habitid
            #     if habit_name in request.form[habit_name]:
            #         habits[i]['Count'] += 1
            #         i += 1


            # Write the updated data back to the CSV file
            with open("habits.csv", mode="w", newline='\n') as file:
                writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
                writer.writeheader()
                writer.writerows(habits)


    return render_template('habits_form.html', task_form=task_form, habit_form=habit_form)

if __name__ == '__main__':
    app.run(debug=True)
