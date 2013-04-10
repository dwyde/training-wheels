from flask import Flask, render_template, request

from exercises import EXERCISES


# Initialize the Flask application.
app = Flask(__name__)


@app.route('/exercise/<int:exercise_num>/')
def exercise(exercise_num):
    try:
        exercise_obj = EXERCISES[exercise_num]
    except IndexError:
        return 'Exercise not found.', 404
    
    context = exercise_obj.process(request)
    response_body = render_template(exercise_obj.template,
                                    title=exercise_obj.name,
                                    exercises=enumerate(EXERCISES),
                                    **context)
    return response_body, 200, {'X-XSS-Protection': '0'}

@app.route('/')
def index():
    return render_template('index.html', exercises=enumerate(EXERCISES))


if __name__ == '__main__':
    app.run(debug=True)
