import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()

cur.execute('''CREATE TABLE users (name text)''')
cur.execute('''INSERT INTO users VALUES ('david')''')
cur.execute('''INSERT INTO users VALUES ('foo')''')
conn.commit()

name = raw_input('Retrieve data on at least one user: ')
cur.execute("SELECT * FROM users WHERE name = '%s'" % name)

results = cur.fetchall()
print results
if len(results) == 2:
    print 'Success!'
else:
    print 'Nope!'

# ' OR '1'='1
