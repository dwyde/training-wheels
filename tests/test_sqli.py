import unittest
import urllib

import web

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        web.app.config['TESTING'] = True
        self.app = web.app.test_client()

    def test_sqli_select_failure(self):
        rv = self.app.get('/level/3/?name=foo')
        self.assertNotIn('Success', rv.data)

    def test_sqli_select_success(self):
        rv = self.app.get("/level/3/?name=' OR '1'='1")
        self.assertIn('Success', rv.data)

    def test_sqli_select_illegal_sql(self):
        rv = self.app.get("/level/3/?name='")
        self.assertNotIn('Success', rv.data)

    def test_sqli_insert_failure(self):
        rv = self.app.get('/level/4/?name=foo')
        self.assertNotIn('Success', rv.data)

    def test_sqli_insert_success(self):
        name = "'; INSERT INTO users VALUES ('zz')--"
        rv = self.app.get("/level/4/?name={0}".format(name))
        self.assertIn('Success', rv.data)
        
    def test_sqli_insert_illegal_sql(self):
        rv = self.app.get("/level/4/?name='")
        self.assertNotIn('Success', rv.data)

if __name__ == '__main__':
    unittest.main()
