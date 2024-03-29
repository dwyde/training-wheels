import json
import os.path
import sys
for library in ('Flask-0.9', 'Jinja2-2.6', 'Werkzeug-0.8.3'):
    sys.path.append(os.path.join('lib', library))

from flask import Flask, render_template, request

from exercises import SQLSelectInjection, SQLInsertInjection


# Initialize the Flask application.
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/password-source')
def password_source():
    return render_template('js-password.html')

@app.route('/xss-attr')
def xss_attr():
    return render_template('xss-attr.html'), 200, {'X-XSS-Protection': '0'}

@app.route('/xss-query')
def xss_query():
    return render_template('xss-query.html'), 200, {'X-XSS-Protection': '0'}

def _sqli_base(request, view_klass, template):
    if request.method == 'POST':
        view_obj = view_klass()
        result = view_obj.process(request)
        return json.dumps(result), 200, {'Content-Type': 'application/json'}
    else:
        return render_template(template)

@app.route('/sqli-select', methods=['GET', 'POST'])
def sqli_select():
    return _sqli_base(request, SQLSelectInjection, 'sqli-select.html')

@app.route('/sqli-insert', methods=['GET', 'POST'])
def sqli_insert():
    return _sqli_base(request, SQLInsertInjection, 'sqli-insert.html')

if __name__ == '__main__':
    app.run(debug=True)
