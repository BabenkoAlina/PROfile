from flask import Flask, session, render_template, request, redirect
import pyrebase

app = Flask(__name__)

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
app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])

def index():
    if ('user' in session):
        return "Logged in as " + session['user']
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['email'] = email
            return redirect('/home')
        except:
            return "Failed to login"
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=1111)