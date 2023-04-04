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

if request.method == 'POST':
        # Handle the "Update Habits" button
        if 'update' in request.form:
        # Read the CSV file
            habits = read_habits()
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