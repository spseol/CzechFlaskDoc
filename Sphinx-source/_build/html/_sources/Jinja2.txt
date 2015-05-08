.. _jinja:

========
Jinja2
========

`Jinja2`_ je šablonovací jazyk pro Python, vytvořený podle Django. Je
rychlý, bezpečný, široce používaný a nabízí sandboxové prostředí pro
zpracovávání šablon.

Proměnné
========

Proměnné mohou obsahovat atributy nebo elementy, ke kterým můžeme přistoupit pomocí tečky nebo hranatých závorek. Následující dva řádky mají stejný význam.

.. code-block:: jinja

    {{ var.attr }}
    {{ var["attr"]}}

Pokud proměnná nebo atribut neexistuje, vrátí se nám nedefinovaná hodnota, což při vytištění zobrazí prázdný string.

Filtry
------

Proměnné mohou být modifikovány filtry. Filtry se od proměnných oddělují
symbolem ``|`` a mohou mít volitelné argumenty v závorkách. Můžeme skládat více
filtrů za sebe, výstup prvního filtru přejde na vstup druhého. Zde je příklad
využití filtrů::

    {{ var|join(", ")|capitalize }}

Komentáře
=========

Pro okomentování části kódu používejte {# Komentář #}. Toto se hodí pro hledání chyb v kódu nebo přidání důležitých informací.

Escapování
==========

Někdy je nutné, aby Jinja2 ignoroval určité části kódu, se kterými by jinak
zacházel jako s proměnnými nebo bloky. Toho můžeme dosáhnout pomocí bloku
``raw``, do kterého vložíme kód, který má být ignorován. Zde je příklad:

.. code-block:: jinja

    {% raw %}
    <ul>
    {%- for item in item_list %}
    <li>{{ item }}</li>
    {% else %}
    <li>No items found</li>
    {%- endfor %}
    </ul>
    {% endraw %}

.. _dědění:

Dědění šablon
=============

Nejužitečnější část jazyku Jinja2 je dědění šablon. Dědění šablon nám umožňuje
vytvořit základní šablonu, která obsahuje všechny elementy naší stránky a
definuje bloky, které mohou dědické šablony přepisovat. 

Rodičovská šablona
------------------

Základní šablona definuje kostru HTML dokumentu pomocí ``{% block %}`` tagů. A
**dědické šablony nám vyplní předdefinované bloky**. Takto může vypadat
jednoduchá kostra:

.. code-block:: jinja

    <!doctype html>
    <head>{% block head %}
        <link rel=stylesheet
            type=text/css href="{{ url_for('static', filename='style.css') }}">
    {% endblock %}</head>
    <body>
        <div class="page">
            <div class="content">
            {% block body %}{% endblock %}
            </div>
        </div>
    </body>

Dědická šablona
---------------

Dědická šablona může vypadat takto:

.. code-block:: jinja

    {% extends "skeleton.html" %}
    
    {% block head %}
        {{ super() }}
        <title>index</title>
    {% endblock %}
    
    {% block body %}
        <h1>This is index</h1>
        <p>This is paragraph</p>
    {% endblock %}

To, že tato šablona rozšiřuje další šablonu, říká tag ``{% extends %}``.
Šablonovací systém, při vyhodnocování této šablony, nejprve vyhledá jejího
rodiče. Extends tag by měl být první tag, protože vše před ním se normálně
vytiskne a může způsobit zmatek. Pro přístup k šabloně v podadresáři můžeme
použít lomítko:

.. code-block:: jinja

    {% extends "kostra/skeleton.html" %}

Není možné použít více bloků se stejným jménem ve stejné šabloně. Pokud by byly
dva stejně pojmenované bloky, rodičovská šablona by nevěděla, který ze dvou
bloků použít. Pokud chcete vypsat stejný blok vícekrát, můžete použít proměnnou
``self`` a zavolat jméno bloku:

.. code-block:: jinja

    {% block body %}AAAA{% endblock %}
    
    Ačka ještě jednou:
    {{ self.body() }}

Je možné vyrenderovat obsah rodičovského bloku zavoláním ``super()``. To nám
vrátí obsah rodičovského bloku a ten můžeme dále rozšířit. Pro lepší
přehlednost je možné napsat jméno bloku na konec endblocku:

.. code-block:: jinja

    {% block head %}
    {{ super() }}
    <title>index</title>
    {% endblock head  %}

V blocích nelze přistoupit k proměnným, které jsou definované v jiných vrstvách:

.. code-block:: jinja

    {%- for item in item_list %}
    {% block neco %}{{ item }}{% endblock %}
    {%- endfor %}

Tento kód by nám vytiskl jen spoustu prázdných řádků, protože uvnitř bloku nelze přistoupit k proměnné item. Toto můžeme změnit přidáním do bloku scoped, což zpřístupní tyto proměnné v daném bloku:

.. code-block:: jinja

    {%- for item in item_list %}
    {% block neco scoped %}{{ item }}{% endblock %}
    {%- endfor %}

Řídící struktury
================

Řídící struktury jsou věci, které řídí tok programu. Například if, elif, else,
for, macro a block. Řídící struktury se nachází uvnitř těchto závorek {% … %}. 

For
---

Řídící struktury jsou věci, které řídí tok programu. Například ``if``,
``elif``, ``else``, ``for``, ``macro`` a ``block``. Řídící struktury se nachází
uvnitř těchto závorek {% … %}. 

.. code-block:: jinja

    <ul>
    {%- for item in item_list %}
        <li>{{ item }}</li>
    {%- endfor %}
    </ul>

Díky tomu, že proměnné v šablonách si zachovávají vlastnosti objektu, je možné
použít i slovník:

.. code-block:: jinja

    <dl>
    {% for key, value in slov.iteritems() %}
        <dt>{{ key|e }}</dt>
        <dd>{{ value|e }}</dd>
    {% endfor %}
    </dl>

Na rozdíl od jazyka Python ve smyčce nemůžeme použít break nebo continue. Ale
můžeme filtrovat seznamy, což nám umožní přeskočit dané položky. Následující
příklad přeskočí všechny skryté položky:

.. code-block:: jinja

    <ul>
    {%- for item in item_list if not item.hidden %}
        <li>{{ item }}</li>
    {%- endfor %}
    </ul>

Pokud žádné opakování neproběhlo, protože je seznam prázdný nebo filtrování
odstranilo všechny položky ze seznamu, můžeme zobrazit náhradní blok pomocí
else:

.. code-block:: jinja

    <ul>
    {%- for item in item_list %}
        <li>{{ item }}</li>
    {% else %}
        <li>No items found</li>
    {%- endfor %}
    </ul>

If
----------

Toto tvrzení je porovnatelné s ``if`` v Pythonu. Můžeme ho použít pro vyzkoušení, jestli proměnná je definovaná, není prázdná nebo není nepravdivá:

.. code-block:: jinja

    {% if not session.logged_in %}
        <a href="{{ url_for('login') }}">log in</a>
    {% else %}
        <a href="{{ url_for('logout') }}">log out</a>
    {% endif %}

Makra
-----

Makra jsou porovnatelná s funkcemi v jiných programovacích jazycích. Jsou
užitečné pro uložení často používaných věcí do znovu použivatelných funkcí. Zde
je příklad vytvoření makra: 

.. code-block:: jinja

    {% macro input(name, value='', type='text', size=16) -%}
        <input name="{{ name }}" value="{{ value|e }}" type="{{ type }}"
                                                       size="{{ size }}">
    {%- endmacro %}

Tímto způsobem můžeme makro zavolat:

.. code-block:: jinja

    <p>Firstname:{{ input("Firstname") }}</p>
    <p>Lastname:{{ input("Lastname") }}</p>
    <p>Nickname:{{ input("Nickname", size="12") }}</p>
    <p>Age:{{ input("Age", type="number", size="3") }}</p>
    <p>Password:{{ input('Password', type='password') }}</p>

Call
----

V některých případech je užitečné předat makro dalšímu makru. Pro tento případ
tu je speciální blok ``call``. Bloku ``call`` můžeme předat argumenty. Zde je
příklad použití bloku call:

.. code-block:: jinja

    {% macro Clanek(title, class='clanek') -%}
      <div class="{{ class }}">
          <h2>{{ title }}</h2>
          <div class="obsah">
            {{ caller() }}
          </div>
        </div>
    {%- endmacro %}

    {% call Clanek("Nadpis") %}
        Text ktery se zobrazi v promenne caller.
    {% endcall %}

Importování
-----------

Jinja2 umožňuje importovat makra z jiných šablon. Je důležité si uvědomit, že
importované šablony nemají přístup k proměnným v aktuální šabloně, pokud
proměnné nejsou globální. Buď můžeme importovat celou šablonu do proměnné, nebo
jen specifická makra. Náš modul může vypadat takto:

.. code-block:: jinja

    {% macro input(name, value='', type='text', size=16) -%}
        <input name="{{ name }}" value="{{ value|e }}" type="{{ type }}"
                                                       size="{{ size }}">
    {%- endmacro %}

    {%- macro textarea(name, value='', rows=10, cols=40) -%}
        <textarea name="{{ name }}" rows="{{ rows }}" 
                                    cols="{{ cols }}">{{ value|e }} </textarea>
    {%- endmacro %} 

Nejjednodušší je importovat celý modul do proměnné:

.. code-block:: jinja

    {% import "forms.html" as forms %}

    <dl>
      <dt>Username</dt>
      <dd>{{ forms.input("autor") }}</dd>
      <dt>Title</dt>
      <dd>{{ forms.input("titulek") }}</dd>
    </dl>
    <p>{{ forms.textarea("clanek") }}</p>

Nebo můžeme importovat jednotlivá makra:

.. code-block:: jinja

    {% from "forms.html" import input, textarea %}
      <dl>
        <dt>Username</dt>
        <dd>{{ input("autor") }}</dd>
        <dt>Title</dt>
        <dd>{{ input("titulek") }}</dd>
      </dl>
    <p>{{ textarea("clanek") }}</p>

Makra a proměnné, jejichž jména začínají jedním nebo více podtržítky jsou soukromá a tak nemohou být importována.

Testování šablon
================

Při hledaní chyb v kódu je užitečné zjistit zdrojový kód, který Jinja2 vyprodukuje z šablon. Toto můžeme zjistit následujícím způsobem:

.. code-block:: python

    from jinja2 import Template
    temp = Template(u'''\
    <!DOCTYPE html>
    <html>
      <head>
        <title>titulek</title>
      </head>
    <body>
    {{ var|e }}
      <ul>
        {% for item in item_list %}
          <li>{{ item }} kostek</li>
        {% endfor %}
      </ul>
      <dl>
        {% for key, value in dict.iteritems() %}
          <dt>{{ key|e }}</dt>
          <dd>{{ value|e }}</dd>
        {% endfor %}
      </dl>
    </body> </html>
    ''')
    print temp.render(
    var = '<h1>neco</h1>',
    item_list = [5, 6, 13, 23, 41],
    dict = {"neco":1,"jine":4, "dalsi":45},
    )

Do ``Template('''…''')`` vložíme šablonu, kterou chceme otestovat a do
``temp.render()`` vložíme proměnné, které chceme, aby šablona převzala. Po
spuštění programu Python vytiskne zdrojový kód do konzole, který Jinja2 vytvoří
z šablony.

