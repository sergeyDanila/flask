from flask import Flask, render_template
import re
from jinja2 import evalcontextfilter, Markup, escape
from random import shuffle
import datafile as data


app = Flask(__name__)

# Создадим фильтр для разбиения разрядов в суммах
thousand_separator = re.compile(r'[0-9](?=(?:[0-9]{3})+(?![0-9]))')

@app.template_filter('thousands')
@evalcontextfilter
def add_thousand_separator(eval_ctx, value):
    result = thousand_separator.sub('\g<0> ', escape(value))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


# Для удобства преобразуем Tours (словарь словарей из исходных данных) в список,
# предварительно добавив новый атрибут tour
tours = []
for tour, dict_tours in data.tours.items():
    dict_tours["tour"] = tour
    tours.append(dict_tours)


@app.route('/')
def render_main():
    tours_top = tours[:] #
    shuffle(tours_top)
    return render_template('index.html',
                           departures=data.departures,
                           tour=False,  # Для подсветки направления в меню при выборе тура
                           tours=tours_top[:6])


@app.route('/departures/<departure>/')
def render_departures(departure):
    return render_template('departure.html', departure=departure,
                           departures=data.departures,
                           tour=False,  # Для подсветки направления в меню при выборе тура
                           tours=[d for d in tours if d["departure"] == departure])


@app.route('/tours/<int:id>/')
def render_tours(id):
    return render_template('tour.html', id=id,
                           departures=data.departures,
                           tour=[d for d in tours if d["tour"] == id][0])


if __name__ == '__main__':
    app.run()

