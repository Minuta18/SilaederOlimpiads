import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = '''t6VZtNSacQhe86wxe7qazG60ppN3tpXu6GlnjFt5VqP221fJxbmV4N2ddrPUuIv+vbUwRWzM2+wukXYYqyo9BA=='''