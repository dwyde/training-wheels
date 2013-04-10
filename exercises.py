import sqlite3


class BaseExercise(object):
    
    name = ''
    
    template = ''
    
    def process(self, request):
        return {}
    

class PasswordInSource(BaseExercise):
    
    name = 'Password in page source'
    
    template = 'js-password.html'

class ReflectedXSSForm(BaseExercise):
    
    name = 'Script injection in a form'
    
    template = 'xss.html'


class ReflectedXSSAttr(BaseExercise):
    
    name = 'Script injection in an attribute'
    
    template = 'xss-attr.html'


class ReflectedXSSQueryParam(BaseExercise):
    
    name = 'XSS in a query parameter'
    
    template = 'xss-query.html'
    
    def process(self, request):
        return {'name': request.args.get('name', '')}


class BaseSQLInjection(BaseExercise):
    
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

    def process(self, request):
        """ Base method, shared between SQLi exercises. """
        name = request.args.get('name', '')
        query = "SELECT * FROM users WHERE name='{0}'".format(name)
        
        conn = self._init_database()
        with conn:
            cursor = conn.cursor()
            try:
                self._run_query(cursor, query)
            except sqlite3.OperationalError:
                pass
            self._extra_statements(cursor)
            results = cursor.fetchall()
            cursor.close()
        conn.close()
        
        success = self._check_success(results)
        return {'query': query, 'success': success}

    def _run_query(self, cursor, query):
        raise NotImplementedError
    
    def _extra_statements(self, cursor):
        raise NotImplementedError
    
    def _check_success(self, results):
        raise NotImplementedError

class SQLSelectInjection(BaseSQLInjection):
    """ Perform an SQL SELECT query that's vulnerable to injection. """
    
    name = 'SQL SELECT injection'
    
    template = 'sqli.html'
    
    def _run_query(self, cursor, query):
        cursor.execute(query)
    
    def _extra_statements(self, cursor):
        pass
    
    def _check_success(self, results):
        return len(results) == len(self.users)
    

class SQLInsertInjection(BaseSQLInjection):
    """ Allow multiple statements to be executed via SQL injection. """
    
    name = 'SQL INSERT injection'
    
    template = 'sqli.html'
    
    def _run_query(self, cursor, query):
        cursor.executescript(query)
    
    def _extra_statements(self, cursor):
        cursor.execute('SELECT * FROM users')
    
    def _check_success(self, results):
        return len(results) > len(self.users)


# An index of available levels.
EXERCISES = [
    PasswordInSource(),
    ReflectedXSSForm(),
    ReflectedXSSAttr(),
    ReflectedXSSQueryParam(),
    SQLSelectInjection(),
    SQLInsertInjection(),
]
