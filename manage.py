import os
from flask_script import Manager

from app import create_app

app = create_app(os.getenv('FLASKY_CONFIG', 'default'))
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
