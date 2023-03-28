from flask import Flask, render_template, request, redirect
import pandas as pd
import os
import csv
import datetime

app = Flask(__name__, template_folder="templates")

# function to read the habit data from CSV file
def read_csv():
    filename = "habits.csv"
    dict_habit = {'User ID': 1, 'Habit ID': 1, 'Name':'Drinking water', 'Count': 0}
    if not os.path.isfile(filename) or os.path.getsize(filename) == 0:
        writer = csv.DictWriter(filename, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
        df = pd.DataFrame(dict_habit)
        writer.writeheader()
        writer.writerow(dict_habit)
        # save dataframe to csv
        df["Count"] = df["Count"].astype(int)
        df.to_csv(filename, index=False)
        habits = list(df["Name"])
        return habits
    df = pd.read_csv(filename)
    habits = list(df["Name"])
    return habits

# home page route to display the habits list
@app.route('/', methods=['GET'])
def index():
    context = {
        'datetime': datetime,
        # Other context variables...
    }
    today = datetime.datetime.now()
    today_str = today.strftime("%B %d, %Y")
    habits = read_csv()
    return render_template('habits.html', habits=habits, today_str=today_str, **context)

def write_new_habit(habitName):
    dict_habit = {'User ID': 1, 'Habit ID': 1, 'Name': habitName, 'Count': 0}
    with open("habits.csv", mode="a", newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
        writer.writerow(dict_habit)

def delete_one_habit(habitName):
    habits = read_csv()
    for habit in habits:
        if habit["Name"] == habitName:
            habits.remove(habit)
    return habits

@app.route('/add_habit', methods=['POST'])
def add_habit():
    if request.method == 'POST':
        name = request.form['name']
        if len(name) != 0:
            write_new_habit(name)
    else:
        return "Method Not Allowed"


# function to write the habit data to CSV file
def write_csv(habits):
    habits = read_csv()
    with open('habits.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
        writer.writeheader()
        for habit in habits:
            writer.writerow(habit)

# update habit route to update the count of a habit

@app.route('/update_habit', methods=['POST'])
def update_habit():
    name = request.form['name']
    count = request.form['count']
    habits = read_csv()
    for habit in habits:
        if habit['Name'] == name:
            if count == 1:
                habit['Count'] = int(count) + 1
            else:
                habit['Count'] = 0
            break
    write_csv(habits)
    return redirect('/')


# delete habit route to remove a habit from the list
@app.route('/delete_habit', methods=['DELETE'])
def delete_habit(habits):
    habits = read_csv()
    name = request.form['name']
    habits = delete_one_habit(name)
    write_csv(habits)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
