import sqlite3  


# Users to initially load into the database.
USERS = ('david', 'foo')


def init_database():
    """ Initialize an in-memory SQLite database of users. """
    conn = sqlite3.connect(':memory:')
    with conn:
        conn.execute('''CREATE TABLE users (name text)''')
        for user in USERS:
            conn.execute('''INSERT INTO users VALUES (?)''', (user,))
    return conn

def sql_select_injection(name):
    """ Perform an SQL SELECT query that's vulnerable to injection.
    
    The return value indicates whether multiple rows were in the result.
    """
    # name = "' OR '1'='1"
    conn = init_database()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name = '%s'" % name)
        results = cur.fetchall()
        cur.close()
    
    success = len(results) == len(USERS)
    return success

def sql_insert_injection(name):
    """ Allow multiple statements to be executed via SQL injection.
    
    Returns success if a new row was inserted as part of the query.
    """
    # name = "'; INSERT INTO users VALUES ('zz')--"
    conn = init_database()
    with conn:
        cursor = conn.cursor()
        cursor.executescript("SELECT * FROM users WHERE name='%s'" % name)
        cursor.execute('SELECT * FROM users')
        results = cursor.fetchall()
        cursor.close()
    
    success = len(results) > len(USERS)
    return success
