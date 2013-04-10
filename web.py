import json

from flask import Flask, render_template, request

from exercises import SQLSelectInjection, SQLInsertInjection


# Initialize the Flask application.
app = Flask(__name__)


@app.route('/password-source')
def password_source():
    return render_template('js-password.html')

@app.route('/xss-form')
def xss_form():
    return render_template('xss-form.html')

@app.route('/xss-attr')
def xss_attr():
    return render_template('xss-attr.html')

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
