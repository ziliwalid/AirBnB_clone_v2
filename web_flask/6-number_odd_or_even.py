#!/usr/bin/python3
"""
starts a Flask web app
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """returns some other stuff"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    """shows c followed by val of var"""
    return 'C ' + text.replace('_', ' ')

@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pythoniscool(text='is cool'):
    """shows some stuff (explained in the task)"""
    return 'Python ' + text.replace('_', ' ')

@app.route('/number/<int:n>', strict_slashes=False)
def imanumber(n):
    """shows something if n is a num"""
    return "{:d} is a number".format(n)

@app.route('/number_template/<int:n>', strict_slashes=False)
def numsTemp(n):
    """does some displaying"""
    return render_template('5-number.html', n=n)

@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def checkifEVEN(n):
    """display a HTML page only if n is an integer"""
    if n % 2 == 0:
        isEven = 'even'
    else:
        isEven = 'odd'
    return render_template('6-number_odd_or_even.html', n=n,
                           isEven=isEven)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
