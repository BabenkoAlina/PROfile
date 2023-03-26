from flask import Flask, render_template, request, redirect
import pandas as pd
import os
import csv
import re
import datetime

app = Flask(__name__, template_folder="templates")

# function to read the habit data from CSV file
def read_csv():
    filename = "habits.csv"
    if not os.path.isfile(filename) or os.path.getsize(filename) == 0:
        df = pd.DataFrame({"Name": ["Drinking water"], "Count": 0})
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
    return render_template('habits_phone.html', habits=habits, today_str=today_str, **context)

@app.route('/add_habit', methods=['POST'])
def add_habit():
    if request.method == 'POST':
        name = request.form['name']
        habit_df = pd.DataFrame({"Name": [name], "Count": [0]})
        if os.path.isfile("habits.csv"):
            habits_df = pd.read_csv("habits.csv")
            habits_df = habits_df.append(habit_df, ignore_index=True)
        else:
            habits_df = habit_df
        habits_df.to_csv("habits.csv", index=False)
        return "Habit added successfully!"
    else:
        return "Method Not Allowed"


# function to write the habit data to CSV file
def write_csv():
    habits = read_csv()
    with open('habits.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Count'])
        writer.writeheader()
        for habit in habits:
            writer.writerow(habit)

# update habit route to update the count of a habit
@app.route('/update_habit', methods=['POST'])
def update_habit():
    name = request.args.get('habitName')
    habits = read_csv()
    for habit in habits:
        if habit['Name'] == name:
            if 'count' in request.form:
                habit['Count'] = int(habit['Count']) + 1
            else:
                habit['Count'] = 0
            break
    write_csv()
    return redirect('/')

# delete habit route to remove a habit from the list
@app.route('/delete_habit', methods=['DELETE'])
def delete_habit():
    name = request.args.get('habitName')
    habits = read_csv()
    habits = [habit for habit in habits if habit['Name'] != name]
    write_csv()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
