from flask import Flask, render_template, request

from levels import LEVELS


# Initialize the Flask application.
app = Flask(__name__)


@app.route('/level/<int:level_num>/')
def level(level_num):
    try:
        level_obj = LEVELS[level_num]
    except IndexError:
        return 'Level not found.', 404
    else:
        return level_obj.render(request)

@app.route('/')
def index():
    return render_template('index.html', levels=enumerate(LEVELS))


if __name__ == '__main__':
    app.run(debug=True)
