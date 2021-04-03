import os
import tempfile

import pytest
import json
import todo


@pytest.fixture
def client():
    app = todo.create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            todo.db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
    
def test_empty_db(client):
    """Start with no todos"""

    rv = client.get('/todos')
    assert rv.status_code == 200
    assert rv.data == b'[]'
    
def test_post(client):
    """ Test inserting a single todo"""
    rv = client.post('/todos', json={"title": "GodZilla", "body": "Rain destruction on random city"})
    assert rv.status_code == 201
    assert rv.data == b'{"id": 1}'

def test_put(client):
    """ Test updating a todo"""
     
    #Insert
    rv = client.post('/todos', json={"title": "GodZilla", "body": "Rain destruction on random city"})
    assert rv.status_code == 201
    assert rv.data == b'{"id": 1}'
    
    #Update
    rv = client.put('/todos', json={"id":"1", "title": "Mothra", "body": "Attack specific cities (New York and Tokyo)"})
    assert rv.status_code == 201
    assert rv.data == b'{"id": 1}'
    
    #Fetch (all)
    # TODO: Implement a GET that takes a single ID
    rv = client.get('/todos')
    assert rv.status_code == 200
    assert b'Attack specific cities (New York and Tokyo)' in rv.data
    
