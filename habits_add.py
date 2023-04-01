from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret'

class TaskForm(FlaskForm):
    task = StringField('Habit', validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class HabitForm(FlaskForm):
    habits = []

@app.route('/', methods=['GET', 'POST'])
def index():
    task_form = TaskForm()
    habit_form = HabitForm()

    if task_form.validate_on_submit():
        habit = {'name': task_form.task.data, 'completed': False}
        habit_form.habits.append(habit)
        return redirect(url_for('index'))

    return render_template('habits_form.html', task_form=task_form, habit_form=habit_form)

if __name__ == '__main__':
    app.run(debug=True)
