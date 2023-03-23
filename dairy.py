from flask import Flask, render_template, request, session
from datetime import datetime
import calendar
from csv import writer

app = Flask(__name__)

@app.route('/')
@app.route('/dairy')
def page():
    dt = datetime.now()
    week = dt.strftime('%A')
    currentMonth = datetime.now().month
    return render_template('try.html', month=calendar.month_name[currentMonth], year=datetime.now().year, week=week)

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

if __name__ == '__main__':
    app.run(debug=True)
