from flask import Flask, session, redirect, url_for, request, render_template, flash
app = Flask(__name__)
app.secret_key = "Tajny klic"
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "admin":
            error = 'Invalid username'
        elif request.form['password'] != "admin":
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('log.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)
