#!/usr/bin/env python3
'''
  This demo application demonstrates the functionality of the safrs documented REST API
  After installing safrs with pip, you can run this app standalone:
  $ python3 demo_relationship.py [Listener-IP]

  This will run the example on http://Listener-Ip:5000

  - A database is created and a user is added
  - A rest api is available
  - swagger documentation is generated

  This is a minimal example, you'll probably want to use demo_relationship_ext.py instead!!!
'''
import sys
import logging
import builtins
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from safrs import SAFRSBase, SAFRSAPI, jsonapi_rpc

db = SQLAlchemy()


class Response(SAFRSBase, db.Model):
    '''
        description: Response description
    '''
    __tablename__ = 'Responses'
    id = db.Column(db.String, primary_key=True)
    response_data = db.Column(db.String, default='')


if __name__ == '__main__':
    HOST = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    PORT = 5000
    app = Flask('SAFRS Demo Application')
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite://', DEBUG=True)
    db.init_app(app)
    db.app = app
    # Create the database
    db.create_all()
    API_PREFIX = ''
    
    with app.app_context():
        # Create a user and a book and add the book to the user.books relationship
        response = Response(response_data='{}')
        api = SAFRSAPI(app, host='{}:{}'.format(HOST,PORT), port=PORT, prefix=API_PREFIX)
        # Expose the database objects as REST API endpoints
        api.expose_object(Response)
        # Register the API at /api/docs
        print('Starting API: http://{}:{}{}'.format(HOST, PORT, API_PREFIX))
        app.run(host=HOST, port=PORT)
