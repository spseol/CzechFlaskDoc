# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 14:23:04 2014

@author: Carko
"""
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
nahravaci_slozka = 'C:\Users\Carko\Desktop\uploads'
povolene_pripony = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['nahravaci_slozka'] = nahravaci_slozka
def povoleny_soubor(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in povolene_pripony
@app.route('/', methods=['GET', 'POST'])
def nahrat_soubor():
    if request.method == 'POST':
        file = request.files['file']
        if file and povoleny_soubor(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['nahravaci_slozka'], filename))
            return redirect(url_for('nahrany_soubor',filename=filename))
    return '''<!doctype html><title>Nahraj nový soubor</title>
<h1>Nahraj nový soubor</h1>
<form action="" method=post enctype=multipart/form-data>
<p><input type=file name=file><input type=submit value=Nahrát>
</form>'''
@app.route('/uploads/<filename>')
def nahrany_soubor(filename):
    return send_from_directory(app.config['nahravaci_slozka'],filename)
if __name__ == '__main__':
    app.run(debug=True)
