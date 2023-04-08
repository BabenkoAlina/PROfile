import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import io
import base64
from flask import Flask, render_template, session, redirect

app = Flask(__name__)


@app.route('/progress', methods=['GET'])
def progress():
    if 'localId' not in session:
        return redirect('/login')
    df = pd.read_csv('user_info.csv')
    df = df[df.user_id == session['localId']]
    df = df[['date', 'km' ,'emotion', 'action']]
    df.date = np.vectorize(datetime.date.fromisoformat)(df.date)
    today = datetime.date.today()
    last_month_df = df[df.date > today - datetime.timedelta(30)]
    last_week_df = df[df.date > today - datetime.timedelta(7)]
    last_month_km = last_month_df.km.sum()
    last_week_km = last_week_df.km.sum()
    try:
        last_month_emotion = last_month_df.emotion.value_counts().idxmax()
    except ValueError:
        last_month_emotion = ''
    try:
        last_week_emotion = last_week_df.emotion.value_counts().idxmax()
    except ValueError:
        last_week_emotion = ''
    try:
        last_month_action = last_month_df.action.value_counts().idxmax()
    except ValueError:
        last_month_action = ''
    try:
        last_week_action = last_week_df.action.value_counts().idxmax()
    except ValueError:
        last_week_action = ''
    
    goals = pd.read_csv('data/goals.csv')
    goals = goals[goals.user_id == session['localId']]
    goals = goals.status.value_counts().sort_index()
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.pie(goals, colors=['k', 'r'])
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode()
    buf.close()

    return render_template(
        'progress.html',
        last_month_km=last_month_km,
        last_month_emotion=last_month_emotion,
        last_month_action=last_month_action,
        last_week_km=last_week_km,
        last_week_emotion=last_week_emotion,
        last_week_action=last_week_action,
        image=image
    )


# if __name__ == '__main__':
#     app.run('0.0.0.0', 8080, True)