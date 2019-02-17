from mongoengine import connect


def connect_db():
    connect(db='admin', host='localhost',
            username='admin',
            password='admin',
            port=27017)
