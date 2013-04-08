from flask import render_template

import sqlite3


class BaseLevel(object):
    
    name = ''
    
    template = ''
    
    def process(self, request):
        return {}
    
    def render(self, request):
        context = self.process(request)
        response_body = render_template(self.template, **context)
        return response_body, 200, {'X-XSS-Protection': '0'}


class ReflectedXSSForm(BaseLevel):
    
    name = 'Reflected XSS in an HTML Form'
    
    template = 'xss.html'


class ReflectedXSSAttr(BaseLevel):
    
    name = 'Reflected XSS on an HTML Attribute'
    
    template = 'xss-attr.html'


class ReflectedXSSQueryParam(BaseLevel):
    
    name = 'Reflected XSS in a Query Parameter'
    
    template = 'xss-query.html'
    
    def process(self, request):
        return {'name': request.args.get('name', '')}


class BaseSQLInjection(BaseLevel):
    
    # Users to initially load into the database.
    users = ('david', 'foo')

    def _init_database(self):
        """ Initialize an in-memory SQLite database of users. """
        conn = sqlite3.connect(':memory:')
        with conn:
            conn.execute('''CREATE TABLE users (name text)''')
            for user in self.users:
                conn.execute('''INSERT INTO users VALUES (?)''', (user,))
        return conn


class SQLSelectInjection(BaseSQLInjection):
    """ Perform an SQL SELECT query that's vulnerable to injection. """
    
    name = 'SQL SELECT Injection'
    
    template = 'sqli.html'
    
    def process(self, request):
        # name = "' OR '1'='1"
        #' OR 1=1--
        name = request.args.get('name', '')
        query = "SELECT * FROM users WHERE name='{0}'".format(name)
        
        conn = self._init_database()
        with conn:
            cur = conn.cursor()
            try:
                cur.execute(query)
            except sqlite3.OperationalError:
                pass
            results = cur.fetchall()
            cur.close()
        
        success = len(results) == len(self.users)
        return {'query': query, 'success': success}


class SQLInsertInjection(BaseSQLInjection):
    """ Allow multiple statements to be executed via SQL injection. """
    
    name = 'SQL INSERT Injection'
    
    template = 'sqli.html'
    
    def process(self, request):
        # name = "'; INSERT INTO users VALUES ('zz')--"
        name = request.args.get('name', '')
        query = "SELECT * FROM users WHERE name='{0}'".format(name)
        
        conn = self._init_database()
        with conn:
            cursor = conn.cursor()
            try:
                cursor.executescript(query)
            except sqlite3.OperationalError:
                pass
            cursor.execute('SELECT * FROM users')
            results = cursor.fetchall()
            cursor.close()
    
        success = len(results) > len(self.users)
        return {'query': query, 'success': success}


# An index of available levels.
LEVELS = [
    ReflectedXSSForm(),
    ReflectedXSSAttr(),
    ReflectedXSSQueryParam(),
    SQLSelectInjection(),
    SQLInsertInjection(),
]
