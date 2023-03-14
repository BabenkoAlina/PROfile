from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__, template_folder="templates")

# function to read the habit data from CSV file
def read_csv():
    habits = []
    if not os.path.exists('habits.csv'):
        with open('habits.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Name', 'Count'])
            writer.writeheader()
    with open('habits.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            habits.append(row)
    return habits

# function to write the habit data to CSV file
def write_csv(habits):
    with open('habits.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Count'])
        writer.writeheader()
        for habit in habits:
            writer.writerow(habit)

# home page route to display the habits list
@app.route('/')
def index():
    habits = read_csv()
    return render_template('habits_phone.html', habits=habits)

# add habit route to add a new habit to the list
# @app.route('/add', methods=['POST'])
# def add_habit():
#     name = request.form['name']
#     habit = {'Name': name, 'Count': '0'}
#     habits = read_csv()
#     habits.append(habit)
#     write_csv(habits)
#     return redirect('/')
import csv
@app.route('/add', methods=['POST'])
def add_habit():
    name = request.form['name']
    habit = {'Name': name, 'Count': '0'}
    # habits = read_csv()
    # habits.append(name)
    with open('habits.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(habit)
    return redirect('/')

# update habit route to update the count of a habit
@app.route('/update', methods=['POST'])
def update_habit():
    name = request.form['name']
    habits = read_csv()
    for habit in habits:
        if habit['Name'] == name:
            if 'count' in request.form:
                habit['Count'] = int(habit['Count']) + 1
            else:
                habit['Count'] = '0'
            break
    write_csv(habits)
    return redirect('/')

# delete habit route to remove a habit from the list
@app.route('/delete', methods=['POST'])
def delete_habit():
    name = request.form['name']
    habits = read_csv()
    habits = [habit for habit in habits if habit['Name'] != name]
    write_csv(habits)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
