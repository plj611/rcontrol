from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

print('1')
db = SQLAlchemy()
print('2')

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevConfig)
    db.init_app(app)
    migrate = Migrate(app, db)
    print('__init__')
    with app.app_context():
        from . import routes
        from . import model
        #a = 1 / 0
        print(app.config['ALGORITHMS'])
        return app
    '''
    @app.route("/")
    def home():
        return jsonify({'status': 'ok'})
    return app
    '''