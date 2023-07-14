import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = '''t6VZtNSacQhe86wxe7qazG60ppN3tpXu6GlnjFt5VqP221fJxbmV4N2ddrPUuIv+vbUwRWzM2+wukXYYqyo9BA=='''

# MAIL_SERVER = 'smtp.yandex.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USERNAME = 'olympiadnik.system@yandex.ru'
# MAIL_PASSWORD = '0l.Mp1aDn(k.s3sT3m)'
# MAIL_DEFAULT_SENDER = 'olympiadnik.system@yandex.ru'
