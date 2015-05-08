=====
Flask
=====

.. _Werkzeug: http://werkzeug.pocoo.org/

Flask je framework pro vytváření webových aplikací napsaný v programovacím
jazyku Python. Flask používá šablonovací systém :ref:`jinja` a `Werkzeug`_ WSGI
knihovnu.

Minimální aplikace
==================

Minimální aplikace může vypadat nějak takto::

    from flask import Flask
    app = Flask(__name__)
    @app.route("/")
    def hello_world():
        return "Hello world"
    if __name__ == "__main__":
        app.run()

Tento soubor můžeme uložit jako jméno.py (nikdy svou aplikaci nepojmenujte
flask.py protože by tato aplikace konfliktovala se samotným Flaskem) a aplikaci
spustíme. Po spuštění naší aplikace by se v konzoli mělo objevit::

    * Running on http://127.0.0.1:5000/

Nyní můžeme otevřít libovolný prohlížeč a dojít na adresu
http://127.0.0.1:5000/ ,kde bychom měli vidět náš nápis Hello world. Pokud je
vše v pořádku server můžete zastavit stisknutím kláves ``Ctrl+C``. 

Takže co náš kód udělal? Nejdříve jsme importovali třídu Flask. Instance této
třídy bude naše WSGI aplikace. Dále jsme vytvořili instanci této třídy. První
argument je jméno modulu nebo balíčku naší aplikace. Pokud používáte jediný
modul jako v tomto případě, tak je vždy správné použít ``__name__``. Potom
použijeme ``route()`` dekorátor, abychom flasku řekli jaká URL adresa má
spustit naši funkci. Funkci dáme jméno, které se také používá ke generování URL
adres pro tuto konkrétní funkci, a vrátí zprávu, kterou chceme zobrazit v
uživatelově prohlížeči. Konečně použijeme funkci ``run()`` k spuštění lokálního
webového serveru s naší aplikací. ``if __name__ == "__main__":`` zajišťuje, že
se server spustí jen tehdy pokud je skript spuštěn přímo z Python interpreteru
a ne jako importovaný modul.

Debugovací mód
==============

Pomocí ``run()`` metody spustíme náš server, ale pokaždé, když provedeme změnu v
našem kódu,  musíme manuálně restartovat server. Tohle je velice nešikovné a
proto existuje debugovací mód. Pokud použijete tento mód, server se sám obnoví
při každé změně v kódu a jestli uděláte chybu v kódu tak vám zobrazí debugger.
Zapnout debugger můžeme dvěma způsoby, přitom oba mají stejný efekt::

    app.debug=True
    app.run()

Nebo takto::

    app.run(debug=True)

.. warning::
    Nikdy nenechávejte vývojový webový server se zapnutým debugovacím
    módem naslouchat na jiné než lokální adrese (127.0.0.1). Pokud se k vaší
    aplikaci dostane někdo cizí a aplikace spadne do debugovacího módu
    může tento cizinec dělat na vašem počítači cokoli, co můžete vy.


Směrování
=========

Moderní webové aplikace mají přehledné URL adresy. Toto pomáhá lidem, aby si
tyto adresy zapamatovali, což zvětšuje šanci, že se příště vrátí. Jak už jste
si dříve mohli všimnout, ``route()`` dekorátor se používá k připojení funkce k
URL adrese. Tady je několik příkladů:

::

    @app.route("/")
    def hello_world():
        return "Hello world"

    @app.route("/welcome/")
    def welcome():
        return "Welcome"



URL pravidla Flasku jsou založena na Werkzeug_ směrovacím modulu. Účel tohoto
modulu je zajistit přehledné a jedinečné URL adresy založené na základech
položených Apachem a dřívějšími HTTP servery. Mezi těmito dvěma příklady je
rozdíl:

::

    @app.route("/welcome")
    def welcome():
        return "Welcome"
    @app.route("/welcome/")
    def welcome():
        return "Welcome"



Liší se **lomítkem** na konci URL. V prvním případě URL adresa na konci
neobsahuje lomítko. Při pokusu o vstup na tuto adresu s lomítkem na konci
vznikne ``Error 404``. V druhém případě URL adresa na konci obsahuje lomítko.
Při pokusu o vstup na tuto adresu bez lomítka na konci způsobí to, že nás Flask
přesměruje na adresu s lomítkem. 

Některé části URL adres můžeme udělat dynamické a připojit více pravidel k
funkci.

Proměnné části URL adresách
-----------------------------

Přidání proměnných částí k URL adrese uděláme takto ``<jméno_proměnné>``. Tato
část se potom předá naší funkci jako klíčový argument. Volitelně můžeme k této
části přidat typ této proměnné ``<typ:jméno_proměnné>``. Zde je opět několik
příkladů::

    @app.route("/welcome/<jmeno>")
    def welcome(jmeno):
        return "Welcome %s" %jmeno

    @app.route("/<int:cislo1>/<int:cislo2>")
    def nasobeni(cislo1,cislo2):
        vysledek=cislo1*cislo2
        return "%i * %i = %i" %(cislo1,cislo2,vysledek)

| Existují následující typy: 
| ``int`` –- celá čísla
| ``float`` –- desetinná čísla
| ``path`` –- používá se pro cesty tudíž přijímá I lomítka  


Vytváření URL adres
-------------------

K vytvoření (nebo zjištění) URL adresy pro specifickou funkci můžeme použít
funkci ``url_for()``. Toto je možné provést jak v šablonách tak přímo v kódu.
Tato funkce přijme **jméno funkce** jako první argument a další klíčové
argumenty odpovídající proměnné části pravidla URL. Neznámé proměnné části jsou
připojeny k URL adrese jako dotazové parametry. Zde je příklad:

::

    >>> from flask import Flask, url_for
    >>> app = Flask(__name__)
    >>> @app.route("/ahoj")
    ... def hello_world(): pass
    ... 
    >>> @app.route("/welcome/<jmeno>")
    ... def welcome(jmeno): pass
    ... 
    >>> with app.test_request_context():
    ...  print url_for("hello_world")
    ...  print url_for("welcome", jmeno="Petr", neznama="neco")
    ... 
    /ahoj
    /welcome/Petr?neznama=neco 

Je zde použita ``test_request_context()`` metoda. Tato metoda říká Flasku, aby
se choval, jako kdyby zvládal požadavek i když s ním pracujeme pomocí Python
shellu.

HTTP metody
-----------

HTTP používá různé metody pro přístup na URL adresy. Standardně ``route()``
odpovídá jen ``GET`` požadavkům. Toto však můžeme změnit přidáním argumentu
``metods`` k ``route()`` dekorátoru. Zde je příklad:

.. code-block:: python

    @app.route("/login", methods=["GET", "POST"])
    def login():
    if request.method == "POST":
        login_user()
    else:
        show_form()

HTTP metody říkají serveru, co chce klient dělat s požadovanou stránkou. Zde je několik běžných metod:

**GET**
    Prohlížeč řekne serveru, aby dostal informace, které jsou uložené na této
    stránce a poslal je. Toto je nejpoužívanější metoda. 
**HEAD**
    Prohlížeč řekne serveru, aby dostal informace, ale chce jen hlavičku,
    ne obsah stránky. 
**POST**
    Prohlížeč řekne serveru, že chce na tuto adresu poslat nějakou novou
    informaci a to že server musí zajistit, aby se data uložila jen jednou.
**PUT**
    Tato metoda je podobná POST metodě s tím rozdílem, že server může uložit
    informaci několikrát přepisováním starých hodnot víc než jednou.
**DELETE**
    Odstraní informaci v daném místě.
**OPTIONS** 
    Poskytuje rychlou cestu pro klienta, jak zjistit které metody jsou
    podporovány touto URL adresou.

Statické soubory
================

Dynamické webové aplikace také potřebují statické soubory. Zde jsou většinou
CSS a JavaScript soubory a obrázky. Stačí vytvořit složku pojmenovanou
``static`` vedle naší Flask aplikace.

Adresářová struktura jednoduché webové aplikace může vypadat například
takto::

    .
    ├── application.py
    ├── static
    │   ├── favico.png
    │   ├── script.js
    │   └── styles.css
    └── templates
        ├── base.html
        ├── login.html
        └── welcome.html

Generování URL adres pro statické soubory se provádí takto::

    url_for("static", filename="script.js")

Aby vše fungovalo, soubor musí být uložen ve složce static vedle naší aplikace
``static/script.js``.

Pokud požadujeme, aby se složka se statickými soubory jmenovala jinak, např.
staticke_soubory. Musíme instanci třídy Flask přidat argument
``static_folder='staticke_soubory'``, který má z výchozího nastavení přiřazenou
hodnotu ``'static'``. Podobně to lze provést i pro složku ze šablonami, která
má ve výchozím nastavení hodnotu ``templates``. Zde je příklad::

    app = Flask(__name__, static_folder='staticke_soubory', template_folder='sablony')


Renderování šablon
==================

Generování HTML kódu v Pythonu je poněkud těžkopádné. Proto Flask používá
šablonovací systém :ref:`jinja`.

Pro renderování šablon používáme metodu ``render_tamplate()``. Této metodě
předáme jméno souboru šablony a jména proměnných, které chceme předat
šablonovacímu systému jako klíčové argumenty. Zde je příklad použití této
metody::

    from flask import render_template
    @app.route("/welcome/<jmeno>")
    def welcome(jmeno):
        return render_template("welcome.html", jmeno=jmeno)

Flask bude hledat šablonu ve složce templates vedle naší aplikace. Naše Flask
aplikace by mohla vypadat takto:

::

    ├── application.py
    ├── static
    │   ├── favico.png
    │   ├── script.js
    │   └── styles.css
    └── templates
        ├── base.html
        ├── login.html
        └── welcome.html

Šablony jsou obzvlášť užitečné při použití :ref:`dědění šablon <dědění>`.
Šablonové dědění umožňuje nechat některé elementy na každé stránce, jako
hlavičku, navigaci a patičku. Tudíž stačí vytvořit základní šablonu se všemi
elementy a nastavenými bloky, které mohou ostatní šablony rozšiřovat.

Přistupování k požadavkům
=========================

Pro webové aplikace je důležité, aby reagovaly na data, které klient pošle
serveru. K přistoupení k přicházejícím požadavkům použijeme globální objekt
``request``. Flask pro nás analyzuje přicházející požadavek a dá nám k němu
přístup skrze globální objekt. To, že objekt může být globální, umožňují místní
kontexty.

Objekt request
--------------

O objektu request jsem se již dříve zmiňoval. Zde je několik příkladů použití, ale nejdříve ho musíme importovat:

::

    from flask import request

Aktuální metoda požadavku je dostupná použitím atributu ``method``. 
K přistoupení k datům formuláře můžeme použít atribut ``form``. 
Zde je příklad
obou výše zmíněných atributů:

::

    @app.route("/log", methods=["GET", "POST"])
    def log():
        error = None
        if request.method == 'POST':
            if request.form["username"] != "admin" or request.form["password"] != 'admin':
                error = "Invalid Credentials. Please try again"
            else:
                session["logged_in"] = True
                return redirect(url_for("logok"))
        return render_template("log.html", error=error)

Jestliže klíč atributu form neexistuje, tak vám prohlížeč místo toho zobrazí
chybovou stránku ``400 Bad Request``.

Nahrávání souborů
-----------------

S nahranými soubory můžeme pomocí Flasku jednoduše zacházet. Ujistěte se, že
váš HTML formulář  obsahuje atribut ``enctype=multipart/form-data`` jinak
prohlížeč vaše soubory nepošle.

.. code-block:: html

    <form method="post" enctype="multipart/form-data">
      <p>
        <input type="file" name="file">
        <input type="submit" value="Nahrát">
      </p>
     </form>

Nahrané soubory jsou uloženy v paměti nebo v dočasném místě na souborovém
systému. K těmto souborům můžeme přistoupit pomocí ``files`` atributu objektu
request. Každý nahraný soubor je uložen v tomto slovníku. Chová se stejně, jako
normální objekt ``file``, ale má navíc metodu save(), která umožňuje ukládat
tento soubor na souborový systém serveru. Pokud chcete vědět, jak se soubor
jmenoval u klienta před tím, než se nahraje do vaší aplikace, můžete použít
atribut ``filename``. Ale jméno souboru se dá jednoduše změnit, takže této
hodnotě nikdy nevěřte. Pokud chcete použít jméno souboru klienta pro uložení na
server, pošlete ho funkci ``secure_filename()``, kterou pro vás poskytuje
Werkzeug. Zde je příklad aplikace pro nahrávání souborů:

::

    import os
    from flask import Flask, request, redirect, url_for, send_from_directory
    from werkzeug import secure_filename

    nahravaci_slozka = 'C:\uploads'
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
    <form method="post" enctype="multipart/form-data">
      <p>
        <input type="file" name="file">
        <input type="submit" value="Nahrát">
      </p>
    </form>'''

    
    @app.route('/uploads/<filename>')
    def nahrany_soubor(filename):
        return send_from_directory(app.config['nahravaci_slozka'],filename)
    if __name__ == '__main__':
        app.run(debug=True)

Cookies
-------

Pro přístoupení k cookies používáme atribut ``cookies``. Pro nastavení cookies
použijeme metodu ``set_cookie``. Cookies atribut požadavkového objektu je
slovník se všemi cookies, které klient pošle. Zde je příklad čtení a ukládání
cookies:

::

    from flask import Flask, request, make_response, render_template
    app = Flask(__name__)
    @app.route("/")
    def index():
        username = request.cookies.get("username") #čte cookie username
        resp = make_response(render_template("html.html",username=username))
        resp.set_cookie("username", "Ahoj") #nastaví cookie username hodnotu Ahoj
        return resp
    if __name__ == "__main__":
        app.run(debug=True)

Přesměrování a chyby
--------------------

Pro přesměrování uživatele používáme funkci ``redirect()`` a pro přerušení
požadavku s chybovým kódem používáme funkci ``abort()``:

::

    from flask import Flask, abort, redirect, url_for
    app = Flask(__name__)

    @app.route("/")
    def index():
        return redirect(url_for("prerus"))

    @app.route("/prerus")
    def prerus():
        abort(401)
    
    if __name__ == "__main__":
        app.run(debug=True)

Tento kód nás po přístupu na index přesměruje na ``/prerus``, což přeruší
přístup a zobrazí chybovou stránku ``401 přístup zamítnut``. Vzhled chybových
stránek můžeme změnit pomocí ``errorhandler()`` dekorátoru. Takto například 
určím, jaká stránka se má zobrazit při chybě s kódem ``401``.

::

    @app.errorhandler(401)
    def page_not_found(error):
        return "<h1>Chyba, pristup zamitnut</h1>", 401

Sessions
========

Session nám umožňuje ukládat informace o určitém uživateli z jednoho požadavku
na druhý. Sessions podepisují cookies kryptograficky. To znamená, že uživatel
se může podívat na obsah naší cookie ale nemůže ho změnit, pokud neznají tajný
klíč používaný pro podepisování. Takže pokud chcete používat session, musíte
nastavit tajný klíč. Zde je příklad:

::

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

Aby byl tajný klíč náhodný, je vhodné jej generovat pomocí konzole:

::

    >>> import os
    >>> os.urandom(24)
    "l\xf9op\xc7/'\xd0 t\xb9\xfd\x8d\x1b\x7f<g(\x9e`\xcbt\x11\xfe"

Flashování zpráv
================

Flask má jednoduchý způsob jak podávat zpětné informace uživateli pomocí
flashování zpráv. **Flashovací systém umožňuje nahrát zprávu na konci požadavku
a přistoupit k ní v dalším požadavku**. Toto se používá s šablonou kostry pro
zobrazení zprávy. Pro odeslání zprávy používáme metodu ``flash()`` a pro
zachycení těchto zpráv ``get_flashed_messages()``, která je přístupná i v
šablonách. Zde je příklad:

::

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

Takto vypadá šablona kostry:

.. code-block:: jinja

    <!doctype html>
    <head>
        <link rel=stylesheet 
           type=text/css href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body><div class="page">
    <div class="metanav">
        {% if not session.logged_in %}
            <a href="{{ url_for('login') }}">log in</a>
        {% else %}
            <a href="{{ url_for('logout') }}">log out</a>
        {% endif %}
        </div>
        {% for message in get_flashed_messages() %}
            <div class=flash>{{ message }}</div>
        {% endfor %}
    {% block body %}{% endblock %}
    </div></body>

Index:

.. code-block:: jinja

    {% extends "kostra.html" %}
    {% block body %}
        <h1>This is index</h1>
    {% endblock %}

Login:

.. code-block:: jinja

    {% extends "kostra.html" %}
    {% block body %}
        <h2>Login</h2>
        {% if error %}
            <p class=error><strong>Error:</strong> {{ error }}
        {% endif %}
        <form action="{{ url_for('login') }}" method=post>
          <dl>
              <dt>Username:</dt>
              <dd><input type=text name=username></dd>
              <dt>Password:</dt>
              <dd><input type=password name=password></dd>
              <dd><input type=submit value=Login></dd>
           </dl>
        </form>
    {% endblock %}

