from flask import Flask, render_template, redirect, request
from services.list import *
from services.goal import *

app = Flask(__name__)
# TODO: get id dynamically
USER_ID=1

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
    # if folder exists
    # if no - error page
    # get goals for current folder

    goals = [] #get_goals(user_id, name)
    return render_template('goals_list.html', list_name = name, goals = goals)

@app.post('/')
def add_folder():
    """
    Create new folder (list) for goals and save it for the user.
    """
    list_name = request.form.get('list')
    create_list_by_user_id(USER_ID, list_name)

    return redirect('/')

if __name__ == "__main__":
    app.run()
