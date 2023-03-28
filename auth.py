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
def main():
    print(session)
    if "email" not in session:
        return redirect('/login')
    else:
        # Тут треба зарендити свій основний шаблон
        return render_template('main.html')
    
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
            # session['localId'] - це і є токен
            session['localId'] = user['localId']
            return "", 302
        except Exception as e:
            return '{"error": "Failed to login"}', 200  
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(port=1111, debug=True)