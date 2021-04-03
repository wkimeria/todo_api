import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
#------------------------- User functions ---------------------------------

def fetch_all():
    """ Fetch rows and convert to list """
    db = get_db()
    result = db.execute(
        'SELECT id, title, body from todos'
    ).fetchall()
    
    rows = [dict(row) for row in result]
    
    return rows

def fetch_one(id):
    """ fetch single row """
    db = get_db()
    cursor=db.cursor()
    result = cursor.execute(
        'SELECT id, title, body from todos where id = ?',
         ( id, )
    ).fetchall()
    rows = [dict(row) for row in result]
    
    return rows

def update_one(id, title, body):
    """ Update record by id"""
    
    db = get_db()
    cursor=db.cursor()
    result = cursor.execute(
        'UPDATE todos SET title = ?, body = ? where id = ?',
         ( title, body, id, )
    )
    db.commit()
    
    return None

def delete_one(id):
    """ Update record by id"""
    
    db = get_db()
    cursor=db.cursor()
    result = cursor.execute(
        'DELETE from todos where id = ?',
         (id, )
    )
    db.commit()
    
    return None
