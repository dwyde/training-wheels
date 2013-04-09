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
    
    context = level_obj.process(request)
    response_body = render_template(level_obj.template,
                                    title=level_obj.name,
                                    levels=enumerate(LEVELS),
                                    **context)
    return response_body, 200, {'X-XSS-Protection': '0'}

@app.route('/')
def index():
    return render_template('index.html', levels=enumerate(LEVELS))


if __name__ == '__main__':
    app.run(debug=True)
