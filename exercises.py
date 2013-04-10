import sqlite3


class BaseSQLInjection(object):
    
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
        name = request.form.get('name', '')
        query = "SELECT * FROM users WHERE name='{0}'".format(name)
        
        conn = self._init_database()
        with conn:
            cursor = conn.cursor()
            try:
                self._run_query(cursor, query)
            except (sqlite3.OperationalError, sqlite3.Warning):
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
