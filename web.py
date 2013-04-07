from flask import Flask, render_template, request

from sqli.sqli import sql_select_injection, sql_insert_injection


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

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

@app.route('/xss')
def xss():
    return render_template('xss.html')

@app.route('/xss-attr')
def xss_attr():
    return render_template('xss-attr.html')

@app.route('/xss-query')
def xss_query():
    name = request.args.get('name', '')
    response_body = render_template('xss-query.html', name=name)
    return response_body, 200, {'X-XSS-Protection': '0'}

if __name__ == '__main__':
    app.run(debug=True)
