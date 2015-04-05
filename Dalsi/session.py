from flask import Flask, session, redirect, url_for, escape, request
app = Flask(__name__)
app.secret_key = "Tajny klic"
@app.route('/')
def index():
    if 'username' in session:
        return "Logged in as %s <br><a href='logout'>Logout</a>" %escape(session['username'])
    return 'You are not logged in <br><a href="login">Login</a>'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''<form action="" method="post">
    <p>Jmeno:<input type=text name=username>
    <p><input type=submit value=Login>
    </form>'''
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)
