from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_main():
    return render_template('index.html')


@app.route('/departures/<departure>')
def render_departures(departure):
    return render_template('departure.html',departure=departure)


@app.route('/tours/<id>')
def render_tours(id):
    return render_template('tour.html', id=id)


if __name__ == '__main__':
    app.run()
