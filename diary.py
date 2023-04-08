from flask import Flask, render_template, request, session
from datetime import datetime
import calendar
from csv import writer
import pandas as pd

app = Flask(__name__)

@app.route('/')
@app.route('/diary')
def page():
    dt = datetime.now()
    week = dt.strftime('%A')
    currentMonth = datetime.now().month
    return render_template('diary.html', month=calendar.month_name[currentMonth], year=datetime.now().year, week=week)

@app.route('/write_csv', methods=['POST'])
def write_csv():
    day_info = [datetime.today().strftime('%Y-%m-%d'), request.form['module'], request.form['value'], \
        request.form['body'], request.form['km'], request.form['heart'], \
        request.form['emotion'], request.form['intelegance'], \
        request.form['action'], request.form['good'], request.form['bad'], \
        request.form['improve'], request.form['day'], request.form['rival']]
    with open('user_info.csv', 'a', encoding='utf-8') as file:
        writer_object = writer(file)
        writer_object.writerow(day_info)
    return render_template('response.html')

@app.route('/diary_info', methods=['GET', 'POST'])
def show_info():
    data = request.form['date']
    content = pd.read_csv("user_info.csv")
    content = content.loc[(content.user_id == session['localId']) & (content['date'].str.contains(data))].iloc[0]
    module = content[2]
    value = content[3]
    body = content[4]
    km = content[5]
    heart = content[6]
    emotion = content[7]
    intelligence = content[8]
    action = content[9]
    good = content[10]
    bad = content[11]
    improve = content[12]
    day = content[13]
    rival = content[14]
    return render_template('diary_info.html', content)


if __name__ == '__main__':
    app.run(debug=True)
