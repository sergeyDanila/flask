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
    return render_template('index.html',
                           departures=data.departures,
                           tours=shuffle(tours)[:6])


@app.route('/departures/<departure>/')
def render_departures(departure):
    return render_template('departure.html', departure=departure,
                           departures=data.departures,
                           tours=[d for d in tours if d["departure"] == departure])


@app.route('/tours/<int:id>/')
def render_tours(id):
    return render_template('tour.html', id=id,  # stars="★★★★★",
                           departures=data.departures,
                           tour=[d for d in tours if d["tour"] == id][0])


@app.route('/test/')
def render_test():
    return data.tours


if __name__ == '__main__':
    app.run(debug=True)

#print(tours[0])