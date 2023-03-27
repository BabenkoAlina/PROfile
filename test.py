# Python:
# from flask import Flask, render_template, request, redirect
# import pandas as pd
# import os
# import csv
# import re
# import datetime

# app = Flask(__name__, template_folder="templates")

# # function to read the habit data from CSV file
# def read_csv():
#     filename = "habits.csv"
#     dict_habit = {'User ID': 1, 'Habit ID': 1, 'Name':'Drinking water', 'Count': 10}
#     if not os.path.isfile(filename) or os.path.getsize(filename) == 0:
#         writer = csv.DictWriter(filename, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
#         df = pd.DataFrame(dict_habit)
#         writer.writeheader()
#         writer.writerow(dict_habit)
#         # save dataframe to csv
#         df["Count"] = df["Count"].astype(int)
#         df.to_csv(filename, index=False)
#         habits = list(df["Name"])
#         return habits
#     df = pd.read_csv(filename)
#     habits = list(df["Name"])
#     return habits

# # home page route to display the habits list
# @app.route('/', methods=['GET'])
# def index():
#     context = {
#         'datetime': datetime,
#         # Other context variables...
#     }
#     today = datetime.datetime.now()
#     today_str = today.strftime("%B %d, %Y")
#     habits = read_csv()
#     return render_template('habits_phone.html', habits=habits, today_str=today_str, **context)

# # def write_new_habit(habitName):
# #     dict_habit = {'User ID': 1, 'Habit ID': 1, 'Name': habitName, 'Count': 10}
# #     with open("habits.csv", mode="a", newline='\n') as file:
# #         writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
# #         writer.writerow(dict_habit)

# @app.route('/add_habit', methods=['POST'])
# def add_habit():
#     if request.method == 'POST':
#         name = request.form['name']
#         habit_df = pd.DataFrame({'User ID': 1, 'Habit ID': 1, 'Name': name, 'Count': 0})
#         if os.path.isfile("habits.csv"):
#             habits_df = pd.read_csv("habits.csv")
#             habits_df = habits_df.append(habit_df, ignore_index=True)
#         else:
#             habits_df = habit_df
#         habits_df.to_csv("habits.csv", index=False)
#         return "Habit added successfully!"
#     else:
#         return "Method Not Allowed"


# # function to write the habit data to CSV file
# def write_csv():
#     habits = read_csv()
#     with open('habits.csv', 'w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=['User ID', 'Habit ID', 'Name', 'Count'])
#         writer.writeheader()
#         for habit in habits:
#             writer.writerow(habit)

# # update habit route to update the count of a habit
# @app.route('/update_habit', methods=['POST'])
# def update_habit():
#     name = request.args.get('habitName')
#     habits = read_csv()
#     for habit in habits:
#         if habit['Name'] == name:
#             if 'count' in request.form:
#                 habit['Count'] = int(habit['Count']) + 1
#             else:
#                 habit['Count'] = 0
#             break
#     write_csv()
#     return redirect('/')

# # delete habit route to remove a habit from the list
# @app.route('/delete_habit', methods=['DELETE'])
# def delete_habit():
#     name = request.args.get('habitName')
#     habits = read_csv()
#     habits = [habit for habit in habits if habit['Name'] != name]
#     write_csv()
#     return redirect('/')

# if __name__ == '__main__':
#     # write_new_habit("Diving")
#     app.run(debug=True)

# HTML:
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Habits List</title>
# 	<link rel="stylesheet" type="text/css" href="static/style.css">
#     <script src="javascript/jquery-3.6.4.js"></script>
# </head>
# <body>
#     <h1>Habits List</h1>
#     <p><span id="current-date"></span></p>
#     <div class="button-container">
#         <button class="day-button {{ 'active' if datetime.datetime.today().weekday() == 0 else '' }}">M</button>
#         <button class="day-button {{ 'active' if datetime.datetime.today().weekday() == 1 else '' }}">T</button>
#         <button class="day-button {{ 'active' if datetime.datetime.today().weekday() == 2 else '' }}">W</button>
#         <button class="day-button {{ 'active' if datetime.datetime.today().weekday() == 3 else '' }}">T</button>
#         <button class="day-button {{ 'active' if datetime.datetime.today().weekday() == 4 else '' }}">F</button>
#         <button class="day-button {{ 'active' if datetime.datetime.today().weekday() == 5 else '' }}">S</button>
#         <button class="day-button {{ 'active' if datetime.datetime.today().weekday() == 6 else '' }}">S</button>
#     </div>
#     <div id="habits-container">
#         <h2>Habits</h2>
#         <ul id="habits-list">
#             {% for habit in habits %}
#             <li>
#                 <span>{{ habit.name }}</span>
#                 <input type="hidden" name="count" value="{{ habit.count }}">
#             </li>
#             {% endfor %}
#         </ul>
#     </div>
    

      
#     <div id="add-habit-modal" class="modal">
#         <div class="modal-content">
#             <span class="close">&times;</span>
#             <form id="add-habit-form" method="POST" action='/add_habit'>
#                 <label for="name">Add new habit:</label>
#                 <input type="text" id="name" name="name">
#                 <input type="submit" value="Add">
#             </form>           
#         </div>
#     </div>
    
#     <button id="add-button">+</button>
    
#     <script>
#         //Set a current date
#         var today = new Date();
#         var currentDate = "{{ today_str }}";
#         // Set date in HTML element
#         document.getElementById("current-date").innerHTML = currentDate;

#         document.getElementById("current-date").innerHTML = currentDate;

#         var addModal = document.getElementById("add-habit-modal");
#         var addButton = document.getElementById("add-button");
#         var closeButton = document.getElementsByClassName("close")[0];

#         addButton.onclick = function() {
#             addModal.style.display = "block";
#         }

#         closeButton.onclick = function() {
#             addModal.style.display = "none";
#         }

#         window.onclick = function(event) {
#             if (event.target == addModal) {
#                 addModal.style.display = "none";
#             }
#         }

#         var habitsList = document.getElementById("habits-list");
#         var addHabitForm = document.getElementById("add-habit-form");

#         addHabitForm.onsubmit = function(event) {
#             event.preventDefault();
#             var habitName = document.getElementById("name").value;
#             var newHabit = document.createElement("li");
#             newHabit.innerHTML = '<span>' + habitName + '</span><input type="checkbox" id="' + habitName + '" name="' + habitName + '" class="habit-checkbox"><button class="delete-button">X</button><input type="hidden" name="count" value=0>';
#             habitsList.appendChild(newHabit);
#             addModal.style.display = "none";
#             addHabitForm.reset();

#             callPythonFunction(habitName);
#         };

#         function callPythonFunction(habitName) {
#             $.post("/add_habit", { name: habitName }, function(data) {
#                 console.log(data);
#             });
#         }
#         // Get all habit items and iterate over them to get their names and call the function
#         var habitItems = document.querySelectorAll("#habits-list li span");
#         habitItems.forEach(function(item) {
#             var habitName = item.textContent;
#             callPythonFunction(habitName);
#         });
        
#         var habitCheckboxes = document.querySelectorAll("#habits-list li input[type='checkbox']");
#         habitCheckboxes.forEach(function(checkbox) {
#             checkbox.addEventListener('change', function() {
#                 var habitName = this.name;
#                 var habitCountInput = this.nextElementSibling.nextElementSibling;
#                 if (this.checked) {
#                     var newCount = parseInt(habitCountInput.value) + 1;
#                     habitCountInput.value = newCount;
#                     upgradeHabit(habitName, newCount);
#                 } else {
#                     habitCountInput.value = 0;
#                 }
#             });
#         });

#         function upgradeHabit(habitName, newCount) {
#             $.post("/upgrade_habit", { name: habitName, count: newCount }, function(data) {
#                 console.log(data);
#             });
#         }

#         habitsList.onclick = function(event) {
#             if (event.target.classList.contains("delete-button")) {
#                 event.target.parentNode.remove();
#             }
#         }

                
#                 // Delete a habit when its delete button is clicked
#                 habitsList.onclick = function(event) {
#                     if (event.target.classList.contains("delete-button")) {
#                         event.target.parentNode.remove();
#                     }
#                 }
#     </script>


#     <div class="fixed">
#         <div class="btn-group">
#             <a href="link1">
#                 <button class="button">Home</button>
#             </a>
#             <a href="link2">
#                 <button class="button">Diary</button>
#             </a>
#             <a href="link3">
#                 <button class="button">Goals</button>
#             </a>
#             <a href="link4 - same link">
#                 <button class="button">Habits</button>
#             </a>
#         </div>
#     </div>
 
# </body>
# </html>


# CSS: 
# body {
#   font-family: Arial, sans-serif;
#   margin: 0;
#   padding: 0;
# }

# h1 {
#   text-align: center;
#   margin-top: 20px;
# }

# #add-habit-modal {
#   display: none;
#   position: fixed;
#   z-index: 1;
#   left: 0;
#   top: 10;
#   width: 100%;
#   height: 100%;
#   overflow: auto;
#   background-color: #fffefe00; 
# }

# .modal-content {
#   background-color: #fff;
#   margin: 15% auto;
#   padding: 20px;
#   border: none;
#   width: 80%;
# }

# .close {
#   color: #aaaaaa;
#   float: right;
#   font-size: 28px;
#   font-weight: bold;
# }

# .close:hover,
# .close:focus {
#   color: #ffffff;
#   text-decoration: none;
#   cursor: pointer;
# }

# #add-habit-form {
#   display: flex;
#   flex-direction: column;
#   align-items: center;
#   margin-top: 10px;
# }

# #add-habit-form label {
#   margin-top: 10px;
#   margin-bottom: 5px;
#   color: #000;
# }

# #add-habit-form input[type="text"] {
#   padding: 5px;
#   border: none;
#   border-bottom: 1px solid #ccc;
#   width: 100%;
#   box-sizing: border-box;
#   background-color: #f2f2f2;
# }

# #add-habit-form input[type="submit"] {
#   margin-top: 10px;
#   padding: 10px 20px;
#   border: none;
#   border-radius: 3px;
#   background-color: #f44336;
#   color: white;
#   cursor: pointer;
# }

# #add-habit-form input[type="submit"]:hover {
#   background-color: #f44336;
# }

# #habits-list {
#   list-style: none;
#   margin: 0;
#   padding: 0;
# }

# .habit {
#   display: flex;
#   align-items: center;
#   padding: 10px;
#   border-bottom: 1px solid #ccc;
# }

# .habit .name {
#   flex-grow: 1;
#   margin-left: 10px;
# }

# .habit .count {
#   display: none;
# }

# .habit input[type="checkbox"] {
#   margin-right: 10px;
#   cursor: pointer;
# }

# .habit .delete {
#   margin-left: 10px;
#   padding: 5px;
#   border: none;
#   border-radius: 50%;
#   background-color: #f44336;
#   color: white;
#   cursor: pointer;
#   font-size: 20px;
#   line-height: 0.7;
#   text-align: center;
#   width: 20px;
#   height: 20px;
# }

# .habit .delete:hover {
#   background-color: #ff6666;
# }
# .button-container {
#   display: flex;
#   justify-content: space-between;
#   align-items: center;
#   width: 80%;
#   margin: 0 auto;
# }

# .day-button {
#   width: 40px;
#   height: 40px;
#   font-size: 1.2rem;
#   color: #333;
#   background-color: #f2f2f2;
#   border: none;
#   border-radius: 50%;
#   cursor: pointer;
# }

# .day-button.active {
#   background-color: red;
#   color: white;
# }

# /* Styles for large screens */
# div.fixed {
#   position: fixed;
#   bottom: 0;
#   width: 100%;
# } 

# .btn-group .button {
#   background-color: #e7e7e7; 
#   border: 1px solid black;
#   color: black;
#   width: auto;
#   padding: 0px 100px;
#   text-align: center;
#   text-decoration: none;
#   display: inline-block;
#   font-size: 50px;
#   cursor: pointer;
# }

# .btn-group .button:hover {
#   background-color: #f44336;
#   color: white;
# }

# /* Styles for smaller screens */
# @media only screen and (max-width: 768px) {
#   .btn-group .button {
#       padding: 0px 50px;
#       font-size: 30px;
#   }
# }
