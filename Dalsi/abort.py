from flask import Flask, abort, redirect, url_for
app = Flask(__name__)
@app.errorhandler(401)
def page_not_found(error):
    return "<h1>Chyba, pristup zamitnut</h1>", 401
@app.route("/")
def index():
    return redirect(url_for("prerus"))
@app.route("/prerus")
def prerus():
    abort(401)
if __name__ == "__main__":
    app.run(debug=True)
    