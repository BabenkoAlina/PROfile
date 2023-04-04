from flask import render_template, redirect, url_for
import datetime
import habits_add as ha

app = ha.Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'secret'
# userID = session["localID"]
# userID = 123

def show_habits():
    habits = ha.read_habits()
    return render_template('habits.html', habits=habits)

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

@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    task_form = ha.TaskForm()
    habit_name = task_form.task.data
    habits = ha.write_new_habit(habit_name)
    ha.write_habits(habits)
    habit_id = ha.write_new_habit(habit_name)
    new_habit = {'User ID': 1, 'Habit ID': habit_id, 'Name': habit_name, 'Count': 0}
    habits.append(new_habit)

    return redirect(url_for('index'))


# function to write the habit data to CSV file
def write_csv():
    habits = ha.read_habits()
    ha.write_habits(habits)

# update habit route to update the count of a habit

@app.route('/update_habit', methods=['GET', 'POST'])
def update_habit():
    ha.update_habit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
