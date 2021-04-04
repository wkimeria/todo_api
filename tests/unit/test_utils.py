import os
import unittest
import flask

 
import todo
from todo import db
from todo import utils
 
 
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = todo.create_app()
        self.app = app.test_client()
        
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
    def test_ensure_json(self):
        app = flask.Flask(__name__)
        with app.test_request_context(json={"title":"boo", "body": "Ya"}):
            assert utils.ensure_json(flask.request) == {'title': 'boo', 'body': 'Ya'}
          
        with app.test_request_context():
            assert utils.ensure_json(flask.request) == None
 
if __name__ == "__main__":
    unittest.main()