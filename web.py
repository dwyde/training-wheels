from flask import Flask, render_template, request

from sqli.sqli import sql_select_injection, sql_insert_injection
from levels import LEVELS


app = Flask(__name__)

@app.route('/sqli')
def sqli():
    name = request.args.get('name', '')
    success = sql_select_injection(name)
    return render_template('sqli.html', success=success, name=name)

@app.route('/sqli-insert')
def sqli_insert():
    name = request.args.get('name', '')
    success = sql_insert_injection(name)
    return render_template('sqli.html', success=success, name=name)

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
