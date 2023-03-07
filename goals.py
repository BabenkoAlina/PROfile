from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def index():
    """
    Get main page from templates.
    """
    return render_template("goals_home.html")

@app.route('/per_week')
def goals_week():
    """
    Redirect to the page with specific goals (weekly).
    """
    return render_template('goals_per_week.html')

@app.route('/per_month')
def goals_month():
    """
    Redirect to the page with specific goals (monthly).
    """
    return render_template('goals_per_month.html')

@app.route('/per_year')
def goals_year():
    """
    Redirect to the page with specific goals (yearly).
    """
    return render_template('goals_per_year.html')

if __name__ == "__main__":
    app.run()
