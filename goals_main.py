from flask import Flask, render_template, redirect, request, flash, url_for, session, jsonify
import pyrebase
from services.list import *
from services.goal import *

app = Flask(__name__)
app.secret_key = b'session_key'

firebaseConfig = {
    'apiKey': "AIzaSyAXoO8gg9C8_osWeI3YgUoOZ5Y3_QndNiI",
    'authDomain': "profile-3403b.firebaseapp.com",
    'projectId': "profile-3403b",
    'storageBucket': "profile-3403b.appspot.com",
    'messagingSenderId': "346310265739",
    'appId': "1:346310265739:web:97398d6f17b6945147fd8e",
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def main():
    print(session)
    if "email" not in session:
        return redirect('/login')
    else:
        return render_template('goals_home.html', lists=get_lists_by_user_id(session['localId']))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "email" in session:
        return "Logged in as " + session['email']
    if request.method == 'POST':
        email = request.json["email"]
        password = request.json["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['email'] = email
            return "", 302
        except:
            return '{"error": "Failed to login"}'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if ('email' in session):
        return "Logged in as " + session['email']
    if request.method == 'POST':
        email = request.json["email"]
        password = request.json["password"]
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['email'] = email
            session['localId'] = user['localId']
            return "", 302
        except Exception as e:
            return '{"error": "Failed to login"}', 200  
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

@app.route('/goals/<name>')
def goals(name):
    """
    Redirect to the page with specific goals (weekly).
    """
    goals = get_goals_by_user_id(session['localId'], name)
    return render_template('goals_list.html', list_name = name, goals = goals)

@app.post('/goals')
def add_list():
    """
    Create new folder (list) for goals and save it for the user.
    """
    try:
        list_name = request.form.get('list')
        if list_name == '' or list_name is None: 
            raise ValueError('A folder with no name cannot be created!')
        create_list_by_user_id(session['localId'], list_name)
    except ValueError as error:
        flash(str(error), 'error')
    finally:
        return redirect('/goals')

@app.post('/goals/goal')
def add_goal():
    """
    Create new goal and save it for the user.
    """
    try:
        list_name = request.form.get('list_name')
        goal = request.form.get('goal')
        if list_name == '' or list_name is None:
            raise ValueError('There is no such list!')
        if goal == '' or goal is None:
            raise ValueError('A goal cannot be created without description!')
        create_goal_by_user_id(session['localId'], goal, list_name)
    except ValueError as error:
        flash(str(error), 'error')
    finally:
        return redirect(url_for('goals', name=list_name))

@app.delete('/goals/goal/<goal_id>')
def delete_goal(goal_id):
    try:
        if goal_id == '' or goal_id is None:
            raise ValueError('There is already no such goal in the list!')
        change_goal_status(session['localId'], int(goal_id), 'deleted')
        return jsonify({"code": 200, "message": "Successfully deleted the goal!"})
    except ValueError:
        return jsonify({"code": 400, "message": "Failed to delete the goal!"})

@app.put('/goals/goal/<goal_id>')
def complete_goal(goal_id):
    try:
        if goal_id == '' or goal_id is None:
            raise ValueError('There is no such goal in the list!')
        change_goal_status(session['localId'], int(goal_id), 'completed')
        return jsonify({"code": 200, "message": "Successfully completed the goal!"})
    except ValueError:
        return jsonify({"code": 400, "message": "Failed to update the goal!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True)
