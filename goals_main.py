from flask import Flask, render_template, redirect, request, flash, url_for
from services.list import *
from services.goal import *
from werkzeug.urls import url_parse

app = Flask(__name__)
app.secret_key = b'session_key'

# TODO: get id dynamically
USER_ID = 1

@app.get("/")
def index():
    """
    Get main page from templates.
    """
    return render_template("goals_home.html", lists=get_lists_by_user_id(USER_ID))

@app.route('/<name>')
def goals(name):
    """
    Redirect to the page with specific goals (weekly).
    """
    goals = get_goals_by_user_id(USER_ID, name)
    return render_template('goals_list.html', list_name = name, goals = goals)

@app.post('/')
def add_list():
    """
    Create new folder (list) for goals and save it for the user.
    """
    try:
        list_name = request.form.get('list')
        if list_name == '' or list_name is None: 
            raise ValueError('A folder with no name cannot be created!')
        create_list_by_user_id(USER_ID, list_name)
    except ValueError as error:
        flash(str(error), 'error')
    finally:
        redirect('/')

@app.post('/goal')
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
        create_goal_by_user_id(USER_ID, goal, list_name)
    except ValueError as error:
        flash(str(error), 'error')
    finally:
        return redirect(url_for('goals', name=list_name))

@app.delete('/goal/<goal_id>')
def delete_goal(goal_id):
    try:
        url = request.referrer
        if url and url_parse(url).path:
            list_name = url_parse(url).path
        if goal_id == '' or goal_id is None:
            raise ValueError('There is already no such goal in the list!')
        change_goal_status(USER_ID, goal_id, 'deleted')
    except ValueError as error:
        flash(str(error), 'error')
    finally:
        return redirect(url_for('goals', name=list_name))

@app.put('/goal/<goal_id>')
def complete_goal(goal_id):
    try:
        url = request.referrer
        if url and url_parse(url).path:
            list_name = url_parse(url).path
        if goal_id == '' or goal_id is None:
            raise ValueError('There is no such goal in the list!')
        change_goal_status(USER_ID, goal_id, 'completed')
    except ValueError as error:
        flash(str(error), 'error')
    finally:
        return redirect(url_for('goals', name=list_name))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True)
