import functools
import json

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, Flask
)


from todo.db import *

bp = Blueprint('todos', __name__, url_prefix='/todos')
app = Flask(__name__)

@bp.route('', methods=('POST', 'GET', 'PUT', 'DELETE'))
def process():
    
    if request.method == 'DELETE':
        
        # the todo id will be in the JSON
        try:
            data = request.get_json()
        except Exception as e: # work on python 3.x
            app.logger.error('Unable to parse POST data'+ str(e))
            response = app.response_class(
                response = '{"error":"Invalid input. Must be valid JSON"}',
                status=400,
                mimetype='application/json'
            )
            return response
            
        id = data['id'] # Required
        
        # Fetch record
        record = fetch_one(id)
        
        if len(record) == 0:
            response = app.response_class(
                response = '{"error":"Record not found"}',
                status=404,
                mimetype='application/json'
            )
            return response
        
        delete_one(id)
        
        id_data = {"id": id}

        # Return as JSON
        response = app.response_class(
            response = json.dumps(id_data),
            status=201,
            mimetype='application/json'
        )
        return response
         
    if request.method == 'PUT':
        # the todo id will be in the JSON
        try:
            data = request.get_json()
        except Exception as e: # work on python 3.x
            app.logger.error('Unable to parse POST data'+ str(e))
            response = app.response_class(
                response = '{"error":"Invalid input. Must be valid JSON"}',
                status=400,
                mimetype='application/json'
            )
            return response
            
        id = data['id'] # Required
        title = data.get('title')
        body = data.get('body')
        
        # Fetch record
        record = fetch_one(id)
        app.logger.error('RECORD'+ str(len(record)))
        
        if len(record) == 0:
            response = app.response_class(
                response = '{"error":"Record not found"}',
                status=404,
                mimetype='application/json'
            )
            return response
        
        update_one(id, title, body)
        
        id_data = {"id": record[0].get('id')}
        
        # Return as JSON
        response = app.response_class(
            response = json.dumps(id_data),
            status=201,
            mimetype='application/json'
        )
        return response
       

    if request.method == 'POST':
       
        # Data must be JSON
        try:
            data = request.get_json()
        except Exception as e: # work on python 3.x
            app.logger.error('Unable to parse POST data'+ str(e))
            response = app.response_class(
                response = '{"error":"Invalid input. Must be valid JSON"}',
                status=400,
                mimetype='application/json'
            )
            return response
            
        title = data['title']
        body = data['body']
        
        db = get_db()
        
        cursor=db.cursor()
        cursor.execute(
                'INSERT INTO todos (title, body) VALUES (?, ?)',
                (title, body)
            )
        id_data = {"id": cursor.lastrowid}
        db.commit()
        
        # Return as JSON
        response = app.response_class(
            response = json.dumps(id_data),
            status=201,
            mimetype='application/json'
        )
        return response
    
    if request.method == 'GET':
        # Get all rows
        rows = fetch_all()
        
        # Return as JSON
        response = app.response_class(
            response=json.dumps(rows),
            status=200,
            mimetype='application/json'
        )
        return response
    


    
    

    
        
    
